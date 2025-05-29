from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User, UserProfile, UserLoginLog
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    UserListSerializer, UserSearchSerializer, UserProfileSerializer,
    PasswordChangeSerializer, UserLoginLogSerializer
)


class UserListCreateView(generics.ListCreateAPIView):
    """用户列表和创建视图"""
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['date_joined', 'last_active', 'username']
    ordering = ['-date_joined']
    filterset_fields = ['is_verified', 'is_premium', 'gender']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer

    def perform_create(self, serializer):
        """创建用户时的额外处理"""
        user = serializer.save()
        # 这里可以添加发送欢迎邮件等逻辑
        return user


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """用户详情视图"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        """获取用户对象，支持通过用户名或ID查询"""
        lookup_value = self.kwargs.get('pk')
        if lookup_value.isdigit():
            return generics.get_object_or_404(User, pk=lookup_value, is_active=True)
        else:
            return generics.get_object_or_404(User, username=lookup_value, is_active=True)

    def perform_update(self, serializer):
        """更新用户信息"""
        serializer.save(updated_at=timezone.now())


class CurrentUserView(APIView):
    """当前用户信息视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取当前用户信息"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """更新当前用户信息"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_at=timezone.now())
            # 返回完整的用户信息
            user_serializer = UserSerializer(request.user)
            return Response(user_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """用户档案视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取用户档案"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        """更新用户档案"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """密码修改视图"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """修改密码"""
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # 更新session，避免用户被登出
            update_session_auth_hash(request, request.user)
            return Response({'message': '密码修改成功'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(generics.ListAPIView):
    """用户搜索视图"""
    serializer_class = UserSearchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'bio']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username']

    def get_queryset(self):
        """获取搜索结果"""
        query = self.request.query_params.get('q', '')
        if not query:
            return User.objects.none()

        # 排除当前用户
        queryset = User.objects.filter(is_active=True).exclude(pk=self.request.user.pk)

        # 搜索条件
        search_conditions = Q()
        search_conditions |= Q(username__icontains=query)
        search_conditions |= Q(first_name__icontains=query)
        search_conditions |= Q(last_name__icontains=query)
        search_conditions |= Q(bio__icontains=query)

        return queryset.filter(search_conditions)[:20]  # 限制返回结果数量


class UserLoginLogView(generics.ListAPIView):
    """用户登录日志视图"""
    serializer_class = UserLoginLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_successful', 'device_type']
    ordering_fields = ['login_time']
    ordering = ['-login_time']

    def get_queryset(self):
        """获取当前用户的登录日志"""
        return UserLoginLog.objects.filter(user=self.request.user)


class UserStatsView(APIView):
    """用户统计视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取用户统计信息"""
        user = request.user
        profile = getattr(user, 'profile', None)

        # 统计登录信息
        login_logs = UserLoginLog.objects.filter(user=user)
        successful_logins = login_logs.filter(is_successful=True).count()
        failed_logins = login_logs.filter(is_successful=False).count()

        # 最近登录记录
        recent_logins = login_logs.filter(is_successful=True).order_by('-login_time')[:5]

        data = {
            'user_info': {
                'username': user.username,
                'date_joined': user.date_joined,
                'last_active': user.last_active,
                'is_verified': user.is_verified,
                'is_premium': user.is_premium,
            },
            'login_stats': {
                'total_logins': successful_logins,
                'failed_logins': failed_logins,
                'login_count': profile.login_count if profile else 0,
            },
            'profile_stats': {
                'points': profile.points if profile else 0,
                'level': profile.level if profile else 1,
            },
            'recent_logins': UserLoginLogSerializer(recent_logins, many=True).data
        }

        return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_last_active(request):
    """更新用户最后活跃时间"""
    request.user.last_active = timezone.now()
    request.user.save(update_fields=['last_active'])
    return Response({'message': '活跃时间已更新'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def deactivate_account(request):
    """停用账户"""
    password = request.data.get('password')
    if not password or not request.user.check_password(password):
        return Response(
            {'error': '密码验证失败'},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.user.is_active = False
    request.user.save(update_fields=['is_active'])

    return Response({'message': '账户已停用'})


class UserFollowersView(generics.ListAPIView):
    """用户关注者列表视图（预留接口）"""
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """获取关注者列表 - 需要在社交应用中实现"""
        # 这里返回空查询集，实际逻辑在social应用中实现
        return User.objects.none()


class UserFollowingView(generics.ListAPIView):
    """用户关注列表视图（预留接口）"""
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """获取关注列表 - 需要在社交应用中实现"""
        # 这里返回空查询集，实际逻辑在social应用中实现
        return User.objects.none()
