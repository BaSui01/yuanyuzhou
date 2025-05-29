from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.core.cache import cache
from apps.core.permissions import IsOwnerOrReadOnly
from apps.core.exceptions import ValidationError
from .models import (
    VirtualWorld, Avatar, UserSession, VirtualObject,
    WorldObject, Event, EventParticipant, WorldPermission
)
from .serializers import (
    VirtualWorldListSerializer, VirtualWorldSerializer,
    AvatarSerializer, UserSessionSerializer, VirtualObjectSerializer,
    WorldObjectSerializer, EventListSerializer, EventSerializer,
    WorldPermissionSerializer, EnterWorldSerializer, UpdatePositionSerializer,
    WorldStatsSerializer, UserActivityStatsSerializer
)
import uuid
import logging

logger = logging.getLogger(__name__)


class VirtualWorldListView(generics.ListCreateAPIView):
    """虚拟世界列表视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VirtualWorldSerializer
        return VirtualWorldListSerializer

    def get_queryset(self):
        queryset = VirtualWorld.objects.filter(is_active=True)

        # 过滤条件
        world_type = self.request.query_params.get('type')
        if world_type:
            queryset = queryset.filter(world_type=world_type)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        # 排序
        ordering = self.request.query_params.get('ordering', '-visit_count')
        return queryset.order_by(ordering).select_related('creator')


class VirtualWorldDetailView(generics.RetrieveUpdateDestroyAPIView):
    """虚拟世界详情视图"""
    queryset = VirtualWorld.objects.filter(is_active=True)
    serializer_class = VirtualWorldSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        # 检查访问权限
        if not obj.is_accessible_by(self.request.user):
            raise ValidationError("您没有权限访问此虚拟世界")
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 增加访问次数
        instance.increment_visit_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AvatarListView(generics.ListCreateAPIView):
    """虚拟形象列表视图"""
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.query_params.get('public') == 'true':
            return Avatar.objects.filter(is_public=True, is_active=True)
        return Avatar.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('-is_default', '-created_at')


class AvatarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """虚拟形象详情视图"""
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Avatar.objects.filter(user=self.request.user, is_active=True)


class VirtualObjectListView(generics.ListCreateAPIView):
    """虚拟物品列表视图"""
    serializer_class = VirtualObjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = VirtualObject.objects.filter(is_active=True)

        # 过滤条件
        object_type = self.request.query_params.get('type')
        if object_type:
            queryset = queryset.filter(object_type=object_type)

        if self.request.query_params.get('public_only') == 'true':
            queryset = queryset.filter(is_public=True)

        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        return queryset.order_by('-rating', '-download_count').select_related('creator')


class VirtualObjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """虚拟物品详情视图"""
    queryset = VirtualObject.objects.filter(is_active=True)
    serializer_class = VirtualObjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class EventListView(generics.ListCreateAPIView):
    """活动列表视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventSerializer
        return EventListSerializer

    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True)

        # 过滤条件
        event_type = self.request.query_params.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 只显示公开活动或用户参与的活动
        if self.request.query_params.get('my_events') == 'true':
            queryset = queryset.filter(
                Q(organizer=self.request.user) |
                Q(participants=self.request.user)
            ).distinct()
        else:
            queryset = queryset.filter(is_public=True)

        return queryset.order_by('start_time').select_related('organizer', 'world')


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """活动详情视图"""
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class WorldObjectListView(generics.ListCreateAPIView):
    """世界物品实例列表视图"""
    serializer_class = WorldObjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        world_id = self.kwargs.get('world_id')
        world = get_object_or_404(VirtualWorld, id=world_id, is_active=True)

        # 检查访问权限
        if not world.is_accessible_by(self.request.user):
            raise ValidationError("您没有权限访问此虚拟世界")

        return WorldObject.objects.filter(
            world=world,
            is_active=True
        ).select_related('virtual_object', 'placed_by')


class WorldObjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """世界物品实例详情视图"""
    queryset = WorldObject.objects.filter(is_active=True)
    serializer_class = WorldObjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        # 检查是否有编辑权限
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.placed_by != self.request.user:
                # 检查是否有世界管理权限
                has_permission = WorldPermission.objects.filter(
                    world=obj.world,
                    user=self.request.user,
                    permission_type__in=['edit', 'admin']
                ).exists()
                if not has_permission and obj.world.creator != self.request.user:
                    raise ValidationError("您没有权限编辑此物品")
        return obj


class UserSessionListView(generics.ListAPIView):
    """用户会话列表视图"""
    serializer_class = UserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('-last_seen').select_related('world', 'avatar')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enter_world(request, world_id):
    """进入虚拟世界"""
    try:
        world = get_object_or_404(VirtualWorld, id=world_id, is_active=True)

        # 检查访问权限
        if not world.is_accessible_by(request.user):
            return Response(
                {'error': '您没有权限访问此虚拟世界'},
                status=status.HTTP_403_FORBIDDEN
            )

        # 检查容量限制
        if world.current_users_count >= world.max_capacity:
            return Response(
                {'error': '虚拟世界已达到最大容量'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EnterWorldSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            avatar = get_object_or_404(
                Avatar,
                id=serializer.validated_data['avatar_id'],
                user=request.user,
                is_active=True
            )

            # 创建或更新会话
            session, created = UserSession.objects.get_or_create(
                user=request.user,
                world=world,
                defaults={
                    'avatar': avatar,
                    'session_id': str(uuid.uuid4()),
                    'status': 'active',
                    'position': serializer.validated_data.get('position', {}),
                    'device_info': serializer.validated_data.get('device_info', {})
                }
            )

            if not created:
                session.avatar = avatar
                session.status = 'active'
                session.position = serializer.validated_data.get('position', {})
                session.device_info = serializer.validated_data.get('device_info', {})
                session.save()

            logger.info(f"用户 {request.user.username} 进入世界 {world.name}")

            return Response({
                'session_id': session.session_id,
                'world': VirtualWorldSerializer(world).data,
                'avatar': AvatarSerializer(avatar).data,
                'message': '成功进入虚拟世界'
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"进入世界失败: {str(e)}")
        return Response(
            {'error': '进入世界失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def leave_world(request, world_id):
    """离开虚拟世界"""
    try:
        world = get_object_or_404(VirtualWorld, id=world_id, is_active=True)

        session = UserSession.objects.filter(
            user=request.user,
            world=world,
            is_active=True
        ).first()

        if session:
            session.disconnect()
            logger.info(f"用户 {request.user.username} 离开世界 {world.name}")
            return Response({'message': '成功离开虚拟世界'})

        return Response(
            {'error': '您当前不在此虚拟世界中'},
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        logger.error(f"离开世界失败: {str(e)}")
        return Response(
            {'error': '离开世界失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_position(request, world_id):
    """更新位置信息"""
    try:
        world = get_object_or_404(VirtualWorld, id=world_id, is_active=True)

        session = UserSession.objects.filter(
            user=request.user,
            world=world,
            is_active=True
        ).first()

        if not session:
            return Response(
                {'error': '您当前不在此虚拟世界中'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UpdatePositionSerializer(data=request.data)
        if serializer.is_valid():
            session.update_activity(
                position=serializer.validated_data['position']
            )
            return Response({'message': '位置更新成功'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"更新位置失败: {str(e)}")
        return Response(
            {'error': '更新位置失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def set_default_avatar(request, avatar_id):
    """设置默认虚拟形象"""
    try:
        avatar = get_object_or_404(
            Avatar,
            id=avatar_id,
            user=request.user,
            is_active=True
        )

        avatar.set_as_default()
        return Response({'message': '默认虚拟形象设置成功'})

    except Exception as e:
        logger.error(f"设置默认形象失败: {str(e)}")
        return Response(
            {'error': '设置默认形象失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def download_object(request, object_id):
    """下载虚拟物品"""
    try:
        virtual_object = get_object_or_404(
            VirtualObject,
            id=object_id,
            is_active=True
        )

        if not virtual_object.is_public and virtual_object.creator != request.user:
            return Response(
                {'error': '您没有权限下载此物品'},
                status=status.HTTP_403_FORBIDDEN
            )

        virtual_object.increment_download_count()

        return Response({
            'download_url': f'/media/objects/{virtual_object.id}/model.zip',
            'object': VirtualObjectSerializer(virtual_object).data,
            'message': '下载开始'
        })

    except Exception as e:
        logger.error(f"下载物品失败: {str(e)}")
        return Response(
            {'error': '下载物品失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_event(request, event_id):
    """参加活动"""
    try:
        event = get_object_or_404(Event, id=event_id, is_active=True)

        if not event.can_join(request.user):
            return Response(
                {'error': '无法参加此活动'},
                status=status.HTTP_400_BAD_REQUEST
            )

        participant, created = EventParticipant.objects.get_or_create(
            event=event,
            user=request.user,
            defaults={'status': 'registered'}
        )

        if created:
            return Response({'message': '成功参加活动'})
        else:
            return Response(
                {'error': '您已经参加了此活动'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        logger.error(f"参加活动失败: {str(e)}")
        return Response(
            {'error': '参加活动失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def leave_event(request, event_id):
    """离开活动"""
    try:
        event = get_object_or_404(Event, id=event_id, is_active=True)

        try:
            participant = EventParticipant.objects.get(
                event=event,
                user=request.user
            )
            participant.status = 'cancelled'
            participant.save()
            return Response({'message': '成功离开活动'})
        except EventParticipant.DoesNotExist:
            return Response(
                {'error': '您没有参加此活动'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        logger.error(f"离开活动失败: {str(e)}")
        return Response(
            {'error': '离开活动失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def active_sessions(request):
    """获取活跃会话"""
    try:
        sessions = UserSession.objects.filter(
            is_active=True,
            last_seen__gte=timezone.now() - timezone.timedelta(minutes=5)
        ).select_related('user', 'world', 'avatar')

        serializer = UserSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    except Exception as e:
        logger.error(f"获取活跃会话失败: {str(e)}")
        return Response(
            {'error': '获取活跃会话失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def world_stats(request):
    """获取世界统计信息"""
    try:
        stats = []
        worlds = VirtualWorld.objects.filter(is_active=True).annotate(
            unique_visitors=Count('user_sessions__user', distinct=True),
            avg_duration=Avg('user_sessions__duration')
        )

        for world in worlds:
            stats.append({
                'world_id': world.id,
                'world_name': world.name,
                'total_visits': world.visit_count,
                'unique_visitors': world.unique_visitors or 0,
                'current_users': world.current_users_count,
                'average_session_duration': world.avg_duration or 0.0,
                'peak_concurrent_users': world.max_capacity  # 简化处理
            })

        serializer = WorldStatsSerializer(stats, many=True)
        return Response(serializer.data)

    except Exception as e:
        logger.error(f"获取世界统计失败: {str(e)}")
        return Response(
            {'error': '获取世界统计失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_activity_stats(request):
    """获取用户活动统计"""
    try:
        user = request.user

        # 缓存键
        cache_key = f'user_activity_stats_{user.id}'
        cached_stats = cache.get(cache_key)
        if cached_stats:
            return Response(cached_stats)

        # 计算统计信息
        sessions = UserSession.objects.filter(user=user)
        total_time = sum(session.duration for session in sessions if session.duration)

        stats = {
            'total_time_spent': total_time,
            'worlds_visited': VirtualWorld.objects.filter(user_sessions__user=user).distinct().count(),
            'events_attended': EventParticipant.objects.filter(user=user, status='attended').count(),
            'objects_created': VirtualObject.objects.filter(creator=user).count(),
            'avatars_created': Avatar.objects.filter(user=user).count(),
            'favorite_world': '暂无数据',
            'most_used_avatar': '暂无数据'
        }

        # 获取最常访问的世界
        most_visited = sessions.values('world__name').annotate(
            visit_count=Count('id')
        ).order_by('-visit_count').first()
        if most_visited:
            stats['favorite_world'] = most_visited['world__name']

        # 获取最常使用的形象
        most_used = sessions.values('avatar__name').annotate(
            usage_count=Count('id')
        ).order_by('-usage_count').first()
        if most_used:
            stats['most_used_avatar'] = most_used['avatar__name']

        # 缓存结果
        cache.set(cache_key, stats, 300)  # 缓存5分钟

        serializer = UserActivityStatsSerializer(stats)
        return Response(serializer.data)

    except Exception as e:
        logger.error(f"获取用户活动统计失败: {str(e)}")
        return Response(
            {'error': '获取用户活动统计失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
