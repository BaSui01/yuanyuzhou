from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from decimal import Decimal
import json
import time

from .models import (
    AIModel, AIRequest, ChatConversation, ChatMessage,
    AITemplate, AIUsageStats
)
from .serializers import (
    AIModelSerializer, AIRequestSerializer, AIRequestCreateSerializer,
    ChatConversationSerializer, ChatConversationListSerializer,
    ChatMessageSerializer, SendMessageSerializer, AITemplateSerializer,
    AIUsageStatsSerializer, UserUsageStatsSerializer, ModelUsageStatsSerializer,
    ChatCompletionSerializer, TextGenerationSerializer, ImageGenerationSerializer,
    TemplateRenderSerializer
)
from apps.core.models import SystemLog


class AIModelListView(generics.ListAPIView):
    """AI模型列表"""
    serializer_class = AIModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = AIModel.objects.filter(is_active=True)
        model_type = self.request.query_params.get('model_type', None)
        status_filter = self.request.query_params.get('status', None)

        if model_type:
            queryset = queryset.filter(model_type=model_type)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('name')


class AIRequestListView(generics.ListCreateAPIView):
    """AI请求列表和创建"""
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AIRequestCreateSerializer
        return AIRequestSerializer

    def get_queryset(self):
        queryset = AIRequest.objects.filter(user=self.request.user)

        # 过滤条件
        status_filter = self.request.query_params.get('status', None)
        model_id = self.request.query_params.get('model_id', None)
        request_type = self.request.query_params.get('request_type', None)

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if model_id:
            queryset = queryset.filter(ai_model_id=model_id)
        if request_type:
            queryset = queryset.filter(request_type=request_type)

        return queryset.order_by('-created_at')


class AIRequestDetailView(generics.RetrieveAPIView):
    """AI请求详情"""
    serializer_class = AIRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AIRequest.objects.filter(user=self.request.user)


class ChatConversationListView(generics.ListCreateAPIView):
    """聊天对话列表和创建"""
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatConversationSerializer
        return ChatConversationListSerializer

    def get_queryset(self):
        queryset = ChatConversation.objects.filter(
            user=self.request.user,
            is_active=True
        )

        # 过滤条件
        is_archived = self.request.query_params.get('archived', None)
        model_id = self.request.query_params.get('model_id', None)

        if is_archived is not None:
            queryset = queryset.filter(is_archived=is_archived.lower() == 'true')
        if model_id:
            queryset = queryset.filter(ai_model_id=model_id)

        return queryset.order_by('-updated_at')


class ChatConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """聊天对话详情、更新和删除"""
    serializer_class = ChatConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatConversation.objects.filter(
            user=self.request.user,
            is_active=True
        )

    def delete(self, request, *args, **kwargs):
        """软删除对话"""
        conversation = self.get_object()
        conversation.is_active = False
        conversation.save()
        return Response({'message': '对话已删除'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_message(request):
    """发送聊天消息"""
    serializer = SendMessageSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        conversation = serializer.validated_data['conversation_id']
        content = serializer.validated_data['content']

        # 创建用户消息
        user_message = ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=content
        )

        # 这里应该调用AI模型API获取回复
        # 暂时返回模拟回复
        ai_response = f"这是对 '{content}' 的AI回复"

        # 创建AI回复消息
        ai_message = ChatMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_response,
            tokens=50,  # 模拟token数
            cost=Decimal('0.0010')  # 模拟成本
        )

        # 更新对话统计
        conversation.total_tokens += 50
        conversation.total_cost += Decimal('0.0010')
        conversation.save()

        # 记录使用统计
        AIUsageStats.record_usage(
            user=request.user,
            ai_model=conversation.ai_model,
            tokens=50,
            cost=Decimal('0.0010'),
            success=True
        )

        return Response({
            'user_message': ChatMessageSerializer(user_message).data,
            'ai_message': ChatMessageSerializer(ai_message).data
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def archive_conversation(request, conversation_id):
    """归档对话"""
    try:
        conversation = ChatConversation.objects.get(
            id=conversation_id,
            user=request.user,
            is_active=True
        )
        conversation.is_archived = not conversation.is_archived
        conversation.save()

        action = '归档' if conversation.is_archived else '取消归档'
        return Response({'message': f'对话已{action}'})

    except ChatConversation.DoesNotExist:
        return Response(
            {'error': '对话不存在'},
            status=status.HTTP_404_NOT_FOUND
        )


class AITemplateListView(generics.ListCreateAPIView):
    """AI模板列表和创建"""
    serializer_class = AITemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # 获取公开模板和用户自己的模板
        queryset = AITemplate.objects.filter(
            Q(is_public=True) | Q(creator=self.request.user),
            is_active=True
        )

        # 过滤条件
        template_type = self.request.query_params.get('template_type', None)
        model_id = self.request.query_params.get('model_id', None)

        if template_type:
            queryset = queryset.filter(template_type=template_type)
        if model_id:
            queryset = queryset.filter(ai_model_id=model_id)

        return queryset.order_by('-usage_count', 'name')


class AITemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """AI模板详情、更新和删除"""
    serializer_class = AITemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 只能操作自己创建的模板
        return AITemplate.objects.filter(
            creator=self.request.user,
            is_active=True
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def render_template(request):
    """渲染模板"""
    serializer = TemplateRenderSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        template = serializer.validated_data['template_id']
        variables = serializer.validated_data['variables']

        try:
            # 简单的变量替换（实际应用中可能需要更复杂的模板引擎）
            rendered_content = template.content
            for key, value in variables.items():
                rendered_content = rendered_content.replace(f'{{{key}}}', str(value))

            # 增加使用次数
            template.increment_usage()

            return Response({
                'template_name': template.name,
                'rendered_content': rendered_content,
                'variables_used': variables
            })

        except Exception as e:
            return Response(
                {'error': f'模板渲染失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUsageStatsView(APIView):
    """用户使用统计"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取用户使用统计"""
        user = request.user
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timezone.timedelta(days=days)

        # 获取统计数据
        stats = AIUsageStats.objects.filter(
            user=user,
            date__range=[start_date, end_date]
        )

        # 聚合数据
        aggregated = stats.aggregate(
            total_requests=Sum('request_count'),
            total_tokens=Sum('token_count'),
            total_cost=Sum('total_cost'),
            total_success=Sum('success_count'),
            total_errors=Sum('error_count')
        )

        # 计算成功率
        total_requests = aggregated['total_requests'] or 0
        total_success = aggregated['total_success'] or 0
        success_rate = (total_success / total_requests * 100) if total_requests > 0 else 0

        # 获取最常用的模型
        most_used = stats.values('ai_model__name').annotate(
            total=Sum('request_count')
        ).order_by('-total').first()
        most_used_model = most_used['ai_model__name'] if most_used else '无'

        # 准备返回数据
        response_data = {
            'total_requests': total_requests,
            'total_tokens': aggregated['total_tokens'] or 0,
            'total_cost': aggregated['total_cost'] or Decimal('0.0000'),
            'total_success': total_success,
            'total_errors': aggregated['total_errors'] or 0,
            'success_rate': round(success_rate, 2),
            'most_used_model': most_used_model,
            'daily_stats': AIUsageStatsSerializer(stats, many=True).data
        }

        return Response(response_data)


class ModelUsageStatsView(APIView):
    """模型使用统计"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """获取模型使用统计"""
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timezone.timedelta(days=days)

        # 获取模型统计
        model_stats = AIUsageStats.objects.filter(
            date__range=[start_date, end_date]
        ).values('ai_model__name').annotate(
            total_requests=Sum('request_count'),
            total_tokens=Sum('token_count'),
            total_cost=Sum('total_cost'),
            unique_users=Count('user', distinct=True),
            total_success=Sum('success_count'),
            total_errors=Sum('error_count')
        ).order_by('-total_requests')

        # 计算成功率
        for stat in model_stats:
            total = stat['total_requests']
            success = stat['total_success']
            stat['success_rate'] = round((success / total * 100) if total > 0 else 0, 2)

        serializer = ModelUsageStatsSerializer(model_stats, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def chat_completion(request):
    """聊天完成接口（兼容OpenAI格式）"""
    serializer = ChatCompletionSerializer(data=request.data)
    if serializer.is_valid():
        model_name = serializer.validated_data['model']
        messages = serializer.validated_data['messages']

        try:
            # 获取AI模型
            ai_model = AIModel.objects.get(name=model_name, is_active=True)
            if not ai_model.is_available():
                return Response(
                    {'error': 'AI模型当前不可用'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

            # 创建请求记录
            ai_request = AIRequest.objects.create(
                user=request.user,
                ai_model=ai_model,
                request_type='text',
                input_data=serializer.validated_data,
                status='processing'
            )

            start_time = time.time()

            # 这里应该调用实际的AI模型API
            # 暂时返回模拟响应
            response_text = f"这是来自{model_name}的回复"
            tokens_used = 50

            processing_time = time.time() - start_time
            cost = ai_model.cost_per_request * tokens_used

            # 更新请求记录
            ai_request.mark_completed({
                'choices': [{
                    'message': {
                        'role': 'assistant',
                        'content': response_text
                    },
                    'finish_reason': 'stop'
                }],
                'usage': {
                    'total_tokens': tokens_used
                }
            }, processing_time)

            ai_request.cost = cost
            ai_request.save()

            # 记录使用统计
            AIUsageStats.record_usage(
                user=request.user,
                ai_model=ai_model,
                tokens=tokens_used,
                cost=cost,
                success=True
            )

            return Response({
                'id': f'chatcmpl-{ai_request.id}',
                'object': 'chat.completion',
                'created': int(ai_request.created_at.timestamp()),
                'model': model_name,
                'choices': [{
                    'index': 0,
                    'message': {
                        'role': 'assistant',
                        'content': response_text
                    },
                    'finish_reason': 'stop'
                }],
                'usage': {
                    'prompt_tokens': tokens_used // 2,
                    'completion_tokens': tokens_used // 2,
                    'total_tokens': tokens_used
                }
            })

        except AIModel.DoesNotExist:
            return Response(
                {'error': '指定的AI模型不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # 记录错误
            if 'ai_request' in locals():
                ai_request.mark_failed(str(e))

            # 记录失败统计
            AIUsageStats.record_usage(
                user=request.user,
                ai_model=ai_model if 'ai_model' in locals() else None,
                success=False
            )

            SystemLog.log(
                level='error',
                module='ai',
                action='chat_completion',
                message=f'聊天完成失败: {str(e)}',
                user=request.user,
                request=request,
                error=str(e)
            )

            return Response(
                {'error': f'处理请求失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def available_models(request):
    """获取可用的AI模型"""
    cache_key = 'available_ai_models'
    models = cache.get(cache_key)

    if not models:
        queryset = AIModel.objects.filter(
            status='active',
            is_active=True
        ).order_by('model_type', 'name')

        models = []
        for model in queryset:
            models.append({
                'id': model.id,
                'name': model.name,
                'type': model.model_type,
                'description': model.description,
                'version': model.version,
                'max_requests_per_minute': model.max_requests_per_minute
            })

        # 缓存5分钟
        cache.set(cache_key, models, 300)

    return Response(models)
