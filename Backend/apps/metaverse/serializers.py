from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    VirtualWorld, Avatar, UserSession, VirtualObject,
    WorldObject, Event, EventParticipant, WorldPermission
)

User = get_user_model()


class VirtualWorldListSerializer(serializers.ModelSerializer):
    """虚拟世界列表序列化器"""
    creator_name = serializers.CharField(source='creator.username', read_only=True)
    current_users_count = serializers.ReadOnlyField()

    class Meta:
        model = VirtualWorld
        fields = [
            'id', 'name', 'description', 'world_type', 'creator', 'creator_name',
            'thumbnail', 'max_capacity', 'status', 'visit_count',
            'current_users_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['creator', 'visit_count', 'created_at', 'updated_at']


class VirtualWorldSerializer(serializers.ModelSerializer):
    """虚拟世界详情序列化器"""
    creator_name = serializers.CharField(source='creator.username', read_only=True)
    current_users_count = serializers.ReadOnlyField()
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = VirtualWorld
        fields = [
            'id', 'name', 'description', 'world_type', 'creator', 'creator_name',
            'thumbnail', 'scene_data', 'max_capacity', 'status', 'visit_count',
            'tags', 'settings', 'current_users_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['creator', 'visit_count', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class AvatarSerializer(serializers.ModelSerializer):
    """虚拟形象序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Avatar
        fields = [
            'id', 'user', 'user_name', 'name', 'avatar_type', 'model_data',
            'appearance_data', 'animations', 'thumbnail', 'is_default',
            'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserSessionSerializer(serializers.ModelSerializer):
    """用户会话序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    world_name = serializers.CharField(source='world.name', read_only=True)
    avatar_name = serializers.CharField(source='avatar.name', read_only=True)

    class Meta:
        model = UserSession
        fields = [
            'id', 'user', 'user_name', 'world', 'world_name', 'avatar', 'avatar_name',
            'session_id', 'status', 'position', 'last_seen', 'duration',
            'device_info', 'created_at'
        ]
        read_only_fields = ['user', 'session_id', 'duration', 'created_at']


class VirtualObjectSerializer(serializers.ModelSerializer):
    """虚拟物品序列化器"""
    creator_name = serializers.CharField(source='creator.username', read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = VirtualObject
        fields = [
            'id', 'name', 'description', 'object_type', 'creator', 'creator_name',
            'model_data', 'physics_data', 'interaction_data', 'thumbnail',
            'is_public', 'download_count', 'rating', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['creator', 'download_count', 'rating', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class WorldObjectSerializer(serializers.ModelSerializer):
    """世界物品实例序列化器"""
    virtual_object_name = serializers.CharField(source='virtual_object.name', read_only=True)
    world_name = serializers.CharField(source='world.name', read_only=True)
    placed_by_name = serializers.CharField(source='placed_by.username', read_only=True)

    class Meta:
        model = WorldObject
        fields = [
            'id', 'world', 'world_name', 'virtual_object', 'virtual_object_name',
            'position', 'rotation', 'scale', 'properties', 'placed_by', 'placed_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['placed_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['placed_by'] = self.context['request'].user
        return super().create(validated_data)


class EventParticipantSerializer(serializers.ModelSerializer):
    """活动参与者序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = EventParticipant
        fields = [
            'id', 'user', 'user_name', 'status', 'registered_at', 'attended_at'
        ]
        read_only_fields = ['registered_at', 'attended_at']


class EventListSerializer(serializers.ModelSerializer):
    """活动列表序列化器"""
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    world_name = serializers.CharField(source='world.name', read_only=True)
    participant_count = serializers.SerializerMethodField()
    is_ongoing = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type', 'organizer', 'organizer_name',
            'world', 'world_name', 'start_time', 'end_time', 'status',
            'max_participants', 'is_public', 'registration_required',
            'participant_count', 'is_ongoing', 'created_at'
        ]
        read_only_fields = ['organizer', 'created_at']

    def get_participant_count(self, obj):
        return obj.participants.count()


class EventSerializer(serializers.ModelSerializer):
    """活动详情序列化器"""
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    world_name = serializers.CharField(source='world.name', read_only=True)
    participants = EventParticipantSerializer(
        source='eventparticipant_set',
        many=True,
        read_only=True
    )
    participant_count = serializers.SerializerMethodField()
    is_ongoing = serializers.ReadOnlyField()
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type', 'organizer', 'organizer_name',
            'world', 'world_name', 'start_time', 'end_time', 'status',
            'max_participants', 'is_public', 'registration_required',
            'participants', 'participant_count', 'is_ongoing', 'tags',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['organizer', 'created_at', 'updated_at']

    def get_participant_count(self, obj):
        return obj.participants.count()

    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)


class WorldPermissionSerializer(serializers.ModelSerializer):
    """世界权限序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    world_name = serializers.CharField(source='world.name', read_only=True)
    granted_by_name = serializers.CharField(source='granted_by.username', read_only=True)

    class Meta:
        model = WorldPermission
        fields = [
            'id', 'world', 'world_name', 'user', 'user_name', 'permission_type',
            'granted_by', 'granted_by_name', 'created_at'
        ]
        read_only_fields = ['granted_by', 'created_at']

    def create(self, validated_data):
        validated_data['granted_by'] = self.context['request'].user
        return super().create(validated_data)


class EnterWorldSerializer(serializers.Serializer):
    """进入世界序列化器"""
    avatar_id = serializers.IntegerField()
    position = serializers.JSONField(required=False, default=dict)
    device_info = serializers.JSONField(required=False, default=dict)

    def validate_avatar_id(self, value):
        try:
            avatar = Avatar.objects.get(
                id=value,
                user=self.context['request'].user,
                is_active=True
            )
            return value
        except Avatar.DoesNotExist:
            raise serializers.ValidationError("指定的虚拟形象不存在或不属于当前用户")


class UpdatePositionSerializer(serializers.Serializer):
    """更新位置序列化器"""
    position = serializers.JSONField()
    rotation = serializers.JSONField(required=False)

    def validate_position(self, value):
        required_fields = ['x', 'y', 'z']
        if not all(field in value for field in required_fields):
            raise serializers.ValidationError("位置信息必须包含 x, y, z 坐标")
        return value


class WorldStatsSerializer(serializers.Serializer):
    """世界统计序列化器"""
    world_id = serializers.IntegerField()
    world_name = serializers.CharField()
    total_visits = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    current_users = serializers.IntegerField()
    average_session_duration = serializers.FloatField()
    peak_concurrent_users = serializers.IntegerField()


class UserActivityStatsSerializer(serializers.Serializer):
    """用户活动统计序列化器"""
    total_time_spent = serializers.IntegerField()
    worlds_visited = serializers.IntegerField()
    events_attended = serializers.IntegerField()
    objects_created = serializers.IntegerField()
    avatars_created = serializers.IntegerField()
    favorite_world = serializers.CharField()
    most_used_avatar = serializers.CharField()
