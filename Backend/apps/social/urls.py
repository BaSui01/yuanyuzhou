from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    # 好友关系相关
    path('friends/', views.FriendshipListView.as_view(), name='friend-list'),
    path('friends/requests/', views.FriendshipListView.as_view(), name='friend-request-list'),
    path('friends/send-request/', views.send_friend_request, name='send-friend-request'),
    path('friends/accept-request/<int:friendship_id>/', views.accept_friend_request, name='accept-friend-request'),
    path('friends/reject-request/<int:request_id>/', views.reject_friend_request, name='reject-friend-request'),
    path('friends/remove/<int:user_id>/', views.remove_friend, name='remove-friend'),
    path('friends/suggestions/', views.friend_suggestions, name='friend-suggestions'),

    # 群组相关
    path('groups/', views.GroupListView.as_view(), name='group-list'),
    path('groups/<int:pk>/', views.GroupDetailView.as_view(), name='group-detail'),
    path('groups/<int:group_id>/join/', views.join_group, name='join-group'),
    path('groups/<int:group_id>/leave/', views.leave_group, name='leave-group'),
    path('groups/<int:group_id>/invite/', views.invite_to_group, name='invite-to-group'),

    # 动态相关
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    path('posts/<int:post_id>/unlike/', views.unlike_post, name='unlike-post'),
    path('posts/<int:post_id>/share/', views.share_post, name='share-post'),

    # 评论相关
    path('posts/<int:post_id>/comments/', views.CommentListView.as_view(), name='comment-list'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like-comment'),

    # 消息相关
    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/conversations/', views.ConversationListView.as_view(), name='conversation-list'),
    path('messages/send/', views.send_message, name='send-message'),

    # 通知相关
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),

    # 关注相关
    path('follow/<int:user_id>/', views.follow_user, name='follow-user'),

    # 统计相关
    path('stats/user/', views.user_social_stats, name='user-social-stats'),
]
