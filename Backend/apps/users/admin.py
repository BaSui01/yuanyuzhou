from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, UserLoginLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = (
        'username', 'email', 'phone', 'first_name', 'last_name',
        'is_verified', 'is_premium', 'is_active', 'is_staff', 'date_joined'
    )
    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 'is_verified', 'is_premium',
        'gender', 'date_joined', 'last_login'
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('个人信息'), {
            'fields': (
                'first_name', 'last_name', 'email', 'phone',
                'avatar', 'birth_date', 'gender', 'bio'
            )
        }),
        (_('地址信息'), {
            'fields': ('country', 'city'),
            'classes': ('collapse',)
        }),
        (_('社交媒体'), {
            'fields': ('website', 'github'),
            'classes': ('collapse',)
        }),
        (_('权限'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_verified', 'is_premium', 'groups', 'user_permissions'
            )
        }),
        (_('重要日期'), {
            'fields': ('last_login', 'date_joined', 'last_active')
        }),
        (_('设置'), {
            'fields': ('privacy_setting',),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login', 'created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户档案管理"""
    list_display = (
        'user', 'language', 'timezone', 'theme',
        'login_count', 'points', 'level', 'created_at'
    )
    list_filter = ('language', 'timezone', 'theme', 'level')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('基本信息'), {
            'fields': ('user',)
        }),
        (_('偏好设置'), {
            'fields': ('language', 'timezone', 'theme')
        }),
        (_('通知设置'), {
            'fields': (
                'email_notifications', 'sms_notifications', 'push_notifications'
            )
        }),
        (_('统计信息'), {
            'fields': ('login_count', 'points', 'level')
        }),
        (_('时间信息'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserLoginLog)
class UserLoginLogAdmin(admin.ModelAdmin):
    """登录日志管理"""
    list_display = (
        'user', 'ip_address', 'device_type', 'location',
        'is_successful', 'login_time'
    )
    list_filter = ('is_successful', 'device_type', 'login_time')
    search_fields = ('user__username', 'user__email', 'ip_address', 'location')
    readonly_fields = ('login_time',)
    date_hierarchy = 'login_time'

    fieldsets = (
        (_('用户信息'), {
            'fields': ('user',)
        }),
        (_('登录信息'), {
            'fields': (
                'ip_address', 'user_agent', 'location',
                'device_type', 'is_successful', 'login_time'
            )
        }),
    )

    def has_add_permission(self, request):
        """禁止手动添加登录日志"""
        return False

    def has_change_permission(self, request, obj=None):
        """禁止修改登录日志"""
        return False
