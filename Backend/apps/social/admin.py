from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Friendship, Group, GroupMembership, Post, PostLike, Comment, CommentLike,
    Message, Conversation, Follow, Notification, PostShare
)


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    """好友关系管理"""
    list_display = [
        'from_user', 'to_user', 'status', 'created_at', 'accepted_at'
    ]
    list_filter = ['status', 'created_at', 'accepted_at']
    search_fields = ['from_user__username', 'to_user__username']
    readonly_fields = ['created_at', 'accepted_at']

    fieldsets = (
        ('好友关系', {
            'fields': ('from_user', 'to_user', 'status')
        }),
        ('时间信息', {
            'fields': ('created_at', 'accepted_at'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('from_user', 'to_user')


class GroupMembershipInline(admin.TabularInline):
    """群组成员内联"""
    model = GroupMembership
    extra = 0
    readonly_fields = ['joined_at']
    fields = ['user', 'role', 'joined_at']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """群组管理"""
    list_display = [
        'name', 'group_type', 'creator', 'member_count', 'max_members',
        'avatar_preview', 'created_at'
    ]
    list_filter = ['group_type', 'created_at']
    search_fields = ['name', 'description', 'creator__username']
    readonly_fields = ['member_count', 'created_at', 'updated_at', 'avatar_preview']
    filter_horizontal = ['tags']
    inlines = [GroupMembershipInline]

    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'group_type', 'creator')
        }),
        ('设置', {
            'fields': ('avatar', 'avatar_preview', 'max_members', 'tags')
        }),
        ('统计信息', {
            'fields': ('member_count',),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;">',
                obj.avatar.url
            )
        return "无头像"
    avatar_preview.short_description = "头像预览"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('creator')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "creator":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    """群组成员管理"""
    list_display = ['group', 'user', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['group__name', 'user__username']
    readonly_fields = ['joined_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('group', 'user')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """动态管理"""
    list_display = [
        'content_preview', 'author', 'post_type', 'visibility',
        'group', 'like_count', 'comment_count', 'is_pinned', 'created_at'
    ]
    list_filter = ['post_type', 'visibility', 'is_pinned', 'created_at']
    search_fields = ['content', 'author__username', 'group__name']
    readonly_fields = ['like_count', 'comment_count', 'share_count', 'created_at', 'updated_at']
    filter_horizontal = ['attachments', 'tags']

    fieldsets = (
        ('动态内容', {
            'fields': ('author', 'content', 'post_type', 'visibility')
        }),
        ('关联信息', {
            'fields': ('group', 'attachments', 'tags')
        }),
        ('设置', {
            'fields': ('is_pinned',)
        }),
        ('统计信息', {
            'fields': ('like_count', 'comment_count', 'share_count'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "内容预览"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'group')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    """动态点赞管理"""
    list_display = ['post_preview', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__content', 'user__username']
    readonly_fields = ['created_at']

    def post_preview(self, obj):
        content = obj.post.content[:30]
        return f"{content}..." if len(obj.post.content) > 30 else content
    post_preview.short_description = "动态预览"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post', 'user')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """评论管理"""
    list_display = [
        'content_preview', 'author', 'post_preview', 'parent',
        'like_count', 'reply_count', 'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['content', 'author__username', 'post__content']
    readonly_fields = ['like_count', 'reply_count', 'created_at', 'updated_at']

    fieldsets = (
        ('评论内容', {
            'fields': ('post', 'author', 'content', 'parent')
        }),
        ('统计信息', {
            'fields': ('like_count', 'reply_count'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "评论预览"

    def post_preview(self, obj):
        content = obj.post.content[:30]
        return f"{content}..." if len(obj.post.content) > 30 else content
    post_preview.short_description = "动态预览"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post', 'parent')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    """评论点赞管理"""
    list_display = ['comment_preview', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['comment__content', 'user__username']
    readonly_fields = ['created_at']

    def comment_preview(self, obj):
        content = obj.comment.content[:30]
        return f"{content}..." if len(obj.comment.content) > 30 else content
    comment_preview.short_description = "评论预览"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('comment', 'user')


class MessageInline(admin.TabularInline):
    """消息内联"""
    model = Message
    extra = 0
    readonly_fields = ['sender', 'created_at', 'is_read', 'read_at']
    fields = ['sender', 'content', 'message_type', 'is_read', 'created_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """对话管理"""
    list_display = [
        'title_display', 'conversation_type', 'participant_count',
        'last_message_at', 'created_at'
    ]
    list_filter = ['conversation_type', 'created_at', 'last_message_at']
    search_fields = ['title', 'participants__username']
    readonly_fields = ['last_message', 'last_message_at', 'created_at', 'participant_count']
    filter_horizontal = ['participants']
    inlines = [MessageInline]

    fieldsets = (
        ('对话信息', {
            'fields': ('conversation_type', 'title', 'participants')
        }),
        ('最后消息', {
            'fields': ('last_message', 'last_message_at'),
            'classes': ('collapse',)
        }),
        ('统计信息', {
            'fields': ('participant_count',),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def title_display(self, obj):
        if obj.title:
            return obj.title
        participants = list(obj.participants.all()[:2])
        if len(participants) == 2:
            return f"{participants[0].username} & {participants[1].username}"
        return f"对话 {obj.id}"
    title_display.short_description = "对话标题"

    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = "参与者数量"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('participants')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """消息管理"""
    list_display = [
        'content_preview', 'sender', 'conversation_display',
        'message_type', 'is_read', 'created_at'
    ]
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['content', 'sender__username']
    readonly_fields = ['created_at', 'read_at']

    fieldsets = (
        ('消息内容', {
            'fields': ('conversation', 'sender', 'content', 'message_type')
        }),
        ('附件', {
            'fields': ('attachment',),
            'classes': ('collapse',)
        }),
        ('状态', {
            'fields': ('is_read', 'read_at')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "消息预览"

    def conversation_display(self, obj):
        return str(obj.conversation)
    conversation_display.short_description = "对话"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'conversation')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sender":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """关注关系管理"""
    list_display = ['follower', 'followed', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'followed__username']
    readonly_fields = ['created_at']

    fieldsets = (
        ('关注关系', {
            'fields': ('follower', 'followed')
        }),
        ('时间信息', {
            'fields': ('created_at',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('follower', 'followed')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """通知管理"""
    list_display = [
        'title', 'recipient', 'sender', 'notification_type',
        'is_read', 'created_at'
    ]
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'content', 'recipient__username', 'sender__username']
    readonly_fields = ['created_at', 'read_at']

    fieldsets = (
        ('通知内容', {
            'fields': ('recipient', 'sender', 'notification_type', 'title', 'content')
        }),
        ('关联对象', {
            'fields': ('related_object_id', 'related_object_type'),
            'classes': ('collapse',)
        }),
        ('状态', {
            'fields': ('is_read', 'read_at')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'sender')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sender":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PostShare)
class PostShareAdmin(admin.ModelAdmin):
    """动态分享管理"""
    list_display = [
        'post_preview', 'user', 'content_preview', 'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['post__content', 'user__username', 'content']
    readonly_fields = ['created_at']

    fieldsets = (
        ('分享信息', {
            'fields': ('post', 'user', 'content')
        }),
        ('时间信息', {
            'fields': ('created_at',)
        })
    )

    def post_preview(self, obj):
        content = obj.post.content[:30]
        return f"{content}..." if len(obj.post.content) > 30 else content
    post_preview.short_description = "原动态预览"

    def content_preview(self, obj):
        if obj.content:
            return obj.content[:30] + "..." if len(obj.content) > 30 else obj.content
        return "无分享内容"
    content_preview.short_description = "分享内容"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post', 'user')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 自定义管理界面标题
admin.site.site_header = "社交网络管理系统"
admin.site.site_title = "社交管理"
admin.site.index_title = "欢迎使用社交网络管理系统"
