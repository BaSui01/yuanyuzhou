import axios from '@/api/axios';

/**
 * 用户功能相关的API服务
 */
export const userService = {
  // 获取用户资料
  getUserProfile: (userId) => {
    return axios.get(`/user/profile${userId ? `/${userId}` : ''}`);
  },

  // 更新用户资料
  updateUserProfile: (data) => {
    return axios.put('/user/profile', data);
  },

  // 更新用户头像
  updateAvatar: (file) => {
    const formData = new FormData();
    formData.append('avatar', file);

    return axios.post('/user/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 获取用户设置
  getUserSettings: () => {
    return axios.get('/user/settings');
  },

  // 更新用户设置
  updateUserSettings: (settings) => {
    return axios.put('/user/settings', settings);
  },

  // 获取用户好友列表
  getFriends: (params = {}) => {
    return axios.get('/user/friends', { params });
  },

  // 发送好友请求
  sendFriendRequest: (userId) => {
    return axios.post('/user/friends/request', { userId });
  },

  // 接受好友请求
  acceptFriendRequest: (requestId) => {
    return axios.post(`/user/friends/request/${requestId}/accept`);
  },

  // 拒绝好友请求
  rejectFriendRequest: (requestId) => {
    return axios.post(`/user/friends/request/${requestId}/reject`);
  },

  // 获取好友请求列表
  getFriendRequests: () => {
    return axios.get('/user/friends/requests');
  },

  // 删除好友
  removeFriend: (friendId) => {
    return axios.delete(`/user/friends/${friendId}`);
  },

  // 获取用户通知
  getNotifications: (params = {}) => {
    return axios.get('/user/notifications', { params });
  },

  // 标记通知为已读
  markNotificationRead: (notificationId) => {
    return axios.put(`/user/notifications/${notificationId}/read`);
  },

  // 标记所有通知为已读
  markAllNotificationsRead: () => {
    return axios.put('/user/notifications/read-all');
  },

  // 删除通知
  deleteNotification: (notificationId) => {
    return axios.delete(`/user/notifications/${notificationId}`);
  },

  // 获取用户活动历史
  getActivityHistory: (params = {}) => {
    return axios.get('/user/activity', { params });
  }
};

export default userService;
