from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel

User = get_user_model()


class AIModel(BaseModel):
    """AI模型管理"""
    MODEL_TYPES = [
        ('text_generation', '文本生成'),
        ('image_generation', '图像生成'),
        ('text_to_speech', '语音合成'),
        ('speech_to_text', '语音识别'),
        ('translation', '翻译'),
        ('summarization', '文本摘要'),
        ('code_generation', '代码生成'),
        ('chatbot', '聊天机器人'),
        ('sentiment_analysis', '情感分析'),
        ('object_detection', '物体检测'),
    ]

    STATUS_CHOICES = [
        ('active', '活跃'),
        ('inactive', '非活跃'),
        ('maintenance', '维护中'),
        ('deprecated', '已弃用'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name='模型名称'
    )
    model_type = models.CharField(
        max_length=50,
        choices=MODEL_TYPES,
        verbose_name='模型类型'
    )
    description = models.TextField(
        verbose_name='模型描述'
    )
    version = models.CharField(
        max_length=20,
        default='1.0.0',
        verbose_name='版本号'
    )
    api_endpoint = models.URLField(
        verbose_name='API端点'
    )
    api_key = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='API密钥'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='状态'
    )
    max_requests_per_minute = models.PositiveIntegerField(
        default=60,
        verbose_name='每分钟最大请求数'
    )
    cost_per_request = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0.0000,
        verbose_name='每次请求成本'
    )
    configuration = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='配置参数'
    )

    class Meta:
        verbose_name = 'AI模型'
        verbose_name_plural = 'AI模型'
        db_table = 'ai_models'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.version})"

    def is_available(self):
        """检查模型是否可用"""
        return self.status == 'active' and self.is_active


class AIRequest(BaseModel):
    """AI请求记录"""
    REQUEST_TYPES = [
        ('text', '文本请求'),
        ('image', '图像请求'),
        ('audio', '音频请求'),
        ('video', '视频请求'),
        ('file', '文件请求'),
    ]

    STATUS_CHOICES = [
        ('pending', '等待中'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('cancelled', '已取消'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ai_requests',
        verbose_name='用户'
    )
    ai_model = models.ForeignKey(
        AIModel,
        on_delete=models.CASCADE,
        related_name='requests',
        verbose_name='AI模型'
    )
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPES,
        verbose_name='请求类型'
    )
    input_data = models.JSONField(
        verbose_name='输入数据'
    )
    output_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name='输出数据'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='状态'
    )
    processing_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name='处理时间(秒)'
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0.0000,
        verbose_name='成本'
    )
    error_message = models.TextField(
        blank=True,
        verbose_name='错误信息'
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='元数据'
    )

    class Meta:
        verbose_name = 'AI请求'
        verbose_name_plural = 'AI请求'
        db_table = 'ai_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['ai_model', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.ai_model.name} ({self.status})"

    def mark_processing(self):
        """标记为处理中"""
        self.status = 'processing'
        self.save(update_fields=['status'])

    def mark_completed(self, output_data, processing_time=None):
        """标记为完成"""
        self.status = 'completed'
        self.output_data = output_data
        if processing_time:
            self.processing_time = processing_time
        self.save(update_fields=['status', 'output_data', 'processing_time'])

    def mark_failed(self, error_message):
        """标记为失败"""
        self.status = 'failed'
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message'])


class ChatConversation(BaseModel):
    """聊天对话"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_conversations',
        verbose_name='用户'
    )
    ai_model = models.ForeignKey(
        AIModel,
        on_delete=models.CASCADE,
        related_name='conversations',
        verbose_name='AI模型'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='对话标题'
    )
    system_prompt = models.TextField(
        blank=True,
        verbose_name='系统提示'
    )
    context = models.JSONField(
        default=list,
        verbose_name='对话上下文'
    )
    total_tokens = models.PositiveIntegerField(
        default=0,
        verbose_name='总Token数'
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0.0000,
        verbose_name='总成本'
    )
    is_archived = models.BooleanField(
        default=False,
        verbose_name='已归档'
    )

    class Meta:
        verbose_name = '聊天对话'
        verbose_name_plural = '聊天对话'
        db_table = 'ai_chat_conversations'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def add_message(self, role, content, tokens=0):
        """添加消息到对话"""
        message = {
            'role': role,
            'content': content,
            'timestamp': timezone.now().isoformat(),
            'tokens': tokens
        }
        self.context.append(message)
        self.total_tokens += tokens
        self.save(update_fields=['context', 'total_tokens', 'updated_at'])


class ChatMessage(BaseModel):
    """聊天消息"""
    ROLE_CHOICES = [
        ('user', '用户'),
        ('assistant', 'AI助手'),
        ('system', '系统'),
    ]

    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='对话'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name='角色'
    )
    content = models.TextField(
        verbose_name='消息内容'
    )
    tokens = models.PositiveIntegerField(
        default=0,
        verbose_name='Token数'
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0.0000,
        verbose_name='成本'
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='元数据'
    )

    class Meta:
        verbose_name = '聊天消息'
        verbose_name_plural = '聊天消息'
        db_table = 'ai_chat_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.conversation.title} - {self.role}: {self.content[:50]}"


class AITemplate(BaseModel):
    """AI模板"""
    TEMPLATE_TYPES = [
        ('prompt', '提示模板'),
        ('workflow', '工作流模板'),
        ('preset', '预设模板'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name='模板名称'
    )
    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPES,
        verbose_name='模板类型'
    )
    description = models.TextField(
        verbose_name='模板描述'
    )
    content = models.TextField(
        verbose_name='模板内容'
    )
    variables = models.JSONField(
        default=list,
        verbose_name='变量定义'
    )
    ai_model = models.ForeignKey(
        AIModel,
        on_delete=models.CASCADE,
        related_name='templates',
        verbose_name='适用模型'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_ai_templates',
        verbose_name='创建者'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='公开模板'
    )
    usage_count = models.PositiveIntegerField(
        default=0,
        verbose_name='使用次数'
    )

    class Meta:
        verbose_name = 'AI模板'
        verbose_name_plural = 'AI模板'
        db_table = 'ai_templates'
        ordering = ['-usage_count', 'name']

    def __str__(self):
        return self.name

    def increment_usage(self):
        """增加使用次数"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])


class AIUsageStats(BaseModel):
    """AI使用统计"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ai_usage_stats',
        verbose_name='用户'
    )
    ai_model = models.ForeignKey(
        AIModel,
        on_delete=models.CASCADE,
        related_name='usage_stats',
        verbose_name='AI模型'
    )
    date = models.DateField(
        verbose_name='日期'
    )
    request_count = models.PositiveIntegerField(
        default=0,
        verbose_name='请求次数'
    )
    token_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Token总数'
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0.0000,
        verbose_name='总成本'
    )
    success_count = models.PositiveIntegerField(
        default=0,
        verbose_name='成功次数'
    )
    error_count = models.PositiveIntegerField(
        default=0,
        verbose_name='错误次数'
    )

    class Meta:
        verbose_name = 'AI使用统计'
        verbose_name_plural = 'AI使用统计'
        db_table = 'ai_usage_stats'
        ordering = ['-date']
        unique_together = ['user', 'ai_model', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.ai_model.name} ({self.date})"

    @classmethod
    def record_usage(cls, user, ai_model, tokens=0, cost=0, success=True):
        """记录使用情况"""
        today = timezone.now().date()
        stats, created = cls.objects.get_or_create(
            user=user,
            ai_model=ai_model,
            date=today,
            defaults={
                'request_count': 0,
                'token_count': 0,
                'total_cost': 0,
                'success_count': 0,
                'error_count': 0,
            }
        )

        stats.request_count += 1
        stats.token_count += tokens
        stats.total_cost += cost

        if success:
            stats.success_count += 1
        else:
            stats.error_count += 1

        stats.save()
        return stats
