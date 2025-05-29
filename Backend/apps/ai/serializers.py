from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    AIModel, AIRequest, ChatConversation, ChatMessage,
    AITemplate, AIUsageStats
)

User = get_user_model()


class AIModelSerializer(serializers.ModelSerializer):
    """AI模型序列化器"""
    is_available = serializers.ReadOnlyField()

    class Meta:
        model = AIModel
        fields = [
            'id', 'name', 'model_type', 'description', 'version',
            'status', 'max_requests_per_minute', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AIRequestSerializer(serializers.ModelSerializer):
    """AI请求序列化器"""
    user = serializers.StringRelatedField(read_only=True)
    ai_model_name = serializers.CharField(source='ai_model.name', read_only=True)

    class Meta:
        model = AIRequest
        fields = [
            'id', 'user', 'ai_model', 'ai_model_name', 'request_type',
            'input_data', 'output_data', 'status', 'processing_time',
            'cost', 'error_message', 'metadata', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'ai_model_name', 'output_data', 'status',
            'processing_time', 'cost', 'error_message', 'created_at', 'updated_at'
        ]


class AIRequestCreateSerializer(serializers.ModelSerializer):
    """AI请求创建序列化器"""

    class Meta:
        model = AIRequest
        fields = ['ai_model', 'request_type', 'input_data', 'metadata']

    def validate_ai_model(self, value):
        """验证AI模型是否可用"""
        if not value.is_available():
            raise serializers.ValidationError("选择的AI模型当前不可用")
        return value

    def create(self, validated_data):
        """创建AI请求"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ChatMessageSerializer(serializers.ModelSerializer):
    """聊天消息序列化器"""

    class Meta:
        model = ChatMessage
        fields = [
            'id', 'role', 'content', 'tokens', 'cost',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'tokens', 'cost', 'created_at']


class ChatConversationSerializer(serializers.ModelSerializer):
    """聊天对话序列化器"""
    user = serializers.StringRelatedField(read_only=True)
    ai_model_name = serializers.CharField(source='ai_model.name', read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatConversation
        fields = [
            'id', 'user', 'ai_model', 'ai_model_name', 'title',
            'system_prompt', 'total_tokens', 'total_cost',
            'is_archived', 'message_count', 'messages',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'ai_model_name', 'total_tokens', 'total_cost',
            'message_count', 'created_at', 'updated_at'
        ]

    def get_message_count(self, obj):
        """获取消息数量"""
        return obj.messages.count()

    def create(self, validated_data):
        """创建对话"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ChatConversationListSerializer(serializers.ModelSerializer):
    """聊天对话列表序列化器（简化版）"""
    ai_model_name = serializers.CharField(source='ai_model.name', read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message_time = serializers.SerializerMethodField()

    class Meta:
        model = ChatConversation
        fields = [
            'id', 'ai_model_name', 'title', 'total_tokens',
            'total_cost', 'is_archived', 'message_count',
            'last_message_time', 'created_at', 'updated_at'
        ]

    def get_message_count(self, obj):
        """获取消息数量"""
        return obj.messages.count()

    def get_last_message_time(self, obj):
        """获取最后消息时间"""
        last_message = obj.messages.last()
        return last_message.created_at if last_message else None


class SendMessageSerializer(serializers.Serializer):
    """发送消息序列化器"""
    conversation_id = serializers.IntegerField()
    content = serializers.CharField()

    def validate_conversation_id(self, value):
        """验证对话ID"""
        user = self.context['request'].user
        try:
            conversation = ChatConversation.objects.get(
                id=value,
                user=user,
                is_active=True
            )
            return conversation
        except ChatConversation.DoesNotExist:
            raise serializers.ValidationError("对话不存在或无权限访问")

    def validate_content(self, value):
        """验证消息内容"""
        if not value.strip():
            raise serializers.ValidationError("消息内容不能为空")
        return value.strip()


class AITemplateSerializer(serializers.ModelSerializer):
    """AI模板序列化器"""
    creator = serializers.StringRelatedField(read_only=True)
    ai_model_name = serializers.CharField(source='ai_model.name', read_only=True)

    class Meta:
        model = AITemplate
        fields = [
            'id', 'name', 'template_type', 'description', 'content',
            'variables', 'ai_model', 'ai_model_name', 'creator',
            'is_public', 'usage_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'creator', 'ai_model_name', 'usage_count',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        """创建模板"""
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class AIUsageStatsSerializer(serializers.ModelSerializer):
    """AI使用统计序列化器"""
    user = serializers.StringRelatedField(read_only=True)
    ai_model_name = serializers.CharField(source='ai_model.name', read_only=True)
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = AIUsageStats
        fields = [
            'id', 'user', 'ai_model_name', 'date', 'request_count',
            'token_count', 'total_cost', 'success_count', 'error_count',
            'success_rate', 'created_at'
        ]

    def get_success_rate(self, obj):
        """计算成功率"""
        if obj.request_count == 0:
            return 0
        return round((obj.success_count / obj.request_count) * 100, 2)


class UserUsageStatsSerializer(serializers.Serializer):
    """用户使用统计序列化器"""
    total_requests = serializers.IntegerField()
    total_tokens = serializers.IntegerField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=4)
    total_success = serializers.IntegerField()
    total_errors = serializers.IntegerField()
    success_rate = serializers.FloatField()
    most_used_model = serializers.CharField()
    daily_stats = AIUsageStatsSerializer(many=True)


class ModelUsageStatsSerializer(serializers.Serializer):
    """模型使用统计序列化器"""
    model_name = serializers.CharField()
    total_requests = serializers.IntegerField()
    total_tokens = serializers.IntegerField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=4)
    unique_users = serializers.IntegerField()
    success_rate = serializers.FloatField()


class ChatCompletionSerializer(serializers.Serializer):
    """聊天完成序列化器"""
    model = serializers.CharField()
    messages = serializers.ListField(
        child=serializers.DictField()
    )
    temperature = serializers.FloatField(
        min_value=0.0,
        max_value=2.0,
        default=1.0
    )
    max_tokens = serializers.IntegerField(
        min_value=1,
        max_value=4096,
        default=150
    )
    top_p = serializers.FloatField(
        min_value=0.0,
        max_value=1.0,
        default=1.0
    )
    frequency_penalty = serializers.FloatField(
        min_value=-2.0,
        max_value=2.0,
        default=0.0
    )
    presence_penalty = serializers.FloatField(
        min_value=-2.0,
        max_value=2.0,
        default=0.0
    )
    stream = serializers.BooleanField(default=False)


class TextGenerationSerializer(serializers.Serializer):
    """文本生成序列化器"""
    model = serializers.CharField()
    prompt = serializers.CharField()
    max_tokens = serializers.IntegerField(
        min_value=1,
        max_value=4096,
        default=150
    )
    temperature = serializers.FloatField(
        min_value=0.0,
        max_value=2.0,
        default=1.0
    )
    top_p = serializers.FloatField(
        min_value=0.0,
        max_value=1.0,
        default=1.0
    )
    frequency_penalty = serializers.FloatField(
        min_value=-2.0,
        max_value=2.0,
        default=0.0
    )
    presence_penalty = serializers.FloatField(
        min_value=-2.0,
        max_value=2.0,
        default=0.0
    )


class ImageGenerationSerializer(serializers.Serializer):
    """图像生成序列化器"""
    model = serializers.CharField()
    prompt = serializers.CharField()
    n = serializers.IntegerField(
        min_value=1,
        max_value=10,
        default=1
    )
    size = serializers.ChoiceField(
        choices=[
            ('256x256', '256x256'),
            ('512x512', '512x512'),
            ('1024x1024', '1024x1024'),
        ],
        default='1024x1024'
    )
    quality = serializers.ChoiceField(
        choices=[
            ('standard', 'Standard'),
            ('hd', 'HD'),
        ],
        default='standard'
    )
    style = serializers.ChoiceField(
        choices=[
            ('vivid', 'Vivid'),
            ('natural', 'Natural'),
        ],
        default='vivid'
    )


class TemplateRenderSerializer(serializers.Serializer):
    """模板渲染序列化器"""
    template_id = serializers.IntegerField()
    variables = serializers.DictField()

    def validate_template_id(self, value):
        """验证模板ID"""
        try:
            template = AITemplate.objects.get(id=value, is_active=True)
            # 检查是否有权限访问
            if not template.is_public and template.creator != self.context['request'].user:
                raise serializers.ValidationError("无权限访问此模板")
            return template
        except AITemplate.DoesNotExist:
            raise serializers.ValidationError("模板不存在")
