from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import secrets
import string

User = get_user_model()


class EmailVerificationToken(models.Model):
    """邮箱验证令牌"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='email_verification_tokens',
        verbose_name='用户'
    )
    token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='验证令牌'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    expires_at = models.DateTimeField(
        verbose_name='过期时间'
    )
    is_used = models.BooleanField(
        default=False,
        verbose_name='已使用'
    )

    class Meta:
        verbose_name = '邮箱验证令牌'
        verbose_name_plural = '邮箱验证令牌'
        db_table = 'auth_email_verification_tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.token[:10]}..."

    @classmethod
    def generate_token(cls, user, hours=24):
        """生成验证令牌"""
        # 生成随机令牌
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))

        # 设置过期时间
        expires_at = timezone.now() + timezone.timedelta(hours=hours)

        # 删除之前未使用的令牌
        cls.objects.filter(user=user, is_used=False).delete()

        # 创建新令牌
        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

    def is_valid(self):
        """检查令牌是否有效"""
        return not self.is_used and timezone.now() < self.expires_at

    def mark_as_used(self):
        """标记令牌为已使用"""
        self.is_used = True
        self.save(update_fields=['is_used'])


class PasswordResetToken(models.Model):
    """密码重置令牌"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        verbose_name='用户'
    )
    token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='重置令牌'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    expires_at = models.DateTimeField(
        verbose_name='过期时间'
    )
    is_used = models.BooleanField(
        default=False,
        verbose_name='已使用'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='请求IP'
    )

    class Meta:
        verbose_name = '密码重置令牌'
        verbose_name_plural = '密码重置令牌'
        db_table = 'auth_password_reset_tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.token[:10]}..."

    @classmethod
    def generate_token(cls, user, ip_address=None, hours=2):
        """生成重置令牌"""
        # 生成随机令牌
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))

        # 设置过期时间（密码重置令牌有效期较短）
        expires_at = timezone.now() + timezone.timedelta(hours=hours)

        # 删除之前未使用的令牌
        cls.objects.filter(user=user, is_used=False).delete()

        # 创建新令牌
        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at,
            ip_address=ip_address
        )

    def is_valid(self):
        """检查令牌是否有效"""
        return not self.is_used and timezone.now() < self.expires_at

    def mark_as_used(self):
        """标记令牌为已使用"""
        self.is_used = True
        self.save(update_fields=['is_used'])


class LoginAttempt(models.Model):
    """登录尝试记录"""
    username = models.CharField(
        max_length=150,
        verbose_name='用户名'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='IP地址'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='用户代理'
    )
    is_successful = models.BooleanField(
        default=False,
        verbose_name='登录成功'
    )
    failure_reason = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='失败原因'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='尝试时间'
    )

    class Meta:
        verbose_name = '登录尝试'
        verbose_name_plural = '登录尝试'
        db_table = 'auth_login_attempts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ip_address', '-created_at']),
            models.Index(fields=['username', '-created_at']),
        ]

    def __str__(self):
        status = '成功' if self.is_successful else '失败'
        return f"{self.username} - {self.ip_address} - {status}"

    @classmethod
    def record_attempt(cls, username, ip_address, user_agent='', is_successful=False, failure_reason=''):
        """记录登录尝试"""
        return cls.objects.create(
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            is_successful=is_successful,
            failure_reason=failure_reason
        )

    @classmethod
    def get_failed_attempts(cls, username=None, ip_address=None, minutes=30):
        """获取失败尝试次数"""
        time_threshold = timezone.now() - timezone.timedelta(minutes=minutes)
        queryset = cls.objects.filter(
            is_successful=False,
            created_at__gte=time_threshold
        )

        if username:
            queryset = queryset.filter(username=username)
        if ip_address:
            queryset = queryset.filter(ip_address=ip_address)

        return queryset.count()

    @classmethod
    def is_blocked(cls, username=None, ip_address=None, max_attempts=5):
        """检查是否被阻止登录"""
        failed_attempts = cls.get_failed_attempts(username, ip_address)
        return failed_attempts >= max_attempts


class TwoFactorAuth(models.Model):
    """双因子认证"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='two_factor_auth',
        verbose_name='用户'
    )
    is_enabled = models.BooleanField(
        default=False,
        verbose_name='启用状态'
    )
    secret_key = models.CharField(
        max_length=32,
        blank=True,
        verbose_name='密钥'
    )
    backup_codes = models.JSONField(
        default=list,
        blank=True,
        verbose_name='备用代码'
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
        verbose_name = '双因子认证'
        verbose_name_plural = '双因子认证'
        db_table = 'auth_two_factor'

    def __str__(self):
        status = '已启用' if self.is_enabled else '未启用'
        return f"{self.user.username} - {status}"

    def generate_backup_codes(self, count=10):
        """生成备用代码"""
        codes = []
        for _ in range(count):
            code = ''.join(secrets.choice(string.digits) for _ in range(8))
            codes.append(code)
        self.backup_codes = codes
        self.save(update_fields=['backup_codes'])
        return codes

    def use_backup_code(self, code):
        """使用备用代码"""
        if code in self.backup_codes:
            self.backup_codes.remove(code)
            self.save(update_fields=['backup_codes'])
            return True
        return False


class APIKey(models.Model):
    """API密钥"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='api_keys',
        verbose_name='用户'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='密钥名称'
    )
    key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='API密钥'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='激活状态'
    )
    permissions = models.JSONField(
        default=list,
        blank=True,
        verbose_name='权限列表'
    )
    last_used = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='最后使用时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='过期时间'
    )

    class Meta:
        verbose_name = 'API密钥'
        verbose_name_plural = 'API密钥'
        db_table = 'auth_api_keys'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    @classmethod
    def generate_key(cls, user, name, permissions=None, expires_days=None):
        """生成API密钥"""
        # 生成密钥
        key = 'ak_' + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(48))

        # 设置过期时间
        expires_at = None
        if expires_days:
            expires_at = timezone.now() + timezone.timedelta(days=expires_days)

        return cls.objects.create(
            user=user,
            name=name,
            key=key,
            permissions=permissions or [],
            expires_at=expires_at
        )

    def is_valid(self):
        """检查密钥是否有效"""
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True

    def update_last_used(self):
        """更新最后使用时间"""
        self.last_used = timezone.now()
        self.save(update_fields=['last_used'])
