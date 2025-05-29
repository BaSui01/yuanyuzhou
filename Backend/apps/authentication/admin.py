from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    EmailVerificationToken, PasswordResetToken,
    LoginAttempt, TwoFactorAuth, APIKey
)


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """邮箱验证令牌管理"""
    list_display = (
        'user', 'token_preview', 'created_at', 'expires_at',
        'is_used', 'is_expired'
    )
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'token')
    readonly_fields = ('token', 'created_at', 'expires_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('用户信息'), {
            'fields': ('user',)
        }),
        (_('令牌信息'), {
            'fields': ('token', 'is_used')
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )

    def token_preview(self, obj):
        """显示令牌预览"""
        return f"{obj.token[:10]}..." if obj.token else ""
    token_preview.short_description = '令牌预览'

    def is_expired(self, obj):
        """检查是否过期"""
        return not obj.is_valid()
    is_expired.boolean = True
    is_expired.short_description = '已过期'

    def has_add_permission(self, request):
        """禁止手动添加令牌"""
        return False

    def has_change_permission(self, request, obj=None):
        """只允许查看，不允许修改"""
        return False


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """密码重置令牌管理"""
    list_display = (
        'user', 'token_preview', 'ip_address', 'created_at',
        'expires_at', 'is_used', 'is_expired'
    )
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'token', 'ip_address')
    readonly_fields = ('token', 'created_at', 'expires_at', 'ip_address')
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('用户信息'), {
            'fields': ('user',)
        }),
        (_('令牌信息'), {
            'fields': ('token', 'is_used')
        }),
        (_('请求信息'), {
            'fields': ('ip_address',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )

    def token_preview(self, obj):
        """显示令牌预览"""
        return f"{obj.token[:10]}..." if obj.token else ""
    token_preview.short_description = '令牌预览'

    def is_expired(self, obj):
        """检查是否过期"""
        return not obj.is_valid()
    is_expired.boolean = True
    is_expired.short_description = '已过期'

    def has_add_permission(self, request):
        """禁止手动添加令牌"""
        return False

    def has_change_permission(self, request, obj=None):
        """只允许查看，不允许修改"""
        return False


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """登录尝试管理"""
    list_display = (
        'username', 'ip_address', 'device_info', 'is_successful',
        'failure_reason', 'created_at'
    )
    list_filter = ('is_successful', 'created_at')
    search_fields = ('username', 'ip_address', 'user_agent', 'failure_reason')
    readonly_fields = ('username', 'ip_address', 'user_agent', 'created_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('登录信息'), {
            'fields': ('username', 'is_successful', 'failure_reason')
        }),
        (_('设备信息'), {
            'fields': ('ip_address', 'user_agent')
        }),
        (_('时间信息'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def device_info(self, obj):
        """显示设备信息简述"""
        if obj.user_agent:
            if 'Mobile' in obj.user_agent:
                return '移动设备'
            elif 'Chrome' in obj.user_agent:
                return 'Chrome浏览器'
            elif 'Firefox' in obj.user_agent:
                return 'Firefox浏览器'
            elif 'Safari' in obj.user_agent:
                return 'Safari浏览器'
            else:
                return '其他设备'
        return '未知设备'
    device_info.short_description = '设备类型'

    def has_add_permission(self, request):
        """禁止手动添加登录尝试"""
        return False

    def has_change_permission(self, request, obj=None):
        """禁止修改登录尝试"""
        return False


@admin.register(TwoFactorAuth)
class TwoFactorAuthAdmin(admin.ModelAdmin):
    """双因子认证管理"""
    list_display = (
        'user', 'is_enabled', 'backup_codes_count', 'created_at', 'updated_at'
    )
    list_filter = ('is_enabled', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('secret_key', 'created_at', 'updated_at')

    fieldsets = (
        (_('用户信息'), {
            'fields': ('user',)
        }),
        (_('认证设置'), {
            'fields': ('is_enabled', 'secret_key')
        }),
        (_('备用代码'), {
            'fields': ('backup_codes',),
            'classes': ('collapse',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def backup_codes_count(self, obj):
        """显示备用代码数量"""
        return len(obj.backup_codes) if obj.backup_codes else 0
    backup_codes_count.short_description = '备用代码数量'

    def has_add_permission(self, request):
        """禁止手动添加双因子认证"""
        return False


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    """API密钥管理"""
    list_display = (
        'user', 'name', 'key_preview', 'is_active', 'permissions_count',
        'last_used', 'created_at', 'expires_at', 'is_expired'
    )
    list_filter = ('is_active', 'created_at', 'expires_at', 'last_used')
    search_fields = ('user__username', 'user__email', 'name', 'key')
    readonly_fields = ('key', 'created_at', 'last_used')
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('基本信息'), {
            'fields': ('user', 'name', 'is_active')
        }),
        (_('密钥信息'), {
            'fields': ('key',)
        }),
        (_('权限设置'), {
            'fields': ('permissions',)
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'last_used', 'expires_at'),
            'classes': ('collapse',)
        }),
    )

    def key_preview(self, obj):
        """显示密钥预览"""
        return f"{obj.key[:20]}..." if obj.key else ""
    key_preview.short_description = '密钥预览'

    def permissions_count(self, obj):
        """显示权限数量"""
        return len(obj.permissions) if obj.permissions else 0
    permissions_count.short_description = '权限数量'

    def is_expired(self, obj):
        """检查是否过期"""
        return not obj.is_valid()
    is_expired.boolean = True
    is_expired.short_description = '已过期'

    def has_add_permission(self, request):
        """禁止手动添加API密钥"""
        return False

    def has_change_permission(self, request, obj=None):
        """只允许修改状态和过期时间"""
        return True

    def get_readonly_fields(self, request, obj=None):
        """设置只读字段"""
        readonly_fields = list(self.readonly_fields)
        if obj:  # 编辑时
            readonly_fields.extend(['user', 'name', 'permissions'])
        return readonly_fields


# 自定义管理站点标题
admin.site.site_header = '后端管理系统'
admin.site.site_title = '认证管理'
admin.site.index_title = '认证模块管理'
