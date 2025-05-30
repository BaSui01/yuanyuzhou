# Generated by Django 5.2.1 on 2025-05-29 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attachment",
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
                ("name", models.CharField(max_length=255, verbose_name="文件名称")),
                (
                    "original_name",
                    models.CharField(max_length=255, verbose_name="原始文件名"),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="attachments/%Y/%m/%d/", verbose_name="文件"
                    ),
                ),
                (
                    "file_type",
                    models.CharField(
                        choices=[
                            ("image", "图片"),
                            ("video", "视频"),
                            ("audio", "音频"),
                            ("document", "文档"),
                            ("archive", "压缩包"),
                            ("other", "其他"),
                        ],
                        default="other",
                        max_length=20,
                        verbose_name="文件类型",
                    ),
                ),
                (
                    "file_size",
                    models.PositiveIntegerField(verbose_name="文件大小(bytes)"),
                ),
                (
                    "mime_type",
                    models.CharField(max_length=100, verbose_name="MIME类型"),
                ),
                (
                    "download_count",
                    models.PositiveIntegerField(default=0, verbose_name="下载次数"),
                ),
                (
                    "is_public",
                    models.BooleanField(default=True, verbose_name="公开访问"),
                ),
            ],
            options={
                "verbose_name": "附件",
                "verbose_name_plural": "附件",
                "db_table": "core_attachments",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100, verbose_name="分类名称")),
                (
                    "slug",
                    models.SlugField(
                        max_length=100, unique=True, verbose_name="分类别名"
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="分类描述")),
                (
                    "icon",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="图标类名"
                    ),
                ),
                (
                    "sort_order",
                    models.PositiveIntegerField(default=0, verbose_name="排序"),
                ),
                (
                    "item_count",
                    models.PositiveIntegerField(default=0, verbose_name="项目数量"),
                ),
            ],
            options={
                "verbose_name": "分类",
                "verbose_name_plural": "分类",
                "db_table": "core_categories",
                "ordering": ["sort_order", "name"],
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
                ("title", models.CharField(max_length=200, verbose_name="通知标题")),
                ("message", models.TextField(verbose_name="通知内容")),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("info", "信息"),
                            ("success", "成功"),
                            ("warning", "警告"),
                            ("error", "错误"),
                            ("system", "系统"),
                        ],
                        default="info",
                        max_length=20,
                        verbose_name="通知类型",
                    ),
                ),
                ("is_read", models.BooleanField(default=False, verbose_name="已读")),
                (
                    "read_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="阅读时间"
                    ),
                ),
                ("action_url", models.URLField(blank=True, verbose_name="操作链接")),
                (
                    "action_text",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="操作文本"
                    ),
                ),
                (
                    "expires_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="过期时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "通知",
                "verbose_name_plural": "通知",
                "db_table": "core_notifications",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Setting",
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
                    "key",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="设置键"
                    ),
                ),
                ("value", models.TextField(verbose_name="设置值")),
                (
                    "value_type",
                    models.CharField(
                        choices=[
                            ("string", "字符串"),
                            ("integer", "整数"),
                            ("float", "浮点数"),
                            ("boolean", "布尔值"),
                            ("json", "JSON"),
                            ("text", "长文本"),
                        ],
                        default="string",
                        max_length=20,
                        verbose_name="值类型",
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="设置描述")),
                (
                    "group",
                    models.CharField(
                        default="general", max_length=50, verbose_name="设置组"
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(default=False, verbose_name="公开设置"),
                ),
                (
                    "is_editable",
                    models.BooleanField(default=True, verbose_name="可编辑"),
                ),
            ],
            options={
                "verbose_name": "系统设置",
                "verbose_name_plural": "系统设置",
                "db_table": "core_settings",
                "ordering": ["group", "key"],
            },
        ),
        migrations.CreateModel(
            name="SystemLog",
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
                    "level",
                    models.CharField(
                        choices=[
                            ("debug", "DEBUG"),
                            ("info", "INFO"),
                            ("warning", "WARNING"),
                            ("error", "ERROR"),
                            ("critical", "CRITICAL"),
                        ],
                        default="info",
                        max_length=20,
                        verbose_name="日志级别",
                    ),
                ),
                ("module", models.CharField(max_length=100, verbose_name="模块名称")),
                ("action", models.CharField(max_length=100, verbose_name="操作")),
                ("message", models.TextField(verbose_name="日志消息")),
                (
                    "ip_address",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="IP地址"
                    ),
                ),
                ("user_agent", models.TextField(blank=True, verbose_name="用户代理")),
                (
                    "extra_data",
                    models.JSONField(blank=True, default=dict, verbose_name="额外数据"),
                ),
            ],
            options={
                "verbose_name": "系统日志",
                "verbose_name_plural": "系统日志",
                "db_table": "core_system_logs",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
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
                    "name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="标签名称"
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="标签别名")),
                ("description", models.TextField(blank=True, verbose_name="标签描述")),
                (
                    "color",
                    models.CharField(
                        default="#007bff", max_length=7, verbose_name="标签颜色"
                    ),
                ),
                (
                    "icon",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="图标类名"
                    ),
                ),
                (
                    "usage_count",
                    models.PositiveIntegerField(default=0, verbose_name="使用次数"),
                ),
            ],
            options={
                "verbose_name": "标签",
                "verbose_name_plural": "标签",
                "db_table": "core_tags",
                "ordering": ["-usage_count", "name"],
            },
        ),
    ]
