from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # 基本认证
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('status/', views.AuthStatusView.as_view(), name='auth-status'),

    # 邮箱验证
    path('verify-email/', views.EmailVerificationView.as_view(), name='verify-email'),
    path('resend-verification/', views.ResendVerificationView.as_view(), name='resend-verification'),

    # 密码重置
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # API密钥管理
    path('api-keys/', views.APIKeyListCreateView.as_view(), name='api-key-list-create'),
    path('api-keys/<int:pk>/', views.APIKeyDetailView.as_view(), name='api-key-detail'),

    # 账户管理
    path('change-email/', views.change_email, name='change-email'),
    path('deactivate-account/', views.deactivate_account, name='deactivate-account'),
]
