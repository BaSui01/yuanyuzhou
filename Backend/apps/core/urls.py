from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # 通知相关
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark-all-notifications-read'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete-notification'),
    path('notifications/unread-count/', views.unread_notification_count, name='unread-notification-count'),

    # 系统信息
    path('system/info/', views.SystemInfoView.as_view(), name='system-info'),
    path('system/health/', views.health_check, name='health-check'),
    path('system/logs/', views.system_logs, name='system-logs'),

    # 设置管理
    path('settings/public/', views.public_settings, name='public-settings'),
    path('settings/update/', views.update_setting, name='update-setting'),
]
