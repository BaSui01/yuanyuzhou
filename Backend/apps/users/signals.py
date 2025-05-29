from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import User, UserProfile, UserLoginLog


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """当创建用户时自动创建用户档案"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存用户时同时保存用户档案"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(pre_save, sender=User)
def update_user_timestamp(sender, instance, **kwargs):
    """更新用户的修改时间"""
    if instance.pk:  # 只有在更新时才设置
        instance.updated_at = timezone.now()


def log_user_login(sender, user, request, **kwargs):
    """记录用户登录日志"""
    try:
        # 获取IP地址
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # 获取用户代理
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # 简单的设备类型检测
        device_type = 'Unknown'
        if user_agent:
            user_agent_lower = user_agent.lower()
            if 'mobile' in user_agent_lower or 'android' in user_agent_lower or 'iphone' in user_agent_lower:
                device_type = 'Mobile'
            elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
                device_type = 'Tablet'
            else:
                device_type = 'Desktop'

        # 创建登录日志
        UserLoginLog.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            device_type=device_type,
            is_successful=True
        )

        # 更新用户档案的登录次数
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.login_count += 1
        profile.save(update_fields=['login_count'])

        # 更新用户最后活跃时间
        user.last_active = timezone.now()
        user.save(update_fields=['last_active'])

    except Exception as e:
        # 记录错误但不影响登录流程
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error logging user login: {e}")


def log_user_login_failed(sender, credentials, request, **kwargs):
    """记录用户登录失败日志"""
    try:
        # 获取IP地址
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # 获取用户代理
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # 尝试找到用户（如果用户名/邮箱存在）
        username = credentials.get('username')
        user = None
        if username:
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.filter(
                    models.Q(username=username) | models.Q(email=username)
                ).first()
            except:
                pass

        # 创建失败登录日志
        UserLoginLog.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            device_type='Unknown',
            is_successful=False
        )

    except Exception as e:
        # 记录错误但不影响登录流程
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error logging failed login: {e}")


# 连接Django的登录信号
from django.contrib.auth.signals import user_logged_in, user_login_failed

user_logged_in.connect(log_user_login)
user_login_failed.connect(log_user_login_failed)
