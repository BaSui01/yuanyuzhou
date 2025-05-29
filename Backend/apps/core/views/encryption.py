"""
加密相关视图
处理会话创建、密钥交换等功能
"""

import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..middleware.encryption import TransportEncryptionService, ApplicationCryptoUtils

logger = logging.getLogger(__name__)


class EncryptionSessionView(View):
    """传输层加密会话管理视图"""

    def __init__(self):
        super().__init__()
        self.transport_service = TransportEncryptionService()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """创建新的加密会话"""
        try:
            # 解析请求数据
            data = json.loads(request.body.decode())
            client_id = data.get('client_id')
            client_public_key = data.get('client_public_key')

            if not client_id:
                return JsonResponse({
                    'error': 'MISSING_CLIENT_ID',
                    'message': '缺少客户端ID'
                }, status=400)

            # 生成会话密钥
            session_info = self.transport_service.generate_session_key(client_id)

            logger.info(f"[加密会话] 新会话已创建 - 客户端: {client_id}, 会话: {session_info['session_id'][:8]}...")

            return JsonResponse({
                'success': True,
                'session_id': session_info['session_id'],
                'server_public_key': session_info['server_public_key'],
                'expires_at': session_info['expires_at'],
                'key_hash': session_info['key_hash']
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'INVALID_JSON',
                'message': '无效的JSON格式'
            }, status=400)
        except Exception as e:
            logger.error(f"会话创建失败: {e}")
            return JsonResponse({
                'error': 'SESSION_CREATION_FAILED',
                'message': '会话创建失败'
            }, status=500)

    def delete(self, request, session_id):
        """撤销加密会话"""
        try:
            self.transport_service.revoke_session(session_id)

            logger.info(f"[加密会话] 会话已撤销 - 会话: {session_id[:8]}...")

            return JsonResponse({
                'success': True,
                'message': '会话已撤销'
            })

        except Exception as e:
            logger.error(f"会话撤销失败: {e}")
            return JsonResponse({
                'error': 'SESSION_REVOCATION_FAILED',
                'message': '会话撤销失败'
            }, status=500)

    def get(self, request, session_id):
        """获取会话状态"""
        try:
            session_info = self.transport_service.get_session_info(session_id)

            if not session_info:
                return JsonResponse({
                    'error': 'SESSION_NOT_FOUND',
                    'message': '会话不存在或已过期'
                }, status=404)

            return JsonResponse({
                'success': True,
                'session_id': session_id,
                'client_id': session_info['client_id'],
                'created_at': session_info['created_at'],
                'expires_at': session_info['expires_at'],
                'valid': True
            })

        except Exception as e:
            logger.error(f"获取会话状态失败: {e}")
            return JsonResponse({
                'error': 'SESSION_STATUS_FAILED',
                'message': '获取会话状态失败'
            }, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_encryption_session(request):
    """
    创建传输层加密会话
    API端点版本
    """
    try:
        client_id = request.data.get('client_id')
        client_public_key = request.data.get('client_public_key')

        if not client_id:
            return Response({
                'error': 'MISSING_CLIENT_ID',
                'message': '缺少客户端ID'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 创建传输服务实例
        transport_service = TransportEncryptionService()

        # 生成会话密钥
        session_info = transport_service.generate_session_key(client_id)

        logger.info(f"[API加密会话] 新会话已创建 - 客户端: {client_id}")

        return Response({
            'success': True,
            'data': {
                'session_id': session_info['session_id'],
                'server_public_key': session_info['server_public_key'],
                'expires_at': session_info['expires_at'],
                'key_hash': session_info['key_hash']
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"API会话创建失败: {e}")
        return Response({
            'error': 'SESSION_CREATION_FAILED',
            'message': '会话创建失败',
            'details': str(e) if request.user.is_staff else None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def revoke_encryption_session(request, session_id):
    """
    撤销传输层加密会话
    API端点版本
    """
    try:
        transport_service = TransportEncryptionService()
        transport_service.revoke_session(session_id)

        logger.info(f"[API加密会话] 会话已撤销 - 会话: {session_id[:8]}...")

        return Response({
            'success': True,
            'message': '会话已撤销'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"API会话撤销失败: {e}")
        return Response({
            'error': 'SESSION_REVOCATION_FAILED',
            'message': '会话撤销失败'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_session_status(request, session_id):
    """
    获取会话状态
    API端点版本
    """
    try:
        transport_service = TransportEncryptionService()
        session_info = transport_service.get_session_info(session_id)

        if not session_info:
            return Response({
                'error': 'SESSION_NOT_FOUND',
                'message': '会话不存在或已过期'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success': True,
            'data': {
                'session_id': session_id,
                'client_id': session_info['client_id'],
                'created_at': session_info['created_at'],
                'expires_at': session_info['expires_at'],
                'valid': True
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"获取API会话状态失败: {e}")
        return Response({
            'error': 'SESSION_STATUS_FAILED',
            'message': '获取会话状态失败'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def test_encryption(request):
    """
    测试加密/解密功能
    开发和调试用途
    """
    try:
        data = request.data.get('data')
        encrypt_level = request.data.get('level', 1)

        if not data:
            return Response({
                'error': 'MISSING_DATA',
                'message': '缺少测试数据'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 创建应用层加密工具
        app_crypto = ApplicationCryptoUtils()

        # 加密数据
        encrypted_data = app_crypto.encrypt(data, encrypt_level)

        # 解密数据
        decrypted_data = app_crypto.decrypt(encrypted_data, encrypt_level)

        return Response({
            'success': True,
            'data': {
                'original': data,
                'encrypted': encrypted_data,
                'decrypted': decrypted_data,
                'level': encrypt_level,
                'match': data == decrypted_data
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"加密测试失败: {e}")
        return Response({
            'error': 'ENCRYPTION_TEST_FAILED',
            'message': '加密测试失败',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def encryption_health_check(request):
    """
    加密服务健康检查
    """
    try:
        # 测试传输层加密服务
        transport_service = TransportEncryptionService()
        test_session = transport_service.generate_session_key('health_check_client')

        # 测试应用层加密
        app_crypto = ApplicationCryptoUtils()
        test_data = {'test': 'health_check_data'}
        encrypted = app_crypto.encrypt(test_data, 1)
        decrypted = app_crypto.decrypt(encrypted, 1)

        # 清理测试会话
        transport_service.revoke_session(test_session['session_id'])

        health_status = {
            'transport_encryption': 'healthy',
            'application_encryption': 'healthy',
            'data_integrity': test_data == decrypted
        }

        all_healthy = all([
            health_status['transport_encryption'] == 'healthy',
            health_status['application_encryption'] == 'healthy',
            health_status['data_integrity']
        ])

        return Response({
            'success': True,
            'status': 'healthy' if all_healthy else 'degraded',
            'services': health_status,
            'timestamp': int(time.time())
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"加密服务健康检查失败: {e}")
        return Response({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': int(time.time())
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class EncryptionStatsView(View):
    """加密统计视图"""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """获取加密服务统计信息"""
        try:
            from django.core.cache import cache
            from django.conf import settings

            # 获取缓存统计
            cache_stats = {
                'active_sessions': 0,
                'used_nonces': 0
            }

            # 计算活跃会话数
            session_prefix = 'transport_session:'
            if hasattr(cache, '_cache') and hasattr(cache._cache, 'keys'):
                # Redis后端
                try:
                    session_keys = cache._cache.keys(f"{session_prefix}*")
                    cache_stats['active_sessions'] = len(session_keys) if session_keys else 0
                except:
                    pass

            # 计算使用的nonce数
            nonce_prefix = 'transport_nonce:'
            if hasattr(cache, '_cache') and hasattr(cache._cache, 'keys'):
                try:
                    nonce_keys = cache._cache.keys(f"{nonce_prefix}*")
                    cache_stats['used_nonces'] = len(nonce_keys) if nonce_keys else 0
                except:
                    pass

            # 配置信息
            config_info = {
                'session_ttl': getattr(settings, 'SESSION_KEY_TTL', 300),
                'time_window': getattr(settings, 'TIME_WINDOW', 30),
                'anti_replay': getattr(settings, 'ANTI_REPLAY', True),
                'integrity_check': getattr(settings, 'INTEGRITY_CHECK', True),
            }

            return JsonResponse({
                'success': True,
                'data': {
                    'cache_stats': cache_stats,
                    'config': config_info,
                    'timestamp': int(time.time())
                }
            })

        except Exception as e:
            logger.error(f"获取加密统计失败: {e}")
            return JsonResponse({
                'error': 'STATS_FETCH_FAILED',
                'message': '获取加密统计失败'
            }, status=500)


# 导入time模块
import time
