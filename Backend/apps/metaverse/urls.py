from django.urls import path
from . import views

app_name = 'metaverse'

urlpatterns = [
    # 虚拟世界相关
    path('worlds/', views.VirtualWorldListView.as_view(), name='world-list'),
    path('worlds/<int:pk>/', views.VirtualWorldDetailView.as_view(), name='world-detail'),
    path('worlds/<int:world_id>/enter/', views.enter_world, name='enter-world'),
    path('worlds/<int:world_id>/leave/', views.leave_world, name='leave-world'),
    path('worlds/<int:world_id>/update-position/', views.update_position, name='update-position'),

    # 虚拟形象相关
    path('avatars/', views.AvatarListView.as_view(), name='avatar-list'),
    path('avatars/<int:pk>/', views.AvatarDetailView.as_view(), name='avatar-detail'),
    path('avatars/<int:avatar_id>/set-default/', views.set_default_avatar, name='set-default-avatar'),

    # 虚拟物品相关
    path('objects/', views.VirtualObjectListView.as_view(), name='object-list'),
    path('objects/<int:pk>/', views.VirtualObjectDetailView.as_view(), name='object-detail'),
    path('objects/<int:object_id>/download/', views.download_object, name='download-object'),

    # 活动相关
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('events/<int:event_id>/join/', views.join_event, name='join-event'),
    path('events/<int:event_id>/leave/', views.leave_event, name='leave-event'),

    # 会话相关
    path('sessions/', views.UserSessionListView.as_view(), name='session-list'),
    path('sessions/active/', views.active_sessions, name='active-sessions'),

    # 世界对象相关
    path('worlds/<int:world_id>/objects/', views.WorldObjectListView.as_view(), name='world-object-list'),
    path('world-objects/<int:pk>/', views.WorldObjectDetailView.as_view(), name='world-object-detail'),

    # 统计和分析
    path('stats/worlds/', views.world_stats, name='world-stats'),
    path('stats/users/', views.user_activity_stats, name='user-activity-stats'),
]
