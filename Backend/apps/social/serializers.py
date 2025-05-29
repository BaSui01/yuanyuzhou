from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Friendship, Group, GroupMembership, Post, PostLike, Comment, CommentLike,
    Message, Conversation, Follow, Notification, PostShare
)

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    """用户简单序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']


class FriendshipSerializer(serializers.ModelSerializer):
    """好友关系序列化器"""
    from_user_info = UserSimpleSerializer(source='from_user', read_only=True)
    to_user_info = UserSimpleSerializer(source='to_user', read_only=True)

    class Meta:
        model = Friendship
        fields = [
            'id', 'from_user', 'to_user', 'from_user_info', 'to_user_info',
            'status', 'created_at', 'accepted_at'
        ]
        read_only_fields = ['from_user', 'created_at', 'accepted_at']

    def create(self, validated_data):
        validated_data['from_user'] = self.context['request'].user
        return super().create(validated_data)


class GroupMembershipSerializer(serializers.ModelSerializer):
    """群组成员序列化器"""
    user_info = UserSimpleSerializer(source='user', read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'user_info', 'role', 'joined_at']
        read_only_fields = ['joined_at']


class GroupListSerializer(serializers.ModelSerializer):
    """群组列表序列化器"""
    creator_info = UserSimpleSerializer(source='creator', read_only=True)

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'description', 'group_type', 'creator', 'creator_info',
            'avatar', 'member_count', 'max_members', 'created_at'
        ]
        read_only_fields = ['creator', 'member_count', 'created_at']


class GroupSerializer(serializers.ModelSerializer):
    """群组详情序列化器"""
    creator_info = UserSimpleSerializer(source='creator', read_only=True)
    members = GroupMembershipSerializer(source='memberships', many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    can_join = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'description', 'group_type', 'creator', 'creator_info',
            'avatar', 'members', 'member_count', 'max_members', 'tags',
            'can_join', 'created_at', 'updated_at'
        ]
        read_only_fields = ['creator', 'member_count', 'created_at', 'updated_at']

    def get_can_join(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.can_join(request.user)
        return False

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """动态列表序列化器"""
    author_info = UserSimpleSerializer(source='author', read_only=True)
    group_info = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_info', 'content', 'post_type', 'visibility',
            'group', 'group_info', 'like_count', 'comment_count', 'share_count',
            'is_pinned', 'is_liked', 'created_at'
        ]
        read_only_fields = ['author', 'like_count', 'comment_count', 'share_count', 'created_at']

    def get_group_info(self, obj):
        if obj.group:
            return {'id': obj.group.id, 'name': obj.group.name}
        return None

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=request.user).exists()
        return False


class PostSerializer(serializers.ModelSerializer):
    """动态详情序列化器"""
    author_info = UserSimpleSerializer(source='author', read_only=True)
    group_info = serializers.SerializerMethodField()
    attachments = serializers.StringRelatedField(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_info', 'content', 'post_type', 'visibility',
            'group', 'group_info', 'attachments', 'tags', 'like_count',
            'comment_count', 'share_count', 'is_pinned', 'is_liked',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'author', 'like_count', 'comment_count', 'share_count',
            'created_at', 'updated_at'
        ]

    def get_group_info(self, obj):
        if obj.group:
            return {'id': obj.group.id, 'name': obj.group.name}
        return None

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=request.user).exists()
        return False

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    author_info = UserSimpleSerializer(source='author', read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'author_info', 'content', 'parent',
            'like_count', 'reply_count', 'replies', 'is_liked',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'author', 'like_count', 'reply_count',
            'created_at', 'updated_at'
        ]

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(
                obj.replies.filter(is_active=True)[:3],
                many=True,
                context=self.context
            ).data
        return []

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommentLike.objects.filter(comment=obj, user=request.user).exists()
        return False

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    """消息序列化器"""
    sender_info = UserSimpleSerializer(source='sender', read_only=True)
    attachment = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'sender_info', 'content',
            'message_type', 'attachment', 'is_read', 'read_at', 'created_at'
        ]
        read_only_fields = ['sender', 'is_read', 'read_at', 'created_at']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """对话序列化器"""
    participants = UserSimpleSerializer(many=True, read_only=True)
    last_message = MessageSerializer(read_only=True)
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'participants', 'conversation_type', 'title',
            'last_message', 'last_message_at', 'unread_count', 'created_at'
        ]
        read_only_fields = ['last_message', 'last_message_at', 'created_at']

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(
                is_read=False,
                sender__ne=request.user
            ).count()
        return 0


class FollowSerializer(serializers.ModelSerializer):
    """关注关系序列化器"""
    follower_info = UserSimpleSerializer(source='follower', read_only=True)
    followed_info = UserSimpleSerializer(source='followed', read_only=True)

    class Meta:
        model = Follow
        fields = [
            'id', 'follower', 'followed', 'follower_info', 'followed_info',
            'created_at'
        ]
        read_only_fields = ['follower', 'created_at']

    def create(self, validated_data):
        validated_data['follower'] = self.context['request'].user
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    """通知序列化器"""
    sender_info = UserSimpleSerializer(source='sender', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'sender', 'sender_info', 'notification_type',
            'title', 'content', 'is_read', 'read_at', 'related_object_id',
            'related_object_type', 'created_at'
        ]
        read_only_fields = [
            'recipient', 'sender', 'is_read', 'read_at', 'created_at'
        ]


class PostShareSerializer(serializers.ModelSerializer):
    """动态分享序列化器"""
    user_info = UserSimpleSerializer(source='user', read_only=True)
    post_info = PostListSerializer(source='post', read_only=True)

    class Meta:
        model = PostShare
        fields = [
            'id', 'post', 'user', 'user_info', 'post_info',
            'content', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SendFriendRequestSerializer(serializers.Serializer):
    """发送好友请求序列化器"""
    to_user_id = serializers.IntegerField()

    def validate_to_user_id(self, value):
        try:
            user = User.objects.get(id=value)
            request_user = self.context['request'].user

            if user == request_user:
                raise serializers.ValidationError("不能向自己发送好友请求")

            # 检查是否已经是好友
            if Friendship.are_friends(request_user, user):
                raise serializers.ValidationError("你们已经是好友了")

            # 检查是否已经发送过请求
            if Friendship.objects.filter(
                from_user=request_user,
                to_user=user,
                status='pending'
            ).exists():
                raise serializers.ValidationError("已经发送过好友请求")

            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("用户不存在")


class JoinGroupSerializer(serializers.Serializer):
    """加入群组序列化器"""
    group_id = serializers.IntegerField()

    def validate_group_id(self, value):
        try:
            group = Group.objects.get(id=value, is_active=True)
            user = self.context['request'].user

            if not group.can_join(user):
                raise serializers.ValidationError("无法加入该群组")

            return value
        except Group.DoesNotExist:
            raise serializers.ValidationError("群组不存在")


class SendMessageSerializer(serializers.Serializer):
    """发送消息序列化器"""
    conversation_id = serializers.IntegerField(required=False)
    recipient_id = serializers.IntegerField(required=False)
    content = serializers.CharField(max_length=5000)
    message_type = serializers.ChoiceField(
        choices=Message.MESSAGE_TYPES,
        default='text'
    )

    def validate(self, data):
        if not data.get('conversation_id') and not data.get('recipient_id'):
            raise serializers.ValidationError("必须指定对话ID或接收者ID")

        if data.get('conversation_id') and data.get('recipient_id'):
            raise serializers.ValidationError("不能同时指定对话ID和接收者ID")

        return data

    def validate_conversation_id(self, value):
        if value:
            try:
                conversation = Conversation.objects.get(id=value)
                user = self.context['request'].user

                if not conversation.participants.filter(id=user.id).exists():
                    raise serializers.ValidationError("您不是该对话的参与者")

                return value
            except Conversation.DoesNotExist:
                raise serializers.ValidationError("对话不存在")

    def validate_recipient_id(self, value):
        if value:
            try:
                recipient = User.objects.get(id=value)
                sender = self.context['request'].user

                if recipient == sender:
                    raise serializers.ValidationError("不能向自己发送消息")

                return value
            except User.DoesNotExist:
                raise serializers.ValidationError("接收者不存在")


class UserSocialStatsSerializer(serializers.Serializer):
    """用户社交统计序列化器"""
    posts_count = serializers.IntegerField()
    friends_count = serializers.IntegerField()
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    groups_count = serializers.IntegerField()
    total_likes_received = serializers.IntegerField()
    total_comments_received = serializers.IntegerField()
    most_liked_post = serializers.CharField()
    most_active_group = serializers.CharField()
