from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BaseModel(models.Model):
    """基础模型类，提供通用字段"""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='激活状态'
    )

    class Meta:
        abstract = True


class Tag(BaseModel):
    """标签模型"""
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='标签名称'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='标签别名'
    )
    description = models.TextField(
        blank=True,
        verbose_name='标签描述'
    )
    color = models.CharField(
        max_length=7,
        default='#007bff',
        verbose_name='标签颜色'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='图标类名'
    )
    usage_count = models.PositiveIntegerField(
        default=0,
        verbose_name='使用次数'
    )

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        db_table = 'core_tags'
        ordering = ['-usage_count', 'name']

    def __str__(self):
        return self.name

    def increment_usage(self):
        """增加使用次数"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])

    def decrement_usage(self):
        """减少使用次数"""
        if self.usage_count > 0:
            self.usage_count -= 1
            self.save(update_fields=['usage_count'])


class Category(BaseModel):
    """分类模型"""
    name = models.CharField(
        max_length=100,
        verbose_name='分类名称'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='分类别名'
    )
    description = models.TextField(
        blank=True,
        verbose_name='分类描述'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='父分类'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='图标类名'
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='排序'
    )
    item_count = models.PositiveIntegerField(
        default=0,
        verbose_name='项目数量'
    )

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        db_table = 'core_categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

    def get_absolute_path(self):
        """获取完整路径"""
        path = [self.slug]
        parent = self.parent
        while parent:
            path.insert(0, parent.slug)
            parent = parent.parent
        return '/'.join(path)

    def increment_item_count(self):
        """增加项目数量"""
        self.item_count += 1
        self.save(update_fields=['item_count'])
        if self.parent:
            self.parent.increment_item_count()

    def decrement_item_count(self):
        """减少项目数量"""
        if self.item_count > 0:
            self.item_count -= 1
            self.save(update_fields=['item_count'])
            if self.parent:
                self.parent.decrement_item_count()


class Attachment(BaseModel):
    """附件模型"""
    ATTACHMENT_TYPES = [
        ('image', '图片'),
        ('video', '视频'),
        ('audio', '音频'),
        ('document', '文档'),
        ('archive', '压缩包'),
        ('other', '其他'),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name='文件名称'
    )
    original_name = models.CharField(
        max_length=255,
        verbose_name='原始文件名'
    )
    file = models.FileField(
        upload_to='attachments/%Y/%m/%d/',
        verbose_name='文件'
    )
    file_type = models.CharField(
        max_length=20,
        choices=ATTACHMENT_TYPES,
        default='other',
        verbose_name='文件类型'
    )
    file_size = models.PositiveIntegerField(
        verbose_name='文件大小(bytes)'
    )
    mime_type = models.CharField(
        max_length=100,
        verbose_name='MIME类型'
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_attachments',
        verbose_name='上传者'
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name='下载次数'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='公开访问'
    )

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = '附件'
        db_table = 'core_attachments'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_file_size_display(self):
        """获取友好的文件大小显示"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def increment_download_count(self):
        """增加下载次数"""
        self.download_count += 1
        self.save(update_fields=['download_count'])


class Notification(BaseModel):
    """通知模型"""
    NOTIFICATION_TYPES = [
        ('info', '信息'),
        ('success', '成功'),
        ('warning', '警告'),
        ('error', '错误'),
        ('system', '系统'),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='接收者'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sent_notifications',
        verbose_name='发送者'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='通知标题'
    )
    message = models.TextField(
        verbose_name='通知内容'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='info',
        verbose_name='通知类型'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='已读'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='阅读时间'
    )
    action_url = models.URLField(
        blank=True,
        verbose_name='操作链接'
    )
    action_text = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='操作文本'
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='过期时间'
    )

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'
        db_table = 'core_notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"

    def mark_as_read(self):
        """标记为已读"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def is_expired(self):
        """检查是否过期"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    @classmethod
    def create_notification(cls, recipient, title, message, notification_type='info', sender=None, **kwargs):
        """创建通知的便捷方法"""
        return cls.objects.create(
            recipient=recipient,
            sender=sender,
            title=title,
            message=message,
            notification_type=notification_type,
            **kwargs
        )


class SystemLog(BaseModel):
    """系统日志模型"""
    LOG_LEVELS = [
        ('debug', 'DEBUG'),
        ('info', 'INFO'),
        ('warning', 'WARNING'),
        ('error', 'ERROR'),
        ('critical', 'CRITICAL'),
    ]

    level = models.CharField(
        max_length=20,
        choices=LOG_LEVELS,
        default='info',
        verbose_name='日志级别'
    )
    module = models.CharField(
        max_length=100,
        verbose_name='模块名称'
    )
    action = models.CharField(
        max_length=100,
        verbose_name='操作'
    )
    message = models.TextField(
        verbose_name='日志消息'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='system_logs',
        verbose_name='用户'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP地址'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='用户代理'
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='额外数据'
    )

    class Meta:
        verbose_name = '系统日志'
        verbose_name_plural = '系统日志'
        db_table = 'core_system_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level', 'created_at']),
            models.Index(fields=['module', 'action']),
        ]

    def __str__(self):
        return f"[{self.level.upper()}] {self.module} - {self.action}"

    @classmethod
    def log(cls, level, module, action, message, user=None, request=None, **extra_data):
        """记录日志的便捷方法"""
        ip_address = None
        user_agent = ''

        if request:
            # 获取IP地址
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')

            # 获取用户代理
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # 如果没有传入用户，尝试从请求中获取
            if not user and hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user

        return cls.objects.create(
            level=level,
            module=module,
            action=action,
            message=message,
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            extra_data=extra_data
        )


class Setting(BaseModel):
    """系统设置模型"""
    SETTING_TYPES = [
        ('string', '字符串'),
        ('integer', '整数'),
        ('float', '浮点数'),
        ('boolean', '布尔值'),
        ('json', 'JSON'),
        ('text', '长文本'),
    ]

    key = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='设置键'
    )
    value = models.TextField(
        verbose_name='设置值'
    )
    value_type = models.CharField(
        max_length=20,
        choices=SETTING_TYPES,
        default='string',
        verbose_name='值类型'
    )
    description = models.TextField(
        blank=True,
        verbose_name='设置描述'
    )
    group = models.CharField(
        max_length=50,
        default='general',
        verbose_name='设置组'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='公开设置'
    )
    is_editable = models.BooleanField(
        default=True,
        verbose_name='可编辑'
    )

    class Meta:
        verbose_name = '系统设置'
        verbose_name_plural = '系统设置'
        db_table = 'core_settings'
        ordering = ['group', 'key']

    def __str__(self):
        return f"{self.group}.{self.key}"

    def get_typed_value(self):
        """获取类型化的值"""
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.value_type == 'json':
            import json
            return json.loads(self.value)
        else:
            return self.value

    @classmethod
    def get_setting(cls, key, default=None):
        """获取设置值"""
        try:
            setting = cls.objects.get(key=key, is_active=True)
            return setting.get_typed_value()
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_setting(cls, key, value, value_type='string', description='', group='general'):
        """设置值"""
        if value_type == 'json':
            import json
            value = json.dumps(value, ensure_ascii=False)
        else:
            value = str(value)

        setting, created = cls.objects.update_or_create(
            key=key,
            defaults={
                'value': value,
                'value_type': value_type,
                'description': description,
                'group': group,
            }
        )
        return setting
