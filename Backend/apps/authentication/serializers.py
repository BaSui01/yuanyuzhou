from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import EmailVerificationToken, PasswordResetToken, APIKey

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # 支持用户名或邮箱登录
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    pass

            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('账户已被禁用')
                attrs['user'] = user
            else:
                raise serializers.ValidationError('用户名或密码错误')
        else:
            raise serializers.ValidationError('必须提供用户名和密码')

        return attrs


class RegisterSerializer(serializers.Serializer):
    """注册序列化器"""
    username = serializers.CharField(
        required=True,
        min_length=3,
        max_length=150
    )
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=30)
    phone = serializers.CharField(required=False, max_length=20)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('该用户名已被使用')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被使用')
        return value

    def validate_phone(self, value):
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已被使用')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('密码不匹配')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class EmailVerificationSerializer(serializers.Serializer):
    """邮箱验证序列化器"""
    token = serializers.CharField(required=True)

    def validate_token(self, value):
        try:
            token_obj = EmailVerificationToken.objects.get(token=value)
            if not token_obj.is_valid():
                raise serializers.ValidationError('验证令牌已过期或无效')
            return token_obj
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError('无效的验证令牌')


class ResendVerificationSerializer(serializers.Serializer):
    """重发验证邮件序列化器"""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.is_verified:
                raise serializers.ValidationError('该邮箱已经验证过了')
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError('该邮箱未注册')


class PasswordResetRequestSerializer(serializers.Serializer):
    """密码重置请求序列化器"""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value, is_active=True)
            return user
        except User.DoesNotExist:
            # 出于安全考虑，不透露邮箱是否存在
            return None


class PasswordResetConfirmSerializer(serializers.Serializer):
    """密码重置确认序列化器"""
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_token(self, value):
        try:
            token_obj = PasswordResetToken.objects.get(token=value)
            if not token_obj.is_valid():
                raise serializers.ValidationError('重置令牌已过期或无效')
            return token_obj
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError('无效的重置令牌')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('密码不匹配')
        return attrs


class LogoutSerializer(serializers.Serializer):
    """登出序列化器"""
    refresh_token = serializers.CharField(required=False)
    logout_all = serializers.BooleanField(required=False, default=False)


class TokenRefreshSerializer(serializers.Serializer):
    """令牌刷新序列化器"""
    refresh = serializers.CharField(required=True)


class APIKeySerializer(serializers.ModelSerializer):
    """API密钥序列化器"""
    key = serializers.CharField(read_only=True)

    class Meta:
        model = APIKey
        fields = [
            'id', 'name', 'key', 'is_active', 'permissions',
            'last_used', 'created_at', 'expires_at'
        ]
        read_only_fields = ['id', 'key', 'last_used', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return APIKey.generate_key(user=user, **validated_data)


class APIKeyCreateSerializer(serializers.Serializer):
    """API密钥创建序列化器"""
    name = serializers.CharField(required=True, max_length=100)
    permissions = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    expires_days = serializers.IntegerField(required=False, min_value=1, max_value=365)

    def validate_name(self, value):
        user = self.context['request'].user
        if APIKey.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError('该名称已被使用')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        return APIKey.generate_key(user=user, **validated_data)


class UserTokenSerializer(serializers.Serializer):
    """用户令牌序列化器"""
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        from apps.users.serializers import UserSerializer
        return UserSerializer(obj['user']).data


class SocialAuthSerializer(serializers.Serializer):
    """第三方登录序列化器"""
    provider = serializers.ChoiceField(choices=['google', 'github', 'wechat'])
    access_token = serializers.CharField(required=True)

    def validate(self, attrs):
        provider = attrs.get('provider')
        access_token = attrs.get('access_token')

        # 这里可以添加第三方token验证逻辑
        # 暂时只做基本验证
        if not access_token:
            raise serializers.ValidationError('access_token is required')

        return attrs


class TwoFactorAuthSerializer(serializers.Serializer):
    """双因子认证序列化器"""
    code = serializers.CharField(required=True, min_length=6, max_length=8)
    backup_code = serializers.CharField(required=False)

    def validate(self, attrs):
        code = attrs.get('code')
        backup_code = attrs.get('backup_code')

        if not code and not backup_code:
            raise serializers.ValidationError('必须提供验证码或备用代码')

        return attrs


class ChangeEmailSerializer(serializers.Serializer):
    """修改邮箱序列化器"""
    new_email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_new_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被使用')
        return value

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('密码不正确')
        return value


class AccountDeactivateSerializer(serializers.Serializer):
    """账户停用序列化器"""
    password = serializers.CharField(required=True, write_only=True)
    confirmation = serializers.CharField(required=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('密码不正确')
        return value

    def validate_confirmation(self, value):
        if value.lower() != 'delete':
            raise serializers.ValidationError('请输入 "delete" 确认删除')
        return value
