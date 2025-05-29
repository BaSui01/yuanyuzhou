from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    VirtualWorld, Avatar, UserSession, VirtualObject,
    WorldObject, Event, EventParticipant, WorldPermission
)


@admin.register(VirtualWorld)
class VirtualWorldAdmin(admin.ModelAdmin):
    """虚拟世界管理"""
    list_display = [
        'name', 'world_type', 'creator', 'status', 'max_capacity',
        'visit_count', 'current_users_count', 'created_at'
    ]
    list_filter = ['world_type', 'status', 'created_at']
    search_fields = ['name', 'description', 'creator__username']
    readonly_fields = ['visit_count', 'current_users_count', 'created_at', 'updated_at']
    filter_horizontal = ['tags']

    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'world_type', 'creator')
        }),
        ('设置', {
            'fields': ('thumbnail', 'max_capacity', 'status', 'tags')
        }),
        ('场景数据', {
            'fields': ('scene_data', 'settings'),
            'classes': ('collapse',)
        }),
        ('统计信息', {
            'fields': ('visit_count', 'current_users_count'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('creator')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "creator":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    """虚拟形象管理"""
    list_display = [
        'name', 'user', 'avatar_type', 'is_default', 'is_public',
        'thumbnail_preview', 'created_at'
    ]
    list_filter = ['avatar_type', 'is_default', 'is_public', 'created_at']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'thumbnail_preview']

    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'name', 'avatar_type')
        }),
        ('外观数据', {
            'fields': ('model_data', 'appearance_data', 'animations'),
            'classes': ('collapse',)
        }),
        ('设置', {
            'fields': ('thumbnail', 'thumbnail_preview', 'is_default', 'is_public')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;">',
                obj.thumbnail.url
            )
        return "无缩略图"
    thumbnail_preview.short_description = "缩略图预览"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """用户会话管理"""
    list_display = [
        'user', 'world', 'avatar', 'status', 'duration_display',
        'last_seen', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'last_seen']
    search_fields = ['user__username', 'world__name', 'session_id']
    readonly_fields = ['session_id', 'duration', 'created_at', 'duration_display']

    fieldsets = (
        ('会话信息', {
            'fields': ('user', 'world', 'avatar', 'session_id', 'status')
        }),
        ('位置和设备', {
            'fields': ('position', 'device_info'),
            'classes': ('collapse',)
        }),
        ('时间统计', {
            'fields': ('duration', 'duration_display', 'last_seen', 'created_at')
        })
    )

    def duration_display(self, obj):
        if obj.duration:
            hours = obj.duration // 3600
            minutes = (obj.duration % 3600) // 60
            return f"{hours}小时{minutes}分钟"
        return "计算中"
    duration_display.short_description = "会话时长"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'world', 'avatar')


@admin.register(VirtualObject)
class VirtualObjectAdmin(admin.ModelAdmin):
    """虚拟物品管理"""
    list_display = [
        'name', 'object_type', 'creator', 'is_public', 'download_count',
        'rating', 'thumbnail_preview', 'created_at'
    ]
    list_filter = ['object_type', 'is_public', 'created_at']
    search_fields = ['name', 'description', 'creator__username']
    readonly_fields = ['download_count', 'rating', 'created_at', 'updated_at', 'thumbnail_preview']
    filter_horizontal = ['tags']

    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'object_type', 'creator')
        }),
        ('数据', {
            'fields': ('model_data', 'physics_data', 'interaction_data'),
            'classes': ('collapse',)
        }),
        ('设置', {
            'fields': ('thumbnail', 'thumbnail_preview', 'is_public', 'tags')
        }),
        ('统计信息', {
            'fields': ('download_count', 'rating'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;">',
                obj.thumbnail.url
            )
        return "无缩略图"
    thumbnail_preview.short_description = "缩略图预览"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('creator')


@admin.register(WorldObject)
class WorldObjectAdmin(admin.ModelAdmin):
    """世界物品实例管理"""
    list_display = [
        'virtual_object', 'world', 'placed_by', 'position_display', 'created_at'
    ]
    list_filter = ['created_at', 'world']
    search_fields = ['virtual_object__name', 'world__name', 'placed_by__username']
    readonly_fields = ['created_at', 'updated_at', 'position_display']

    fieldsets = (
        ('基本信息', {
            'fields': ('world', 'virtual_object', 'placed_by')
        }),
        ('变换数据', {
            'fields': ('position', 'position_display', 'rotation', 'scale')
        }),
        ('属性', {
            'fields': ('properties',),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def position_display(self, obj):
        if obj.position:
            return f"X: {obj.position.get('x', 0)}, Y: {obj.position.get('y', 0)}, Z: {obj.position.get('z', 0)}"
        return "未设置位置"
    position_display.short_description = "位置坐标"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('virtual_object', 'world', 'placed_by')


class EventParticipantInline(admin.TabularInline):
    """活动参与者内联"""
    model = EventParticipant
    extra = 0
    readonly_fields = ['registered_at', 'attended_at']
    fields = ['user', 'status', 'registered_at', 'attended_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """活动管理"""
    list_display = [
        'title', 'event_type', 'organizer', 'world', 'start_time',
        'end_time', 'status', 'participant_count', 'is_public'
    ]
    list_filter = ['event_type', 'status', 'is_public', 'start_time']
    search_fields = ['title', 'description', 'organizer__username', 'world__name']
    readonly_fields = ['created_at', 'updated_at', 'participant_count']
    filter_horizontal = ['tags']
    inlines = [EventParticipantInline]

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'event_type', 'organizer', 'world')
        }),
        ('时间设置', {
            'fields': ('start_time', 'end_time', 'status')
        }),
        ('参与设置', {
            'fields': ('max_participants', 'is_public', 'registration_required', 'tags')
        }),
        ('统计信息', {
            'fields': ('participant_count',),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = "参与人数"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('organizer', 'world')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organizer":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    """活动参与者管理"""
    list_display = ['event', 'user', 'status', 'registered_at', 'attended_at']
    list_filter = ['status', 'registered_at']
    search_fields = ['event__title', 'user__username']
    readonly_fields = ['registered_at', 'attended_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event', 'user')


@admin.register(WorldPermission)
class WorldPermissionAdmin(admin.ModelAdmin):
    """世界权限管理"""
    list_display = ['world', 'user', 'permission_type', 'granted_by', 'created_at']
    list_filter = ['permission_type', 'created_at']
    search_fields = ['world__name', 'user__username', 'granted_by__username']
    readonly_fields = ['created_at']

    fieldsets = (
        ('权限信息', {
            'fields': ('world', 'user', 'permission_type', 'granted_by')
        }),
        ('时间信息', {
            'fields': ('created_at',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('world', 'user', 'granted_by')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "granted_by":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 自定义管理界面标题
admin.site.site_header = "元宇宙管理系统"
admin.site.site_title = "元宇宙管理"
admin.site.index_title = "欢迎使用元宇宙管理系统"
