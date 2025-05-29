from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    # AI模型相关
    path('models/', views.AIModelListView.as_view(), name='model-list'),
    path('models/available/', views.available_models, name='available-models'),

    # AI请求相关
    path('requests/', views.AIRequestListView.as_view(), name='request-list'),
    path('requests/<int:pk>/', views.AIRequestDetailView.as_view(), name='request-detail'),

    # 聊天对话相关
    path('conversations/', views.ChatConversationListView.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/', views.ChatConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<int:conversation_id>/archive/', views.archive_conversation, name='archive-conversation'),
    path('chat/send/', views.send_message, name='send-message'),

    # AI模板相关
    path('templates/', views.AITemplateListView.as_view(), name='template-list'),
    path('templates/<int:pk>/', views.AITemplateDetailView.as_view(), name='template-detail'),
    path('templates/render/', views.render_template, name='render-template'),

    # 统计相关
    path('stats/user/', views.UserUsageStatsView.as_view(), name='user-stats'),
    path('stats/models/', views.ModelUsageStatsView.as_view(), name='model-stats'),

    # OpenAI兼容接口
    path('chat/completions/', views.chat_completion, name='chat-completion'),
]
