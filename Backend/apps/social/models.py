from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinLengthValidator
from apps.core.models import BaseModel

User = get_user_model()


class Friendship(BaseModel):
    """好友关系"""
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('accepted', '已接受'),
        ('blocked', '已屏蔽'),
    ]

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_friendships',
        verbose_name='发起者'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_friendships',
        verbose_name='接收者'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='接受时间'
    )

    class Meta:
        verbose_name = '好友关系'
        verbose_name_plural = '好友关系'
        db_table = 'social_friendships'
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"

    def accept(self):
        """接受好友请求"""
        self.status = 'accepted'
        self.accepted_at = timezone.now()
        self.save(update_fields=['status', 'accepted_at'])

        # 创建反向好友关系
        Friendship.objects.get_or_create(
            from_user=self.to_user,
            to_user=self.from_user,
            defaults={
                'status': 'accepted',
                'accepted_at': timezone.now()
            }
        )

    def block(self):
        """屏蔽用户"""
        self.status = 'blocked'
        self.save(update_fields=['status'])

    @classmethod
    def are_friends(cls, user1, user2):
        """检查两个用户是否是好友"""
        return cls.objects.filter(
            from_user=user1,
            to_user=user2,
            status='accepted'
        ).exists()


class Group(BaseModel):
    """群组"""
    GROUP_TYPES = [
        ('public', '公开群组'),
        ('private', '私密群组'),
        ('secret', '秘密群组'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name='群组名称'
    )
    description = models.TextField(
        blank=True,
        verbose_name='群组描述'
    )
    group_type = models.CharField(
        max_length=20,
        choices=GROUP_TYPES,
        default='public',
        verbose_name='群组类型'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_groups',
        verbose_name='创建者'
    )
    avatar = models.ImageField(
        upload_to='groups/avatars/',
        null=True,
        blank=True,
        verbose_name='群组头像'
    )
    members = models.ManyToManyField(
        User,
        through='GroupMembership',
        verbose_name='成员'
    )
    member_count = models.PositiveIntegerField(
        default=0,
        verbose_name='成员数量'
    )
    max_members = models.PositiveIntegerField(
        default=500,
        verbose_name='最大成员数'
    )
    tags = models.ManyToManyField(
        'core.Tag',
        blank=True,
        verbose_name='标签'
    )

    class Meta:
        verbose_name = '群组'
        verbose_name_plural = '群组'
        db_table = 'social_groups'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def add_member(self, user, role='member'):
        """添加成员"""
        membership, created = GroupMembership.objects.get_or_create(
            group=self,
            user=user,
            defaults={'role': role}
        )
        if created:
            self.update_member_count()
        return membership

    def remove_member(self, user):
        """移除成员"""
        try:
            membership = GroupMembership.objects.get(group=self, user=user)
            membership.delete()
            self.update_member_count()
            return True
        except GroupMembership.DoesNotExist:
            return False

    def update_member_count(self):
        """更新成员数量"""
        self.member_count = self.memberships.count()
        self.save(update_fields=['member_count'])

    def can_join(self, user):
        """检查用户是否可以加入"""
        if self.member_count >= self.max_members:
            return False
        if self.memberships.filter(user=user).exists():
            return False
        return True


class GroupMembership(BaseModel):
    """群组成员关系"""
    ROLE_CHOICES = [
        ('owner', '群主'),
        ('admin', '管理员'),
        ('member', '成员'),
    ]

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='群组'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_memberships',
        verbose_name='用户'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member',
        verbose_name='角色'
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='加入时间'
    )

    class Meta:
        verbose_name = '群组成员'
        verbose_name_plural = '群组成员'
        db_table = 'social_group_memberships'
        unique_together = ['group', 'user']
        ordering = ['role', '-joined_at']

    def __str__(self):
        return f"{self.user.username} in {self.group.name} ({self.role})"

    def can_manage_group(self):
        """检查是否可以管理群组"""
        return self.role in ['owner', 'admin']


class Post(BaseModel):
    """动态"""
    POST_TYPES = [
        ('text', '文本'),
        ('image', '图片'),
        ('video', '视频'),
        ('link', '链接'),
        ('poll', '投票'),
    ]

    VISIBILITY_CHOICES = [
        ('public', '公开'),
        ('friends', '仅好友'),
        ('private', '仅自己'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='作者'
    )
    content = models.TextField(
        verbose_name='内容'
    )
    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPES,
        default='text',
        verbose_name='动态类型'
    )
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default='public',
        verbose_name='可见性'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='所属群组'
    )
    attachments = models.ManyToManyField(
        'core.Attachment',
        blank=True,
        verbose_name='附件'
    )
    tags = models.ManyToManyField(
        'core.Tag',
        blank=True,
        verbose_name='标签'
    )
    like_count = models.PositiveIntegerField(
        default=0,
        verbose_name='点赞数'
    )
    comment_count = models.PositiveIntegerField(
        default=0,
        verbose_name='评论数'
    )
    share_count = models.PositiveIntegerField(
        default=0,
        verbose_name='分享数'
    )
    is_pinned = models.BooleanField(
        default=False,
        verbose_name='置顶'
    )

    class Meta:
        verbose_name = '动态'
        verbose_name_plural = '动态'
        db_table = 'social_posts'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

    def update_like_count(self):
        """更新点赞数"""
        self.like_count = self.likes.count()
        self.save(update_fields=['like_count'])

    def update_comment_count(self):
        """更新评论数"""
        self.comment_count = self.comments.filter(is_active=True).count()
        self.save(update_fields=['comment_count'])

    def update_share_count(self):
        """更新分享数"""
        self.share_count = self.shares.count()
        self.save(update_fields=['share_count'])


class PostLike(BaseModel):
    """动态点赞"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='动态'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_likes',
        verbose_name='用户'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='点赞时间'
    )

    class Meta:
        verbose_name = '动态点赞'
        verbose_name_plural = '动态点赞'
        db_table = 'social_post_likes'
        unique_together = ['post', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class Comment(BaseModel):
    """评论"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='动态'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='作者'
    )
    content = models.TextField(
        validators=[MinLengthValidator(1)],
        verbose_name='评论内容'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='父评论'
    )
    like_count = models.PositiveIntegerField(
        default=0,
        verbose_name='点赞数'
    )
    reply_count = models.PositiveIntegerField(
        default=0,
        verbose_name='回复数'
    )

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        db_table = 'social_comments'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

    def update_like_count(self):
        """更新点赞数"""
        self.like_count = self.comment_likes.count()
        self.save(update_fields=['like_count'])

    def update_reply_count(self):
        """更新回复数"""
        self.reply_count = self.replies.filter(is_active=True).count()
        self.save(update_fields=['reply_count'])


class CommentLike(BaseModel):
    """评论点赞"""
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment_likes',
        verbose_name='评论'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_likes',
        verbose_name='用户'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='点赞时间'
    )

    class Meta:
        verbose_name = '评论点赞'
        verbose_name_plural = '评论点赞'
        db_table = 'social_comment_likes'
        unique_together = ['comment', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"


class Message(BaseModel):
    """私信"""
    MESSAGE_TYPES = [
        ('text', '文本'),
        ('image', '图片'),
        ('file', '文件'),
        ('system', '系统消息'),
    ]

    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='对话'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='发送者'
    )
    content = models.TextField(
        verbose_name='消息内容'
    )
    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default='text',
        verbose_name='消息类型'
    )
    attachment = models.ForeignKey(
        'core.Attachment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='附件'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='已读'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='阅读时间'
    )

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = '私信'
        db_table = 'social_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"

    def mark_as_read(self, user):
        """标记为已读"""
        if not self.is_read and self.sender != user:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class Conversation(BaseModel):
    """对话"""
    CONVERSATION_TYPES = [
        ('private', '私聊'),
        ('group', '群聊'),
    ]

    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        verbose_name='参与者'
    )
    conversation_type = models.CharField(
        max_length=20,
        choices=CONVERSATION_TYPES,
        default='private',
        verbose_name='对话类型'
    )
    title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='对话标题'
    )
    last_message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='最后消息'
    )
    last_message_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='最后消息时间'
    )

    class Meta:
        verbose_name = '对话'
        verbose_name_plural = '对话'
        db_table = 'social_conversations'
        ordering = ['-last_message_at']

    def __str__(self):
        if self.title:
            return self.title
        participants = list(self.participants.all()[:2])
        if len(participants) == 2:
            return f"{participants[0].username} & {participants[1].username}"
        return f"对话 {self.id}"

    def update_last_message(self, message):
        """更新最后消息"""
        self.last_message = message
        self.last_message_at = message.created_at
        self.save(update_fields=['last_message', 'last_message_at'])


class Follow(BaseModel):
    """关注关系"""
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='关注者'
    )
    followed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='被关注者'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='关注时间'
    )

    class Meta:
        verbose_name = '关注关系'
        verbose_name_plural = '关注关系'
        db_table = 'social_follows'
        unique_together = ['follower', 'followed']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"


class Notification(BaseModel):
    """通知"""
    NOTIFICATION_TYPES = [
        ('like', '点赞'),
        ('comment', '评论'),
        ('follow', '关注'),
        ('friend_request', '好友请求'),
        ('group_invite', '群组邀请'),
        ('message', '私信'),
        ('system', '系统通知'),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='social_notifications',
        verbose_name='接收者'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='social_sent_notifications',
        verbose_name='发送者'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name='通知类型'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='标题'
    )
    content = models.TextField(
        verbose_name='内容'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='已读'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='阅读时间'
    )
    related_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='关联对象ID'
    )
    related_object_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='关联对象类型'
    )

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'
        db_table = 'social_notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient', 'notification_type']),
        ]

    def __str__(self):
        return f"{self.recipient.username}: {self.title}"

    def mark_as_read(self):
        """标记为已读"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    @classmethod
    def create_notification(cls, recipient, notification_type, title, content, sender=None, related_object=None):
        """创建通知"""
        notification_data = {
            'recipient': recipient,
            'notification_type': notification_type,
            'title': title,
            'content': content,
            'sender': sender,
        }

        if related_object:
            notification_data['related_object_id'] = related_object.id
            notification_data['related_object_type'] = related_object.__class__.__name__

        return cls.objects.create(**notification_data)


class PostShare(BaseModel):
    """动态分享"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='shares',
        verbose_name='动态'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_shares',
        verbose_name='用户'
    )
    content = models.TextField(
        blank=True,
        verbose_name='分享内容'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='分享时间'
    )

    class Meta:
        verbose_name = '动态分享'
        verbose_name_plural = '动态分享'
        db_table = 'social_post_shares'
        unique_together = ['post', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} shares {self.post.id}"
