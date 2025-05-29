from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Count, Sum, Avg
from .models import (
    AIModel, AIRequest, ChatConversation, ChatMessage,
    AITemplate, AIUsageStats
)


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    """AI模型管理"""
    list_display = ('name', 'model_type', 'version', 'status', 'is_available', 'cost_per_request', 'created_at')
    list_filter = ('model_type', 'status', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'version')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['model_type', 'name']

    fieldsets = (
        (_('基本信息'), {
            'fields': ('name', 'model_type', 'description', 'version')
        }),
        (_('API配置'), {
            'fields': ('api_endpoint', 'api_key', 'configuration')
        }),
        (_('状态设置'), {
            'fields': ('status', 'is_active')
        }),
        (_('性能配置'), {
            'fields': ('max_requests_per_minute', 'cost_per_request')
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def is_available(self, obj):
        """显示是否可用"""
        if obj.is_available():
            return format_html('<span style="color: green;">✓ 可用</span>')
        else:
            return format_html('<span style="color: red;">✗ 不可用</span>')
    is_available.short_description = '可用状态'
    is_available.admin_order_field = 'status'


@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    """AI请求管理"""
    list_display = ('id', 'user', 'ai_model', 'request_type', 'status', 'cost', 'processing_time', 'created_at')
    list_filter = ('status', 'request_type', 'ai_model', 'created_at')
    search_fields = ('user__username', 'ai_model__name', 'input_data', 'error_message')
    readonly_fields = ('user', 'input_data', 'output_data', 'processing_time', 'cost', 'error_message', 'metadata', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        (_('请求信息'), {
            'fields': ('user', 'ai_model', 'request_type', 'status')
        }),
        (_('输入数据'), {
            'fields': ('input_data',),
            'classes': ('collapse',)
        }),
        (_('输出数据'), {
            'fields': ('output_data',),
            'classes': ('collapse',)
        }),
        (_('性能信息'), {
            'fields': ('processing_time', 'cost')
        }),
        (_('错误信息'), {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        (_('元数据'), {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """禁止手动添加请求"""
        return False

    def has_change_permission(self, request, obj=None):
        """禁止修改请求"""
        return False


class ChatMessageInline(admin.TabularInline):
    """聊天消息内联"""
    model = ChatMessage
    extra = 0
    readonly_fields = ('role', 'content', 'tokens', 'cost', 'created_at')
    fields = ('role', 'content', 'tokens', 'cost', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    """聊天对话管理"""
    list_display = ('title', 'user', 'ai_model', 'message_count', 'total_tokens', 'total_cost', 'is_archived', 'created_at')
    list_filter = ('ai_model', 'is_archived', 'is_active', 'created_at')
    search_fields = ('title', 'user__username', 'ai_model__name', 'system_prompt')
    readonly_fields = ('total_tokens', 'total_cost', 'message_count', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ['-updated_at']
    inlines = [ChatMessageInline]

    fieldsets = (
        (_('对话信息'), {
            'fields': ('user', 'ai_model', 'title', 'system_prompt')
        }),
        (_('统计信息'), {
            'fields': ('total_tokens', 'total_cost', 'message_count')
        }),
        (_('状态设置'), {
            'fields': ('is_archived', 'is_active')
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def message_count(self, obj):
        """显示消息数量"""
        return obj.messages.count()
    message_count.short_description = '消息数量'

    def get_queryset(self, request):
        """优化查询"""
        return super().get_queryset(request).select_related('user', 'ai_model').prefetch_related('messages')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """聊天消息管理"""
    list_display = ('conversation_title', 'role', 'content_preview', 'tokens', 'cost', 'created_at')
    list_filter = ('role', 'conversation__ai_model', 'created_at')
    search_fields = ('conversation__title', 'content', 'conversation__user__username')
    readonly_fields = ('conversation', 'role', 'content', 'tokens', 'cost', 'metadata', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        (_('消息信息'), {
            'fields': ('conversation', 'role', 'content')
        }),
        (_('统计信息'), {
            'fields': ('tokens', 'cost')
        }),
        (_('元数据'), {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def conversation_title(self, obj):
        """显示对话标题"""
        return obj.conversation.title
    conversation_title.short_description = '对话标题'
    conversation_title.admin_order_field = 'conversation__title'

    def content_preview(self, obj):
        """显示内容预览"""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = '内容预览'

    def has_add_permission(self, request):
        """禁止手动添加消息"""
        return False

    def has_change_permission(self, request, obj=None):
        """禁止修改消息"""
        return False

    def get_queryset(self, request):
        """优化查询"""
        return super().get_queryset(request).select_related('conversation', 'conversation__user', 'conversation__ai_model')


@admin.register(AITemplate)
class AITemplateAdmin(admin.ModelAdmin):
    """AI模板管理"""
    list_display = ('name', 'template_type', 'ai_model', 'creator', 'is_public', 'usage_count', 'created_at')
    list_filter = ('template_type', 'ai_model', 'is_public', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'content', 'creator__username')
    readonly_fields = ('usage_count', 'created_at', 'updated_at')
    ordering = ['-usage_count', 'name']

    fieldsets = (
        (_('模板信息'), {
            'fields': ('name', 'template_type', 'description', 'ai_model')
        }),
        (_('模板内容'), {
            'fields': ('content', 'variables')
        }),
        (_('权限设置'), {
            'fields': ('creator', 'is_public', 'is_active')
        }),
        (_('统计信息'), {
            'fields': ('usage_count',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """优化查询"""
        return super().get_queryset(request).select_related('ai_model', 'creator')


@admin.register(AIUsageStats)
class AIUsageStatsAdmin(admin.ModelAdmin):
    """AI使用统计管理"""
    list_display = ('user', 'ai_model', 'date', 'request_count', 'token_count', 'total_cost', 'success_rate_display')
    list_filter = ('ai_model', 'date', 'created_at')
    search_fields = ('user__username', 'ai_model__name')
    readonly_fields = ('user', 'ai_model', 'date', 'request_count', 'token_count', 'total_cost', 'success_count', 'error_count', 'created_at', 'updated_at')
    date_hierarchy = 'date'
    ordering = ['-date', '-request_count']

    fieldsets = (
        (_('统计信息'), {
            'fields': ('user', 'ai_model', 'date')
        }),
        (_('使用数据'), {
            'fields': ('request_count', 'token_count', 'total_cost')
        }),
        (_('成功失败'), {
            'fields': ('success_count', 'error_count')
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def success_rate_display(self, obj):
        """显示成功率"""
        if obj.request_count == 0:
            return '0%'
        rate = (obj.success_count / obj.request_count) * 100
        color = 'green' if rate >= 95 else 'orange' if rate >= 85 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    success_rate_display.short_description = '成功率'

    def has_add_permission(self, request):
        """禁止手动添加统计"""
        return False

    def has_change_permission(self, request, obj=None):
        """禁止修改统计"""
        return False

    def get_queryset(self, request):
        """优化查询"""
        return super().get_queryset(request).select_related('user', 'ai_model')


# 自定义管理界面标题
admin.site.site_header = 'AI功能管理'
admin.site.site_title = 'AI管理'
admin.site.index_title = 'AI功能管理后台'
