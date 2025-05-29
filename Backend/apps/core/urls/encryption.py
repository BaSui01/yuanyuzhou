"""
加密服务URL配置
"""

from django.urls import path
from ..views.encryption import (
    EncryptionSessionView,
    EncryptionStatsView,
    create_encryption_session,
    revoke_encryption_session,
    get_session_status,
    test_encryption,
    encryption_health_check
)

app_name = 'encryption'

urlpatterns = [
    # 传输层加密会话管理（类视图）
    path('session/create/', EncryptionSessionView.as_view(), name='session_create'),
    path('session/<str:session_id>/status/', EncryptionSessionView.as_view(), name='session_status'),
    path('session/<str:session_id>/revoke/', EncryptionSessionView.as_view(), name='session_revoke'),

    # API端点（函数视图）
    path('api/session/create/', create_encryption_session, name='api_session_create'),
    path('api/session/<str:session_id>/revoke/', revoke_encryption_session, name='api_session_revoke'),
    path('api/session/<str:session_id>/status/', get_session_status, name='api_session_status'),

    # 测试和调试端点
    path('api/test/', test_encryption, name='api_test_encryption'),
    path('api/health/', encryption_health_check, name='api_health_check'),

    # 统计信息
    path('stats/', EncryptionStatsView.as_view(), name='encryption_stats'),
]
