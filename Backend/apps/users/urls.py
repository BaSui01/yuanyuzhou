from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'users'

urlpatterns = [
    # 用户基本操作
    path('', views.UserListCreateView.as_view(), name='user-list-create'),
    path('<str:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # 当前用户相关
    path('me/profile/', views.CurrentUserView.as_view(), name='current-user'),
    path('me/settings/', views.UserProfileView.as_view(), name='user-profile'),
    path('me/password/', views.PasswordChangeView.as_view(), name='password-change'),
    path('me/stats/', views.UserStatsView.as_view(), name='user-stats'),
    path('me/login-logs/', views.UserLoginLogView.as_view(), name='user-login-logs'),
    path('me/update-activity/', views.update_last_active, name='update-last-active'),
    path('me/deactivate/', views.deactivate_account, name='deactivate-account'),

    # 用户搜索和社交
    path('search/', views.UserSearchView.as_view(), name='user-search'),
    path('me/followers/', views.UserFollowersView.as_view(), name='user-followers'),
    path('me/following/', views.UserFollowingView.as_view(), name='user-following'),
]
