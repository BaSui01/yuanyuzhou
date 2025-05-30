# Generated by Django 5.2.1 on 2025-05-29 17:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                (
                    "content",
                    models.TextField(
                        validators=[django.core.validators.MinLengthValidator(1)],
                        verbose_name="评论内容",
                    ),
                ),
                (
                    "like_count",
                    models.PositiveIntegerField(default=0, verbose_name="点赞数"),
                ),
                (
                    "reply_count",
                    models.PositiveIntegerField(default=0, verbose_name="回复数"),
                ),
            ],
            options={
                "verbose_name": "评论",
                "verbose_name_plural": "评论",
                "db_table": "social_comments",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="CommentLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="点赞时间"),
                ),
            ],
            options={
                "verbose_name": "评论点赞",
                "verbose_name_plural": "评论点赞",
                "db_table": "social_comment_likes",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Conversation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                (
                    "conversation_type",
                    models.CharField(
                        choices=[("private", "私聊"), ("group", "群聊")],
                        default="private",
                        max_length=20,
                        verbose_name="对话类型",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="对话标题"
                    ),
                ),
                (
                    "last_message_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="最后消息时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "对话",
                "verbose_name_plural": "对话",
                "db_table": "social_conversations",
                "ordering": ["-last_message_at"],
            },
        ),
        migrations.CreateModel(
            name="Follow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="关注时间"),
                ),
            ],
            options={
                "verbose_name": "关注关系",
                "verbose_name_plural": "关注关系",
                "db_table": "social_follows",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Friendship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "待确认"),
                            ("accepted", "已接受"),
                            ("blocked", "已屏蔽"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="状态",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "accepted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="接受时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "好友关系",
                "verbose_name_plural": "好友关系",
                "db_table": "social_friendships",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                ("name", models.CharField(max_length=100, verbose_name="群组名称")),
                ("description", models.TextField(blank=True, verbose_name="群组描述")),
                (
                    "group_type",
                    models.CharField(
                        choices=[
                            ("public", "公开群组"),
                            ("private", "私密群组"),
                            ("secret", "秘密群组"),
                        ],
                        default="public",
                        max_length=20,
                        verbose_name="群组类型",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="groups/avatars/",
                        verbose_name="群组头像",
                    ),
                ),
                (
                    "member_count",
                    models.PositiveIntegerField(default=0, verbose_name="成员数量"),
                ),
                (
                    "max_members",
                    models.PositiveIntegerField(default=500, verbose_name="最大成员数"),
                ),
            ],
            options={
                "verbose_name": "群组",
                "verbose_name_plural": "群组",
                "db_table": "social_groups",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="GroupMembership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("owner", "群主"),
                            ("admin", "管理员"),
                            ("member", "成员"),
                        ],
                        default="member",
                        max_length=20,
                        verbose_name="角色",
                    ),
                ),
                (
                    "joined_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="加入时间"),
                ),
            ],
            options={
                "verbose_name": "群组成员",
                "verbose_name_plural": "群组成员",
                "db_table": "social_group_memberships",
                "ordering": ["role", "-joined_at"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                ("content", models.TextField(verbose_name="消息内容")),
                (
                    "message_type",
                    models.CharField(
                        choices=[
                            ("text", "文本"),
                            ("image", "图片"),
                            ("file", "文件"),
                            ("system", "系统消息"),
                        ],
                        default="text",
                        max_length=20,
                        verbose_name="消息类型",
                    ),
                ),
                ("is_read", models.BooleanField(default=False, verbose_name="已读")),
                (
                    "read_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="阅读时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "私信",
                "verbose_name_plural": "私信",
                "db_table": "social_messages",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("like", "点赞"),
                            ("comment", "评论"),
                            ("follow", "关注"),
                            ("friend_request", "好友请求"),
                            ("group_invite", "群组邀请"),
                            ("message", "私信"),
                            ("system", "系统通知"),
                        ],
                        max_length=20,
                        verbose_name="通知类型",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="标题")),
                ("content", models.TextField(verbose_name="内容")),
                ("is_read", models.BooleanField(default=False, verbose_name="已读")),
                (
                    "read_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="阅读时间"
                    ),
                ),
                (
                    "related_object_id",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="关联对象ID"
                    ),
                ),
                (
                    "related_object_type",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="关联对象类型"
                    ),
                ),
            ],
            options={
                "verbose_name": "通知",
                "verbose_name_plural": "通知",
                "db_table": "social_notifications",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                ("content", models.TextField(verbose_name="内容")),
                (
                    "post_type",
                    models.CharField(
                        choices=[
                            ("text", "文本"),
                            ("image", "图片"),
                            ("video", "视频"),
                            ("link", "链接"),
                            ("poll", "投票"),
                        ],
                        default="text",
                        max_length=20,
                        verbose_name="动态类型",
                    ),
                ),
                (
                    "visibility",
                    models.CharField(
                        choices=[
                            ("public", "公开"),
                            ("friends", "仅好友"),
                            ("private", "仅自己"),
                        ],
                        default="public",
                        max_length=20,
                        verbose_name="可见性",
                    ),
                ),
                (
                    "like_count",
                    models.PositiveIntegerField(default=0, verbose_name="点赞数"),
                ),
                (
                    "comment_count",
                    models.PositiveIntegerField(default=0, verbose_name="评论数"),
                ),
                (
                    "share_count",
                    models.PositiveIntegerField(default=0, verbose_name="分享数"),
                ),
                ("is_pinned", models.BooleanField(default=False, verbose_name="置顶")),
            ],
            options={
                "verbose_name": "动态",
                "verbose_name_plural": "动态",
                "db_table": "social_posts",
                "ordering": ["-is_pinned", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PostLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="点赞时间"),
                ),
            ],
            options={
                "verbose_name": "动态点赞",
                "verbose_name_plural": "动态点赞",
                "db_table": "social_post_likes",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PostShare",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="激活状态"),
                ),
                ("content", models.TextField(blank=True, verbose_name="分享内容")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="分享时间"),
                ),
            ],
            options={
                "verbose_name": "动态分享",
                "verbose_name_plural": "动态分享",
                "db_table": "social_post_shares",
                "ordering": ["-created_at"],
            },
        ),
    ]
