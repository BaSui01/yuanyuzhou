import axios from '../axios';

/**
 * 用户相关API
 */
export const userAPI = {
  // 获取用户列表
  getUsers: (params = {}) => {
    return axios.get('/users', {
      params: {
        page: params.page || 1,
        per_page: params.perPage || 20,
        search: params.search || '',
        sort_by: params.sortBy || 'created_at',
        sort_order: params.sortOrder || 'desc',
        status: params.status
      }
    });
  },

  // 获取单个用户
  getUser: (userId) => {
    return axios.get(`/users/${userId}`);
  },

  // 创建用户
  createUser: (userData) => {
    return axios.post('/users', userData);
  },

  // 更新用户
  updateUser: (userId, userData) => {
    return axios.put(`/users/${userId}`, userData);
  },

  // 删除用户
  deleteUser: (userId) => {
    return axios.delete(`/users/${userId}`);
  },

  // 获取用户角色
  getUserRoles: (userId) => {
    return axios.get(`/users/${userId}/roles`);
  },

  // 分配角色给用户
  assignRoles: (userId, roles) => {
    return axios.post(`/users/${userId}/roles`, { roles });
  },

  // 获取用户权限
  getUserPermissions: (userId) => {
    return axios.get(`/users/${userId}/permissions`);
  },

  // 获取用户活动日志
  getUserActivities: (userId, params = {}) => {
    return axios.get(`/users/${userId}/activities`, {
      params: {
        page: params.page || 1,
        per_page: params.perPage || 20,
        start_date: params.startDate,
        end_date: params.endDate,
        type: params.type
      }
    });
  },

  // 获取在线用户
  getOnlineUsers: () => {
    return axios.get('/users/online');
  },

  // 获取用户统计
  getUserStats: () => {
    return axios.get('/users/stats');
  },

  // 导出用户数据
  exportUsers: (format = 'csv') => {
    return axios.get('/users/export', {
      params: { format },
      responseType: 'blob'
    });
  },

  // 导入用户数据
  importUsers: (file) => {
    const formData = new FormData();
    formData.append('file', file);

    return axios.post('/users/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 批量操作用户
  bulkActionUsers: (userIds, action) => {
    return axios.post('/users/bulk-action', {
      user_ids: userIds,
      action: action
    });
  },

  // 获取用户好友列表
  getUserFriends: (userId) => {
    return axios.get(`/users/${userId}/friends`);
  },

  // 添加好友
  addFriend: (userId) => {
    return axios.post(`/users/${userId}/friends`);
  },

  // 移除好友
  removeFriend: (userId, friendId) => {
    return axios.delete(`/users/${userId}/friends/${friendId}`);
  },

  // 获取好友请求
  getFriendRequests: () => {
    return axios.get('/users/friend-requests');
  },

  // 接受好友请求
  acceptFriendRequest: (requestId) => {
    return axios.post(`/users/friend-requests/${requestId}/accept`);
  },

  // 拒绝好友请求
  rejectFriendRequest: (requestId) => {
    return axios.post(`/users/friend-requests/${requestId}/reject`);
  },

  // 获取用户通知
  getUserNotifications: (params = {}) => {
    return axios.get('/users/notifications', {
      params: {
        page: params.page || 1,
        per_page: params.perPage || 20,
        read: params.read
      }
    });
  },

  // 标记通知为已读
  markNotificationAsRead: (notificationId) => {
    return axios.put(`/users/notifications/${notificationId}/read`);
  },

  // 标记所有通知为已读
  markAllNotificationsAsRead: () => {
    return axios.put('/users/notifications/read-all');
  },

  // 删除通知
  deleteNotification: (notificationId) => {
    return axios.delete(`/users/notifications/${notificationId}`);
  },

  // 获取用户设置
  getUserSettings: () => {
    return axios.get('/users/settings');
  },

  // 更新用户设置
  updateUserSettings: (settings) => {
    return axios.put('/users/settings', settings);
  }
};
