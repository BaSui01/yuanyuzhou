from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User, UserProfile, UserLoginLog


class UserProfileSerializer(serializers.ModelSerializer):
    """用户档案序列化器"""

    class Meta:
        model = UserProfile
        fields = [
            'language', 'timezone', 'theme',
            'email_notifications', 'sms_notifications', 'push_notifications',
            'login_count', 'points', 'level'
        ]
        read_only_fields = ['login_count', 'points', 'level']


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'avatar', 'avatar_url', 'birth_date', 'gender', 'bio',
            'country', 'city', 'website', 'github',
            'is_verified', 'is_premium', 'is_active',
            'date_joined', 'last_active', 'profile'
        ]
        read_only_fields = [
            'id', 'is_verified', 'is_premium', 'is_active',
            'date_joined', 'last_active'
        ]
        extra_kwargs = {
            'email': {'required': True},
        }

    def get_avatar_url(self, obj):
        """获取头像URL"""
        return obj.get_avatar_url()

    def validate_email(self, value):
        """验证邮箱唯一性"""
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("该邮箱已被使用")
        return value

    def validate_phone(self, value):
        """验证手机号唯一性"""
        if value and User.objects.filter(phone=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("该手机号已被使用")
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate(self, attrs):
        """验证密码确认"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密码不匹配")
        return attrs

    def validate_email(self, value):
        """验证邮箱唯一性"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被使用")
        return value

    def validate_username(self, value):
        """验证用户名唯一性"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被使用")
        return value

    def validate_phone(self, value):
        """验证手机号唯一性"""
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("该手机号已被使用")
        return value

    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # 创建用户档案
        UserProfile.objects.create(user=user)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'avatar',
            'birth_date', 'gender', 'bio', 'country', 'city',
            'website', 'github'
        ]

    def validate_phone(self, value):
        """验证手机号唯一性"""
        if value and User.objects.filter(phone=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("该手机号已被使用")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """密码修改序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, value):
        """验证旧密码"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("旧密码不正确")
        return value

    def validate(self, attrs):
        """验证新密码确认"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("新密码不匹配")
        return attrs

    def save(self):
        """保存新密码"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserLoginLogSerializer(serializers.ModelSerializer):
    """登录日志序列化器"""
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserLoginLog
        fields = [
            'id', 'user', 'user_username', 'ip_address',
            'user_agent', 'location', 'device_type',
            'login_time', 'is_successful'
        ]
        read_only_fields = ['id', 'login_time']


class UserListSerializer(serializers.ModelSerializer):
    """用户列表序列化器（简化版本）"""
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'avatar_url', 'is_verified', 'is_premium',
            'date_joined', 'last_active'
        ]

    def get_avatar_url(self, obj):
        """获取头像URL"""
        return obj.get_avatar_url()


class UserSearchSerializer(serializers.ModelSerializer):
    """用户搜索序列化器"""
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'avatar_url', 'bio', 'city', 'is_verified'
        ]

    def get_avatar_url(self, obj):
        """获取头像URL"""
        return obj.get_avatar_url()
