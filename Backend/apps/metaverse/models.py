from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel

User = get_user_model()


class VirtualWorld(BaseModel):
    """虚拟世界"""
    WORLD_TYPES = [
        ('public', '公共世界'),
        ('private', '私人世界'),
        ('group', '群组世界'),
        ('event', '活动世界'),
    ]

    STATUS_CHOICES = [
        ('active', '活跃'),
        ('inactive', '非活跃'),
        ('maintenance', '维护中'),
        ('archived', '已归档'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name='世界名称'
    )
    description = models.TextField(
        verbose_name='世界描述'
    )
    world_type = models.CharField(
        max_length=20,
        choices=WORLD_TYPES,
        default='public',
        verbose_name='世界类型'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_worlds',
        verbose_name='创建者'
    )
    thumbnail = models.ImageField(
        upload_to='worlds/thumbnails/',
        null=True,
        blank=True,
        verbose_name='缩略图'
    )
    scene_data = models.JSONField(
        default=dict,
        verbose_name='场景数据'
    )
    max_capacity = models.PositiveIntegerField(
        default=50,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        verbose_name='最大容量'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='状态'
    )
    visit_count = models.PositiveIntegerField(
        default=0,
        verbose_name='访问次数'
    )
    tags = models.ManyToManyField(
        'core.Tag',
        blank=True,
        verbose_name='标签'
    )
    settings = models.JSONField(
        default=dict,
        verbose_name='世界设置'
    )

    class Meta:
        verbose_name = '虚拟世界'
        verbose_name_plural = '虚拟世界'
        db_table = 'metaverse_worlds'
        ordering = ['-visit_count', '-created_at']

    def __str__(self):
        return self.name

    def increment_visit_count(self):
        """增加访问次数"""
        self.visit_count += 1
        self.save(update_fields=['visit_count'])

    @property
    def current_users_count(self):
        """当前在线用户数"""
        return self.user_sessions.filter(
            is_active=True,
            last_seen__gte=timezone.now() - timezone.timedelta(minutes=5)
        ).count()

    def is_accessible_by(self, user):
        """检查用户是否可以访问"""
        if self.world_type == 'public':
            return True
        elif self.world_type == 'private':
            return user == self.creator or self.permissions.filter(user=user).exists()
        elif self.world_type == 'group':
            # 这里可以添加群组权限检查
            return True
        return False


class Avatar(BaseModel):
    """虚拟形象"""
    AVATAR_TYPES = [
        ('human', '人类'),
        ('anime', '动漫'),
        ('robot', '机器人'),
        ('animal', '动物'),
        ('fantasy', '幻想'),
        ('custom', '自定义'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='avatars',
        verbose_name='用户'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='形象名称'
    )
    avatar_type = models.CharField(
        max_length=20,
        choices=AVATAR_TYPES,
        default='human',
        verbose_name='形象类型'
    )
    model_data = models.JSONField(
        default=dict,
        verbose_name='模型数据'
    )
    appearance_data = models.JSONField(
        default=dict,
        verbose_name='外观数据'
    )
    animations = models.JSONField(
        default=list,
        verbose_name='动画数据'
    )
    thumbnail = models.ImageField(
        upload_to='avatars/thumbnails/',
        null=True,
        blank=True,
        verbose_name='缩略图'
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='默认形象'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='公开形象'
    )

    class Meta:
        verbose_name = '虚拟形象'
        verbose_name_plural = '虚拟形象'
        db_table = 'metaverse_avatars'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    def set_as_default(self):
        """设置为默认形象"""
        # 取消其他默认形象
        Avatar.objects.filter(user=self.user, is_default=True).update(is_default=False)
        self.is_default = True
        self.save(update_fields=['is_default'])


class UserSession(BaseModel):
    """用户会话"""
    SESSION_STATUS = [
        ('connecting', '连接中'),
        ('active', '活跃'),
        ('idle', '空闲'),
        ('disconnected', '已断开'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='metaverse_sessions',
        verbose_name='用户'
    )
    world = models.ForeignKey(
        VirtualWorld,
        on_delete=models.CASCADE,
        related_name='user_sessions',
        verbose_name='虚拟世界'
    )
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='使用的形象'
    )
    session_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='会话ID'
    )
    status = models.CharField(
        max_length=20,
        choices=SESSION_STATUS,
        default='connecting',
        verbose_name='会话状态'
    )
    position = models.JSONField(
        default=dict,
        verbose_name='位置信息'
    )
    last_seen = models.DateTimeField(
        auto_now=True,
        verbose_name='最后活跃时间'
    )
    duration = models.PositiveIntegerField(
        default=0,
        verbose_name='会话时长(秒)'
    )
    device_info = models.JSONField(
        default=dict,
        verbose_name='设备信息'
    )

    class Meta:
        verbose_name = '用户会话'
        verbose_name_plural = '用户会话'
        db_table = 'metaverse_user_sessions'
        ordering = ['-last_seen']

    def __str__(self):
        return f"{self.user.username} in {self.world.name}"

    def update_activity(self, position=None):
        """更新活动状态"""
        self.last_seen = timezone.now()
        if position:
            self.position = position
        self.save(update_fields=['last_seen', 'position'])

    def disconnect(self):
        """断开连接"""
        self.status = 'disconnected'
        self.is_active = False
        # 计算会话时长
        if self.created_at:
            self.duration = int((timezone.now() - self.created_at).total_seconds())
        self.save(update_fields=['status', 'is_active', 'duration'])


class VirtualObject(BaseModel):
    """虚拟物品"""
    OBJECT_TYPES = [
        ('furniture', '家具'),
        ('decoration', '装饰'),
        ('interactive', '交互物品'),
        ('vehicle', '载具'),
        ('tool', '工具'),
        ('game', '游戏物品'),
        ('media', '媒体'),
        ('other', '其他'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name='物品名称'
    )
    description = models.TextField(
        blank=True,
        verbose_name='物品描述'
    )
    object_type = models.CharField(
        max_length=20,
        choices=OBJECT_TYPES,
        verbose_name='物品类型'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_objects',
        verbose_name='创建者'
    )
    model_data = models.JSONField(
        default=dict,
        verbose_name='模型数据'
    )
    physics_data = models.JSONField(
        default=dict,
        verbose_name='物理数据'
    )
    interaction_data = models.JSONField(
        default=dict,
        verbose_name='交互数据'
    )
    thumbnail = models.ImageField(
        upload_to='objects/thumbnails/',
        null=True,
        blank=True,
        verbose_name='缩略图'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='公开物品'
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name='下载次数'
    )
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name='评分'
    )
    tags = models.ManyToManyField(
        'core.Tag',
        blank=True,
        verbose_name='标签'
    )

    class Meta:
        verbose_name = '虚拟物品'
        verbose_name_plural = '虚拟物品'
        db_table = 'metaverse_objects'
        ordering = ['-rating', '-download_count']

    def __str__(self):
        return self.name

    def increment_download_count(self):
        """增加下载次数"""
        self.download_count += 1
        self.save(update_fields=['download_count'])


class WorldObject(BaseModel):
    """世界物品实例"""
    world = models.ForeignKey(
        VirtualWorld,
        on_delete=models.CASCADE,
        related_name='world_objects',
        verbose_name='虚拟世界'
    )
    virtual_object = models.ForeignKey(
        VirtualObject,
        on_delete=models.CASCADE,
        related_name='instances',
        verbose_name='虚拟物品'
    )
    position = models.JSONField(
        default=dict,
        verbose_name='位置信息'
    )
    rotation = models.JSONField(
        default=dict,
        verbose_name='旋转信息'
    )
    scale = models.JSONField(
        default=dict,
        verbose_name='缩放信息'
    )
    properties = models.JSONField(
        default=dict,
        verbose_name='自定义属性'
    )
    placed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='放置者'
    )

    class Meta:
        verbose_name = '世界物品实例'
        verbose_name_plural = '世界物品实例'
        db_table = 'metaverse_world_objects'
        ordering = ['world', '-created_at']

    def __str__(self):
        return f"{self.virtual_object.name} in {self.world.name}"


class Event(BaseModel):
    """元宇宙活动"""
    EVENT_TYPES = [
        ('meeting', '会议'),
        ('party', '聚会'),
        ('concert', '音乐会'),
        ('exhibition', '展览'),
        ('game', '游戏'),
        ('education', '教育'),
        ('other', '其他'),
    ]

    STATUS_CHOICES = [
        ('scheduled', '已安排'),
        ('ongoing', '进行中'),
        ('ended', '已结束'),
        ('cancelled', '已取消'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='活动标题'
    )
    description = models.TextField(
        verbose_name='活动描述'
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        verbose_name='活动类型'
    )
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_events',
        verbose_name='组织者'
    )
    world = models.ForeignKey(
        VirtualWorld,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='举办世界'
    )
    start_time = models.DateTimeField(
        verbose_name='开始时间'
    )
    end_time = models.DateTimeField(
        verbose_name='结束时间'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name='活动状态'
    )
    max_participants = models.PositiveIntegerField(
        default=100,
        verbose_name='最大参与人数'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='公开活动'
    )
    registration_required = models.BooleanField(
        default=False,
        verbose_name='需要注册'
    )
    participants = models.ManyToManyField(
        User,
        through='EventParticipant',
        verbose_name='参与者'
    )
    tags = models.ManyToManyField(
        'core.Tag',
        blank=True,
        verbose_name='标签'
    )

    class Meta:
        verbose_name = '元宇宙活动'
        verbose_name_plural = '元宇宙活动'
        db_table = 'metaverse_events'
        ordering = ['start_time']

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        """检查活动是否正在进行"""
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def can_join(self, user):
        """检查用户是否可以参加"""
        if not self.is_public and not self.participants.filter(id=user.id).exists():
            return False
        if self.participants.count() >= self.max_participants:
            return False
        return True


class EventParticipant(BaseModel):
    """活动参与者"""
    PARTICIPATION_STATUS = [
        ('registered', '已注册'),
        ('attended', '已参加'),
        ('cancelled', '已取消'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name='活动'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    status = models.CharField(
        max_length=20,
        choices=PARTICIPATION_STATUS,
        default='registered',
        verbose_name='参与状态'
    )
    registered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='注册时间'
    )
    attended_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='参加时间'
    )

    class Meta:
        verbose_name = '活动参与者'
        verbose_name_plural = '活动参与者'
        db_table = 'metaverse_event_participants'
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    def mark_attended(self):
        """标记为已参加"""
        self.status = 'attended'
        self.attended_at = timezone.now()
        self.save(update_fields=['status', 'attended_at'])


class WorldPermission(BaseModel):
    """世界权限"""
    PERMISSION_TYPES = [
        ('view', '查看'),
        ('edit', '编辑'),
        ('admin', '管理'),
    ]

    world = models.ForeignKey(
        VirtualWorld,
        on_delete=models.CASCADE,
        related_name='permissions',
        verbose_name='虚拟世界'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    permission_type = models.CharField(
        max_length=20,
        choices=PERMISSION_TYPES,
        verbose_name='权限类型'
    )
    granted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='granted_permissions',
        verbose_name='授权者'
    )

    class Meta:
        verbose_name = '世界权限'
        verbose_name_plural = '世界权限'
        db_table = 'metaverse_world_permissions'
        unique_together = ['world', 'user', 'permission_type']

    def __str__(self):
        return f"{self.user.username} - {self.world.name} ({self.permission_type})"
