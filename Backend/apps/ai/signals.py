from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from apps.core.models import SystemLog
from .models import AIRequest, ChatMessage, AIUsageStats


@receiver(post_save, sender=AIRequest)
def ai_request_created(sender, instance, created, **kwargs):
    """AI请求创建后的处理"""
    if created:
        # 记录系统日志
        SystemLog.log(
            level='info',
            module='ai',
            action='request_created',
            message=f'用户 {instance.user.username} 创建了AI请求',
            user=instance.user,
            ai_model=instance.ai_model.name,
            request_type=instance.request_type
        )

        # 清除相关缓存
        cache.delete('available_ai_models')


@receiver(post_save, sender=ChatMessage)
def chat_message_created(sender, instance, created, **kwargs):
    """聊天消息创建后的处理"""
    if created:
        # 更新对话的token和成本统计
        conversation = instance.conversation
        conversation.total_tokens += instance.tokens
        conversation.total_cost += instance.cost
        conversation.save(update_fields=['total_tokens', 'total_cost', 'updated_at'])

        # 如果是AI回复，记录使用统计
        if instance.role == 'assistant':
            AIUsageStats.record_usage(
                user=conversation.user,
                ai_model=conversation.ai_model,
                tokens=instance.tokens,
                cost=instance.cost,
                success=True
            )


@receiver(post_delete, sender=AIRequest)
def ai_request_deleted(sender, instance, **kwargs):
    """AI请求删除后的处理"""
    SystemLog.log(
        level='info',
        module='ai',
        action='request_deleted',
        message=f'AI请求 {instance.id} 已被删除',
        user=instance.user,
        ai_model=instance.ai_model.name if instance.ai_model else None
    )
