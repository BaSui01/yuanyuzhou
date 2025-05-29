from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction

from .models import (
    EmailVerificationToken, PasswordResetToken,
    LoginAttempt, APIKey, TwoFactorAuth
)
from .serializers import (
    LoginSerializer, RegisterSerializer, EmailVerificationSerializer,
    ResendVerificationSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, LogoutSerializer,
    APIKeyCreateSerializer, APIKeySerializer, TwoFactorAuthSerializer,
    ChangeEmailSerializer, AccountDeactivateSerializer
)
from apps.users.serializers import UserSerializer

User = get_user_model()


class LoginView(APIView):
    """用户登录视图"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """用户登录"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            remember_me = serializer.validated_data.get('remember_me', False)

            # 记录成功登录
            LoginAttempt.record_attempt(
                username=user.username,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                is_successful=True
            )

            # 创建或获取token
            token, created = Token.objects.get_or_create(user=user)

            # 设置session过期时间
            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)

            # 登录用户
            login(request, user)

            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'message': '登录成功'
            })

        # 记录失败登录
        username = request.data.get('username', '')
        LoginAttempt.record_attempt(
            username=username,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            is_successful=False,
            failure_reason='Invalid credentials'
        )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RegisterView(APIView):
    """用户注册视图"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """用户注册"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()

                # 生成邮箱验证令牌
                token = EmailVerificationToken.generate_token(user)

                # 发送验证邮件
                self.send_verification_email(user, token)

                return Response({
                    'user': UserSerializer(user).data,
                    'message': '注册成功，请查收验证邮件'
                }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_email(self, user, token):
        """发送验证邮件"""
        subject = '验证您的邮箱'
        message = f'请点击以下链接验证您的邮箱: {settings.FRONTEND_URL}/verify-email/{token.token}'
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            # 记录邮件发送错误，但不影响注册流程
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send verification email: {e}")


class LogoutView(APIView):
    """用户登出视图"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """用户登出"""
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            logout_all = serializer.validated_data.get('logout_all', False)

            if logout_all:
                # 删除用户所有token
                Token.objects.filter(user=request.user).delete()
            else:
                # 只删除当前token
                try:
                    token = Token.objects.get(user=request.user)
                    token.delete()
                except Token.DoesNotExist:
                    pass

            # Django session登出
            logout(request)

            return Response({'message': '登出成功'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """邮箱验证视图"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """验证邮箱"""
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            token_obj = serializer.validated_data['token']
            user = token_obj.user

            # 标记用户为已验证
            user.is_verified = True
            user.save(update_fields=['is_verified'])

            # 标记token为已使用
            token_obj.mark_as_used()

            return Response({'message': '邮箱验证成功'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationView(APIView):
    """重发验证邮件视图"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """重发验证邮件"""
        serializer = ResendVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['email']

            # 生成新的验证令牌
            token = EmailVerificationToken.generate_token(user)

            # 发送验证邮件
            self.send_verification_email(user, token)

            return Response({'message': '验证邮件已重新发送'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_email(self, user, token):
        """发送验证邮件"""
        subject = '验证您的邮箱'
        message = f'请点击以下链接验证您的邮箱: {settings.FRONTEND_URL}/verify-email/{token.token}'
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send verification email: {e}")


class PasswordResetRequestView(APIView):
    """密码重置请求视图"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """请求密码重置"""
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['email']

            if user:
                # 生成重置令牌
                ip_address = self.get_client_ip(request)
                token = PasswordResetToken.generate_token(user, ip_address)

                # 发送重置邮件
                self.send_reset_email(user, token)

            # 无论邮箱是否存在都返回相同消息，出于安全考虑
            return Response({'message': '如果邮箱存在，重置链接已发送'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_reset_email(self, user, token):
        """发送密码重置邮件"""
        subject = '密码重置'
        message = f'请点击以下链接重置您的密码: {settings.FRONTEND_URL}/reset-password/{token.token}'
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send reset email: {e}")

    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class PasswordResetConfirmView(APIView):
    """密码重置确认视图"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """确认密码重置"""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token_obj = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            user = token_obj.user
            user.set_password(new_password)
            user.save()

            # 标记token为已使用
            token_obj.mark_as_used()

            # 删除用户所有token，强制重新登录
            Token.objects.filter(user=user).delete()

            return Response({'message': '密码重置成功，请重新登录'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIKeyListCreateView(APIView):
    """API密钥列表和创建视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取用户的API密钥列表"""
        api_keys = APIKey.objects.filter(user=request.user)
        serializer = APIKeySerializer(api_keys, many=True)
        return Response(serializer.data)

    def post(self, request):
        """创建新的API密钥"""
        serializer = APIKeyCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            api_key = serializer.save()
            return Response(APIKeySerializer(api_key).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIKeyDetailView(APIView):
    """API密钥详情视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, pk):
        """获取API密钥对象"""
        try:
            return APIKey.objects.get(pk=pk, user=request.user)
        except APIKey.DoesNotExist:
            return None

    def get(self, request, pk):
        """获取API密钥详情"""
        api_key = self.get_object(request, pk)
        if not api_key:
            return Response({'error': 'API密钥不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = APIKeySerializer(api_key)
        return Response(serializer.data)

    def put(self, request, pk):
        """更新API密钥"""
        api_key = self.get_object(request, pk)
        if not api_key:
            return Response({'error': 'API密钥不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = APIKeySerializer(api_key, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """删除API密钥"""
        api_key = self.get_object(request, pk)
        if not api_key:
            return Response({'error': 'API密钥不存在'}, status=status.HTTP_404_NOT_FOUND)

        api_key.delete()
        return Response({'message': 'API密钥已删除'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_email(request):
    """修改邮箱"""
    serializer = ChangeEmailSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        new_email = serializer.validated_data['new_email']

        # 生成邮箱验证令牌
        user = request.user
        user.email = new_email
        user.is_verified = False  # 重置验证状态
        user.save()

        token = EmailVerificationToken.generate_token(user)

        # 发送验证邮件到新邮箱
        subject = '验证新邮箱'
        message = f'请点击以下链接验证您的新邮箱: {settings.FRONTEND_URL}/verify-email/{token.token}'
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [new_email],
                fail_silently=False,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send verification email: {e}")

        return Response({'message': '邮箱已更新，请验证新邮箱'})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def deactivate_account(request):
    """停用账户"""
    serializer = AccountDeactivateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.is_active = False
        user.save()

        # 删除所有token
        Token.objects.filter(user=user).delete()

        # 登出
        logout(request)

        return Response({'message': '账户已停用'})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthStatusView(APIView):
    """认证状态视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取当前认证状态"""
        user = request.user
        return Response({
            'user': UserSerializer(user).data,
            'is_authenticated': True,
            'has_token': Token.objects.filter(user=user).exists(),
        })
