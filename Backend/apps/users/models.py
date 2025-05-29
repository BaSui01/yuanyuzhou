from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """扩展的用户模型"""

    class GenderChoices(models.TextChoices):
        MALE = 'M', _('男性')
        FEMALE = 'F', _('女性')
        OTHER = 'O', _('其他')

    # 基本信息
    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name='手机号码'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='头像'
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='出生日期'
    )
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        null=True,
        blank=True,
        verbose_name='性别'
    )
    bio = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='个人简介'
    )

    # 地址信息
    country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='国家'
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='城市'
    )

    # 社交媒体
    website = models.URLField(
        null=True,
        blank=True,
        verbose_name='个人网站'
    )
    github = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='GitHub'
    )

    # 账户设置
    is_verified = models.BooleanField(
        default=False,
        verbose_name='已验证'
    )
    is_premium = models.BooleanField(
        default=False,
        verbose_name='高级用户'
    )
    privacy_setting = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='隐私设置'
    )

    # 时间戳
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    last_active = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='最后活跃时间'
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'users'
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.username or self.email

    @property
    def full_name(self):
        """获取完整姓名"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_avatar_url(self):
        """获取头像URL"""
        if self.avatar:
            return self.avatar.url
        return None


class UserProfile(models.Model):
    """用户档案扩展"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='用户'
    )

    # 偏好设置
    language = models.CharField(
        max_length=10,
        default='zh-hans',
        verbose_name='语言'
    )
    timezone = models.CharField(
        max_length=50,
        default='Asia/Shanghai',
        verbose_name='时区'
    )
    theme = models.CharField(
        max_length=20,
        default='light',
        choices=[
            ('light', '浅色'),
            ('dark', '深色'),
            ('auto', '自动'),
        ],
        verbose_name='主题'
    )

    # 通知设置
    email_notifications = models.BooleanField(
        default=True,
        verbose_name='邮件通知'
    )
    sms_notifications = models.BooleanField(
        default=True,
        verbose_name='短信通知'
    )
    push_notifications = models.BooleanField(
        default=True,
        verbose_name='推送通知'
    )

    # 统计信息
    login_count = models.PositiveIntegerField(
        default=0,
        verbose_name='登录次数'
    )
    points = models.PositiveIntegerField(
        default=0,
        verbose_name='积分'
    )
    level = models.PositiveIntegerField(
        default=1,
        verbose_name='等级'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        verbose_name = '用户档案'
        verbose_name_plural = '用户档案'
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.username}的档案"


class UserLoginLog(models.Model):
    """用户登录日志"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_logs',
        verbose_name='用户'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='IP地址'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='用户代理'
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='登录地点'
    )
    device_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='设备类型'
    )
    login_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='登录时间'
    )
    is_successful = models.BooleanField(
        default=True,
        verbose_name='登录成功'
    )

    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志'
        db_table = 'user_login_logs'
        ordering = ['-login_time']
        indexes = [
            models.Index(fields=['user', '-login_time']),
            models.Index(fields=['ip_address']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"
