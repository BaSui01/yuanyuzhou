from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Tag, Category, Attachment, Notification, SystemLog, Setting


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """标签管理"""
    list_display = ('name', 'color_display', 'usage_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('usage_count', 'created_at', 'updated_at')

    fieldsets = (
        (_('基本信息'), {
            'fields': ('name', 'slug', 'description')
        }),
        (_('显示设置'), {
            'fields': ('color', 'icon')
        }),
        (_('状态信息'), {
            'fields': ('usage_count', 'is_active'),
            'classes': ('collapse',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def color_display(self, obj):
        """显示颜色预览"""
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; display: inline-block; margin-right: 10px;"></div>{}',
            obj.color,
            obj.color
        )
    color_display.short_description = '颜色'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """分类管理"""
    list_display = ('name', 'parent', 'item_count', 'sort_order', 'is_active', 'created_at')
    list_filter = ('parent', 'is_active', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('item_count', 'created_at', 'updated_at')
    ordering = ['sort_order', 'name']

    fieldsets = (
        (_('基本信息'), {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        (_('显示设置'), {
            'fields': ('icon', 'sort_order')
        }),
        (_('状态信息'), {
            'fields': ('item_count', 'is_active'),
            'classes': ('collapse',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """附件管理"""
    list_display = ('name', 'file_type', 'file_size_display', 'uploaded_by', 'download_count', 'is_public', 'created_at')
    list_filter = ('file_type', 'is_public', 'is_active', 'created_at')
    search_fields = ('name', 'original_name', 'uploaded_by__username')
    readonly_fields = ('file_size', 'mime_type', 'download_count', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('文件信息'), {
            'fields': ('name', 'original_name', 'file', 'file_type')
        }),
        (_('技术信息'), {
            'fields': ('file_size', 'mime_type'),
            'classes': ('collapse',)
        }),
        (_('访问控制'), {
            'fields': ('uploaded_by', 'is_public', 'is_active')
        }),
        (_('统计信息'), {
            'fields': ('download_count',),
            'classes': ('collapse',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def file_size_display(self, obj):
        """显示友好的文件大小"""
        return obj.get_file_size_display()
    file_size_display.short_description = '文件大小'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """通知管理"""
    list_display = ('title', 'recipient', 'notification_type', 'is_read', 'sender', 'created_at')
    list_filter = ('notification_type', 'is_read', 'is_active', 'created_at')
    search_fields = ('title', 'message', 'recipient__username', 'sender__username')
    readonly_fields = ('read_at', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('通知内容'), {
            'fields': ('title', 'message', 'notification_type')
        }),
        (_('收发信息'), {
            'fields': ('recipient', 'sender')
        }),
        (_('操作设置'), {
            'fields': ('action_url', 'action_text')
        }),
        (_('状态信息'), {
            'fields': ('is_read', 'read_at', 'expires_at', 'is_active'),
            'classes': ('collapse',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        """批量标记为已读"""
        updated = queryset.filter(is_read=False).update(is_read=True)
        self.message_user(request, f'已标记 {updated} 条通知为已读。')
    mark_as_read.short_description = '标记为已读'

    def mark_as_unread(self, request, queryset):
        """批量标记为未读"""
        updated = queryset.filter(is_read=True).update(is_read=False, read_at=None)
        self.message_user(request, f'已标记 {updated} 条通知为未读。')
    mark_as_unread.short_description = '标记为未读'


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    """系统日志管理"""
    list_display = ('level', 'module', 'action', 'user', 'ip_address', 'created_at')
    list_filter = ('level', 'module', 'created_at')
    search_fields = ('module', 'action', 'message', 'user__username', 'ip_address')
    readonly_fields = ('level', 'module', 'action', 'message', 'user', 'ip_address', 'user_agent', 'extra_data', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('日志信息'), {
            'fields': ('level', 'module', 'action', 'message')
        }),
        (_('用户信息'), {
            'fields': ('user', 'ip_address')
        }),
        (_('设备信息'), {
            'fields': ('user_agent',),
            'classes': ('collapse',)
        }),
        (_('额外数据'), {
            'fields': ('extra_data',),
            'classes': ('collapse',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """禁止手动添加日志"""
        return False

    def has_change_permission(self, request, obj=None):
        """禁止修改日志"""
        return False


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """系统设置管理"""
    list_display = ('key', 'value_preview', 'value_type', 'group', 'is_public', 'is_editable', 'is_active')
    list_filter = ('value_type', 'group', 'is_public', 'is_editable', 'is_active')
    search_fields = ('key', 'value', 'description', 'group')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('设置信息'), {
            'fields': ('key', 'value', 'value_type', 'group')
        }),
        (_('设置描述'), {
            'fields': ('description',)
        }),
        (_('访问控制'), {
            'fields': ('is_public', 'is_editable', 'is_active')
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def value_preview(self, obj):
        """显示值预览"""
        if len(obj.value) > 50:
            return f"{obj.value[:50]}..."
        return obj.value
    value_preview.short_description = '设置值'

    def get_readonly_fields(self, request, obj=None):
        """根据是否可编辑设置只读字段"""
        readonly_fields = list(self.readonly_fields)
        if obj and not obj.is_editable:
            readonly_fields.extend(['key', 'value', 'value_type'])
        return readonly_fields
