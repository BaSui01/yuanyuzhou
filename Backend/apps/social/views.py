from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.core.cache import cache
from django.utils import timezone
from apps.core.permissions import IsOwnerOrReadOnly
from apps.core.exceptions import ValidationError
from .models import (
    Friendship, Group, GroupMembership, Post, PostLike, Comment, CommentLike,
    Message, Conversation, Follow, Notification, PostShare
)
from .serializers import (
    FriendshipSerializer, GroupListSerializer, GroupSerializer,
    PostListSerializer, PostSerializer, CommentSerializer, MessageSerializer,
    ConversationSerializer, FollowSerializer, NotificationSerializer,
    PostShareSerializer, SendFriendRequestSerializer, JoinGroupSerializer,
    SendMessageSerializer, UserSocialStatsSerializer
)
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class FriendshipListView(generics.ListAPIView):
    """好友关系列表视图"""
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get('status', 'accepted')

        if status_filter == 'pending_received':
            # 收到的好友请求
            return Friendship.objects.filter(
                to_user=user,
                status='pending'
            ).select_related('from_user', 'to_user')
        elif status_filter == 'pending_sent':
            # 发送的好友请求
            return Friendship.objects.filter(
                from_user=user,
                status='pending'
            ).select_related('from_user', 'to_user')
        else:
            # 已接受的好友
            return Friendship.objects.filter(
                Q(from_user=user) | Q(to_user=user),
                status='accepted'
            ).select_related('from_user', 'to_user')


class GroupListView(generics.ListCreateAPIView):
    """群组列表视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GroupSerializer
        return GroupListSerializer

    def get_queryset(self):
        queryset = Group.objects.filter(is_active=True)

        # 过滤条件
        group_type = self.request.query_params.get('type')
        if group_type:
            queryset = queryset.filter(group_type=group_type)

        # 我的群组
        if self.request.query_params.get('my_groups') == 'true':
            queryset = queryset.filter(
                Q(creator=self.request.user) |
                Q(members=self.request.user)
            ).distinct()

        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        return queryset.order_by('-member_count').select_related('creator')


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """群组详情视图"""
    queryset = Group.objects.filter(is_active=True)
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        # 检查访问权限
        if obj.group_type == 'secret':
            if not obj.memberships.filter(user=self.request.user).exists():
                raise ValidationError("您没有权限访问此群组")
        return obj


class PostListView(generics.ListCreateAPIView):
    """动态列表视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostSerializer
        return PostListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(is_active=True)

        # 获取动态类型
        feed_type = self.request.query_params.get('feed_type', 'public')

        if feed_type == 'friends':
            # 好友动态
            friend_ids = Friendship.objects.filter(
                Q(from_user=user) | Q(to_user=user),
                status='accepted'
            ).values_list('from_user_id', 'to_user_id')

            friend_user_ids = set()
            for from_id, to_id in friend_ids:
                friend_user_ids.add(from_id if from_id != user.id else to_id)

            queryset = queryset.filter(
                Q(author=user) | Q(author_id__in=friend_user_ids),
                visibility__in=['public', 'friends']
            )
        elif feed_type == 'my_posts':
            # 我的动态
            queryset = queryset.filter(author=user)
        elif feed_type == 'group':
            # 群组动态
            group_id = self.request.query_params.get('group_id')
            if group_id:
                queryset = queryset.filter(group_id=group_id)
        else:
            # 公开动态
            queryset = queryset.filter(visibility='public')

        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(content__icontains=search)

        return queryset.order_by('-is_pinned', '-created_at').select_related(
            'author', 'group'
        ).prefetch_related('attachments', 'tags')


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """动态详情视图"""
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        # 检查可见性权限
        if obj.visibility == 'private' and obj.author != user:
            raise ValidationError("您没有权限查看此动态")
        elif obj.visibility == 'friends':
            if not Friendship.are_friends(user, obj.author) and obj.author != user:
                raise ValidationError("您没有权限查看此动态")

        return obj


class CommentListView(generics.ListCreateAPIView):
    """评论列表视图"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(
            post_id=post_id,
            is_active=True,
            parent__isnull=True  # 只获取顶级评论
        ).select_related('author', 'post').prefetch_related('replies')


class ConversationListView(generics.ListAPIView):
    """对话列表视图"""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).order_by('-last_message_at').prefetch_related('participants')


class MessageListView(generics.ListCreateAPIView):
    """消息列表视图"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=self.request.user
        )

        # 标记消息为已读
        conversation.messages.filter(
            is_read=False,
            sender__ne=self.request.user
        ).update(is_read=True, read_at=timezone.now())

        return conversation.messages.order_by('created_at').select_related('sender')


class NotificationListView(generics.ListAPIView):
    """通知列表视图"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(
            recipient=self.request.user
        ).select_related('sender')

        # 过滤条件
        notification_type = self.request.query_params.get('type')
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)

        unread_only = self.request.query_params.get('unread_only')
        if unread_only == 'true':
            queryset = queryset.filter(is_read=False)

        return queryset.order_by('-created_at')


class FollowListView(generics.ListAPIView):
    """关注关系列表视图"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', self.request.user.id)
        follow_type = self.request.query_params.get('type', 'following')

        if follow_type == 'followers':
            return Follow.objects.filter(
                followed_id=user_id
            ).select_related('follower', 'followed')
        else:
            return Follow.objects.filter(
                follower_id=user_id
            ).select_related('follower', 'followed')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request(request):
    """发送好友请求"""
    try:
        serializer = SendFriendRequestSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            to_user = User.objects.get(id=serializer.validated_data['to_user_id'])

            friendship = Friendship.objects.create(
                from_user=request.user,
                to_user=to_user,
                status='pending'
            )

            # 创建通知
            Notification.create_notification(
                recipient=to_user,
                notification_type='friend_request',
                title='新的好友请求',
                content=f'{request.user.username} 向您发送了好友请求',
                sender=request.user,
                related_object=friendship
            )

            logger.info(f"用户 {request.user.username} 向 {to_user.username} 发送好友请求")
            return Response({'message': '好友请求发送成功'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"发送好友请求失败: {str(e)}")
        return Response(
            {'error': '发送好友请求失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request(request, friendship_id):
    """接受好友请求"""
    try:
        friendship = get_object_or_404(
            Friendship,
            id=friendship_id,
            to_user=request.user,
            status='pending'
        )

        # 更新好友关系状态
        friendship.status = 'accepted'
        friendship.updated_at = timezone.now()
        friendship.save()

        # 创建通知
        Notification.objects.create(
            recipient=friendship.from_user,
            sender=request.user,
            notification_type='friend_request_accepted',
            content=f"{request.user.username} 接受了您的好友请求",
            related_object_id=friendship.id,
            related_object_type='friendship'
        )

        return Response({
            'message': '已接受好友请求',
            'friendship': FriendshipSerializer(friendship).data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"接受好友请求出错: {str(e)}")
        return Response({
            'error': '处理好友请求时出错'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_friend_request(request, request_id):
    """拒绝好友请求"""
    try:
        friendship = get_object_or_404(
            Friendship,
            id=request_id,
            to_user=request.user,
            status='pending'
        )

        # 删除好友请求
        friendship.delete()

        # 创建通知
        Notification.objects.create(
            recipient=friendship.from_user,
            sender=request.user,
            notification_type='friend_request_rejected',
            content=f"{request.user.username} 拒绝了您的好友请求",
            related_object_id=friendship.from_user.id,
            related_object_type='user'
        )

        return Response({
            'message': '已拒绝好友请求'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"拒绝好友请求出错: {str(e)}")
        return Response({
            'error': '处理好友请求时出错'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_friend(request, user_id):
    """删除好友"""
    try:
        friend = get_object_or_404(User, id=user_id)

        # 查找并删除好友关系
        friendship = Friendship.objects.filter(
            (Q(from_user=request.user, to_user=friend) |
             Q(from_user=friend, to_user=request.user)),
            status='accepted'
        ).first()

        if not friendship:
            return Response({
                'error': '您与该用户不是好友关系'
            }, status=status.HTTP_400_BAD_REQUEST)

        friendship.delete()

        logger.info(f"用户 {request.user.username} 删除了好友 {friend.username}")
        return Response({'message': '已删除好友关系'})

    except Exception as e:
        logger.error(f"删除好友失败: {str(e)}")
        return Response(
            {'error': '删除好友失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def friend_suggestions(request):
    """好友推荐"""
    try:
        user = request.user

        # 获取当前好友ID列表
        friend_ids = Friendship.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status='accepted'
        ).values_list('from_user_id', 'to_user_id')

        existing_friend_ids = set()
        for from_id, to_id in friend_ids:
            existing_friend_ids.add(from_id if from_id != user.id else to_id)

        # 获取好友的好友（朋友的朋友）
        friends_of_friends_ids = set()
        for friend_id in existing_friend_ids:
            ff_ids = Friendship.objects.filter(
                Q(from_user_id=friend_id) | Q(to_user_id=friend_id),
                status='accepted'
            ).values_list('from_user_id', 'to_user_id')

            for from_id, to_id in ff_ids:
                if from_id != user.id and from_id != friend_id:
                    friends_of_friends_ids.add(from_id)
                if to_id != user.id and to_id != friend_id:
                    friends_of_friends_ids.add(to_id)

        # 排除已经是好友的用户
        suggestion_ids = friends_of_friends_ids - existing_friend_ids

        # 获取推荐用户信息
        suggestions = User.objects.filter(id__in=suggestion_ids)[:10]

        # 序列化结果
        from apps.users.serializers import UserListSerializer
        serializer = UserListSerializer(suggestions, many=True)

        return Response(serializer.data)

    except Exception as e:
        logger.error(f"获取好友推荐失败: {str(e)}")
        return Response(
            {'error': '获取好友推荐失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_group(request):
    """加入群组"""
    try:
        serializer = JoinGroupSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            group = Group.objects.get(id=serializer.validated_data['group_id'])
            membership = group.add_member(request.user)

            if membership:
                logger.info(f"用户 {request.user.username} 加入群组 {group.name}")
                return Response({'message': '成功加入群组'})
            else:
                return Response(
                    {'error': '加入群组失败'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"加入群组失败: {str(e)}")
        return Response(
            {'error': '加入群组失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def leave_group(request, group_id):
    """离开群组"""
    try:
        group = get_object_or_404(Group, id=group_id, is_active=True)

        if group.remove_member(request.user):
            logger.info(f"用户 {request.user.username} 离开群组 {group.name}")
            return Response({'message': '成功离开群组'})
        else:
            return Response(
                {'error': '您不是该群组的成员'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        logger.error(f"离开群组失败: {str(e)}")
        return Response(
            {'error': '离开群组失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def invite_to_group(request, group_id):
    """邀请用户加入群组"""
    try:
        group = get_object_or_404(Group, id=group_id, is_active=True)
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {'error': '请提供用户ID'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 检查邀请人是否是群组成员
        if not group.is_member(request.user):
            return Response(
                {'error': '您不是该群组的成员，无法发送邀请'},
                status=status.HTTP_403_FORBIDDEN
            )

        # 获取被邀请用户
        invited_user = get_object_or_404(User, id=user_id)

        # 检查用户是否已经是成员
        if group.is_member(invited_user):
            return Response(
                {'error': '该用户已经是群组成员'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 创建通知
        Notification.objects.create(
            recipient=invited_user,
            sender=request.user,
            notification_type='group_invitation',
            content=f"{request.user.username} 邀请您加入群组 {group.name}",
            related_object_id=group.id,
            related_object_type='group'
        )

        logger.info(f"用户 {request.user.username} 邀请 {invited_user.username} 加入群组 {group.name}")
        return Response({'message': '邀请已发送'})

    except Exception as e:
        logger.error(f"邀请加入群组失败: {str(e)}")
        return Response(
            {'error': '邀请失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    """点赞动态"""
    try:
        post = get_object_or_404(Post, id=post_id, is_active=True)

        like, created = PostLike.objects.get_or_create(
            post=post,
            user=request.user
        )

        if created:
            post.update_like_count()

            # 创建通知
            if post.author != request.user:
                Notification.create_notification(
                    recipient=post.author,
                    notification_type='like',
                    title='有人点赞了您的动态',
                    content=f'{request.user.username} 点赞了您的动态',
                    sender=request.user,
                    related_object=post
                )

            return Response({'message': '点赞成功'})
        else:
            like.delete()
            post.update_like_count()
            return Response({'message': '取消点赞'})

    except Exception as e:
        logger.error(f"点赞动态失败: {str(e)}")
        return Response(
            {'error': '点赞失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, post_id):
    """取消点赞动态"""
    try:
        post = get_object_or_404(Post, id=post_id, is_active=True)

        # 查找并删除点赞记录
        like = PostLike.objects.filter(post=post, user=request.user).first()

        if like:
            like.delete()
            post.update_like_count()
            return Response({'message': '已取消点赞'})
        else:
            return Response(
                {'error': '您未点赞此动态'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        logger.error(f"取消点赞失败: {str(e)}")
        return Response(
            {'error': '取消点赞失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def share_post(request, post_id):
    """分享动态"""
    try:
        original_post = get_object_or_404(Post, id=post_id, is_active=True)

        # 检查是否有权限查看原动态
        if original_post.visibility == 'private' and original_post.author != request.user:
            return Response(
                {'error': '您没有权限分享此动态'},
                status=status.HTTP_403_FORBIDDEN
            )
        elif original_post.visibility == 'friends':
            if not Friendship.are_friends(request.user, original_post.author) and original_post.author != request.user:
                return Response(
                    {'error': '您没有权限分享此动态'},
                    status=status.HTTP_403_FORBIDDEN
                )

        # 创建分享记录
        content = request.data.get('content', '')
        visibility = request.data.get('visibility', 'public')

        # 创建新的动态作为分享
        shared_post = Post.objects.create(
            author=request.user,
            content=content,
            visibility=visibility
        )

        # 创建分享关联
        PostShare.objects.create(
            shared_post=shared_post,
            original_post=original_post
        )

        # 更新原动态的分享计数
        original_post.update_share_count()

        # 创建通知
        if original_post.author != request.user:
            Notification.objects.create(
                recipient=original_post.author,
                sender=request.user,
                notification_type='share',
                content=f"{request.user.username} 分享了您的动态",
                related_object_id=shared_post.id,
                related_object_type='post'
            )

        return Response({
            'message': '分享成功',
            'post_id': shared_post.id
        })

    except Exception as e:
        logger.error(f"分享动态失败: {str(e)}")
        return Response(
            {'error': '分享失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_comment(request, comment_id):
    """点赞评论"""
    try:
        comment = get_object_or_404(Comment, id=comment_id, is_active=True)

        like, created = CommentLike.objects.get_or_create(
            comment=comment,
            user=request.user
        )

        if created:
            comment.update_like_count()

            # 创建通知
            if comment.author != request.user:
                Notification.create_notification(
                    recipient=comment.author,
                    notification_type='like',
                    title='有人点赞了您的评论',
                    content=f'{request.user.username} 点赞了您的评论',
                    sender=request.user,
                    related_object=comment
                )

            return Response({'message': '点赞成功'})
        else:
            like.delete()
            comment.update_like_count()
            return Response({'message': '取消点赞'})

    except Exception as e:
        logger.error(f"点赞评论失败: {str(e)}")
        return Response(
            {'error': '点赞失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """关注用户"""
    try:
        followed_user = get_object_or_404(User, id=user_id)

        if followed_user == request.user:
            return Response(
                {'error': '不能关注自己'},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            followed=followed_user
        )

        if created:
            # 创建通知
            Notification.create_notification(
                recipient=followed_user,
                notification_type='follow',
                title='有新的关注者',
                content=f'{request.user.username} 关注了您',
                sender=request.user,
                related_object=follow
            )

            logger.info(f"用户 {request.user.username} 关注了 {followed_user.username}")
            return Response({'message': '关注成功'})
        else:
            follow.delete()
            logger.info(f"用户 {request.user.username} 取消关注了 {followed_user.username}")
            return Response({'message': '取消关注'})

    except Exception as e:
        logger.error(f"关注用户失败: {str(e)}")
        return Response(
            {'error': '关注失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_message(request):
    """发送消息"""
    try:
        serializer = SendMessageSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            data = serializer.validated_data

            # 获取或创建对话
            if data.get('conversation_id'):
                conversation = Conversation.objects.get(id=data['conversation_id'])
            else:
                recipient = User.objects.get(id=data['recipient_id'])
                # 查找现有对话
                conversation = Conversation.objects.filter(
                    conversation_type='private',
                    participants=request.user
                ).filter(participants=recipient).first()

                if not conversation:
                    # 创建新对话
                    conversation = Conversation.objects.create(
                        conversation_type='private'
                    )
                    conversation.participants.add(request.user, recipient)

            # 创建消息
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=data['content'],
                message_type=data.get('message_type', 'text')
            )

            # 更新对话的最后消息
            conversation.update_last_message(message)

            logger.info(f"用户 {request.user.username} 发送了消息")
            return Response({
                'message': '消息发送成功',
                'data': MessageSerializer(message).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"发送消息失败: {str(e)}")
        return Response(
            {'error': '发送消息失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notifications_read(request):
    """标记通知为已读"""
    try:
        notification_ids = request.data.get('notification_ids', [])

        if notification_ids:
            notifications = Notification.objects.filter(
                id__in=notification_ids,
                recipient=request.user,
                is_read=False
            )
        else:
            notifications = Notification.objects.filter(
                recipient=request.user,
                is_read=False
            )

        count = notifications.update(
            is_read=True,
            read_at=timezone.now()
        )

        return Response({'message': f'已标记 {count} 条通知为已读'})

    except Exception as e:
        logger.error(f"标记通知失败: {str(e)}")
        return Response(
            {'error': '标记通知失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_social_stats(request):
    """获取用户社交统计"""
    try:
        user = request.user

        # 缓存键
        cache_key = f'user_social_stats_{user.id}'
        cached_stats = cache.get(cache_key)
        if cached_stats:
            return Response(cached_stats)

        # 计算统计信息
        stats = {
            'posts_count': Post.objects.filter(author=user, is_active=True).count(),
            'friends_count': Friendship.objects.filter(
                Q(from_user=user) | Q(to_user=user),
                status='accepted'
            ).count(),
            'followers_count': Follow.objects.filter(followed=user).count(),
            'following_count': Follow.objects.filter(follower=user).count(),
            'groups_count': GroupMembership.objects.filter(user=user).count(),
            'total_likes_received': PostLike.objects.filter(post__author=user).count(),
            'total_comments_received': Comment.objects.filter(post__author=user, is_active=True).count(),
            'most_liked_post': '暂无数据',
            'most_active_group': '暂无数据'
        }

        # 获取最多点赞的动态
        most_liked = Post.objects.filter(
            author=user,
            is_active=True
        ).order_by('-like_count').first()
        if most_liked:
            stats['most_liked_post'] = most_liked.content[:50]

        # 获取最活跃的群组
        most_active_group = GroupMembership.objects.filter(
            user=user
        ).select_related('group').first()
        if most_active_group:
            stats['most_active_group'] = most_active_group.group.name

        # 缓存结果
        cache.set(cache_key, stats, 300)  # 缓存5分钟

        serializer = UserSocialStatsSerializer(stats)
        return Response(serializer.data)

    except Exception as e:
        logger.error(f"获取用户社交统计失败: {str(e)}")
        return Response(
            {'error': '获取统计信息失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_counts(request):
    """获取未读消息数量"""
    try:
        user = request.user

        counts = {
            'unread_messages': Message.objects.filter(
                conversation__participants=user,
                is_read=False,
                sender__ne=user
            ).count(),
            'unread_notifications': Notification.objects.filter(
                recipient=user,
                is_read=False
            ).count(),
            'pending_friend_requests': Friendship.objects.filter(
                to_user=user,
                status='pending'
            ).count()
        }

        return Response(counts)

    except Exception as e:
        logger.error(f"获取未读数量失败: {str(e)}")
        return Response(
            {'error': '获取未读数量失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
