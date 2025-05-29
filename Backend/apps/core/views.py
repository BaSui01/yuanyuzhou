from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.conf import settings

from .models import Notification, SystemLog, Setting

User = get_user_model()


# 错误处理视图
def handler404(request, exception):
    """404错误处理"""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': '资源未找到',
            'status_code': 404,
            'path': request.path
        }, status=404)
    return render(request, '404.html', status=404)


def handler500(request):
    """500错误处理"""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': '服务器内部错误',
            'status_code': 500,
            'path': request.path
        }, status=500)
    return render(request, '500.html', status=500)


# API视图
class NotificationListView(generics.ListAPIView):
    """用户通知列表"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
            is_active=True
        ).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            notifications = []
            for notification in page:
                notifications.append({
                    'id': notification.id,
                    'title': notification.title,
                    'message': notification.message,
                    'type': notification.notification_type,
                    'is_read': notification.is_read,
                    'action_url': notification.action_url,
                    'action_text': notification.action_text,
                    'created_at': notification.created_at,
                    'is_expired': notification.is_expired(),
                })
            return self.get_paginated_response(notifications)

        # 非分页响应
        notifications = []
        for notification in queryset:
            notifications.append({
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'type': notification.notification_type,
                'is_read': notification.is_read,
                'action_url': notification.action_url,
                'action_text': notification.action_text,
                'created_at': notification.created_at,
                'is_expired': notification.is_expired(),
            })

        return Response(notifications)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """标记通知为已读"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user,
            is_active=True
        )
        notification.mark_as_read()
        return Response({'message': '通知已标记为已读'})
    except Notification.DoesNotExist:
        return Response(
            {'error': '通知不存在'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """标记所有通知为已读"""
    updated = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
        is_active=True
    ).update(is_read=True)

    return Response({
        'message': f'已标记 {updated} 条通知为已读'
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_notification(request, notification_id):
    """删除通知"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user,
            is_active=True
        )
        notification.is_active = False
        notification.save()
        return Response({'message': '通知已删除'})
    except Notification.DoesNotExist:
        return Response(
            {'error': '通知不存在'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_notification_count(request):
    """获取未读通知数量"""
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
        is_active=True
    ).count()

    return Response({'unread_count': count})


class SystemInfoView(APIView):
    """系统信息视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取系统信息"""
        # 缓存系统信息
        cache_key = 'system_info'
        system_info = cache.get(cache_key)

        if not system_info:
            system_info = {
                'app_name': getattr(settings, 'APP_NAME', '后端管理系统'),
                'app_version': getattr(settings, 'APP_VERSION', '1.0.0'),
                'api_version': getattr(settings, 'API_VERSION', 'v1'),
                'debug_mode': settings.DEBUG,
                'time_zone': settings.TIME_ZONE,
                'language_code': settings.LANGUAGE_CODE,
            }

            # 如果是管理员，显示更多信息
            if request.user.is_staff:
                import django
                system_info.update({
                    'django_version': django.get_version(),
                    'python_version': '.'.join(map(str, __import__('sys').version_info[:3])),
                    'total_users': User.objects.count(),
                    'active_users': User.objects.filter(is_active=True).count(),
                })

            # 缓存5分钟
            cache.set(cache_key, system_info, 300)

        return Response(system_info)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_settings(request):
    """获取公开设置"""
    cache_key = 'public_settings'
    public_settings = cache.get(cache_key)

    if not public_settings:
        settings_queryset = Setting.objects.filter(
            is_public=True,
            is_active=True
        )

        public_settings = {}
        for setting in settings_queryset:
            if setting.group not in public_settings:
                public_settings[setting.group] = {}
            public_settings[setting.group][setting.key] = setting.get_typed_value()

        # 缓存10分钟
        cache.set(cache_key, public_settings, 600)

    return Response(public_settings)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def update_setting(request):
    """更新系统设置"""
    key = request.data.get('key')
    value = request.data.get('value')
    value_type = request.data.get('value_type', 'string')
    description = request.data.get('description', '')
    group = request.data.get('group', 'general')

    if not key:
        return Response(
            {'error': '设置键不能为空'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        setting = Setting.set_setting(
            key=key,
            value=value,
            value_type=value_type,
            description=description,
            group=group
        )

        # 清除相关缓存
        cache.delete('public_settings')
        cache.delete('system_info')

        # 记录日志
        SystemLog.log(
            level='info',
            module='core',
            action='update_setting',
            message=f'设置 {key} 已更新',
            user=request.user,
            request=request,
            setting_key=key,
            old_value=getattr(setting, '_old_value', None),
            new_value=value
        )

        return Response({
            'message': '设置已更新',
            'setting': {
                'key': setting.key,
                'value': setting.get_typed_value(),
                'type': setting.value_type,
                'group': setting.group
            }
        })

    except Exception as e:
        return Response(
            {'error': f'更新设置失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def system_logs(request):
    """获取系统日志"""
    level = request.GET.get('level', '')
    module = request.GET.get('module', '')
    action = request.GET.get('action', '')

    logs = SystemLog.objects.all()

    if level:
        logs = logs.filter(level=level)
    if module:
        logs = logs.filter(module__icontains=module)
    if action:
        logs = logs.filter(action__icontains=action)

    logs = logs.order_by('-created_at')[:100]  # 限制返回100条

    log_data = []
    for log in logs:
        log_data.append({
            'id': log.id,
            'level': log.level,
            'module': log.module,
            'action': log.action,
            'message': log.message,
            'user': log.user.username if log.user else None,
            'ip_address': log.ip_address,
            'created_at': log.created_at,
        })

    return Response(log_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """健康检查端点"""
    try:
        # 检查数据库连接
        User.objects.count()

        # 检查缓存
        cache.set('health_check', 'ok', 10)
        cache_status = cache.get('health_check') == 'ok'

        return Response({
            'status': 'healthy',
            'timestamp': __import__('django.utils.timezone').timezone.now(),
            'services': {
                'database': 'ok',
                'cache': 'ok' if cache_status else 'error',
            }
        })

    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': __import__('django.utils.timezone').timezone.now(),
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
