import axios from '../axios';

/**
 * 元宇宙相关API
 */
export const metaverseAPI = {
  // 获取可用的虚拟空间列表
  getSpaces: (params = {}) => {
    return axios.get('/metaverse/spaces', {
      params: {
        page: params.page || 1,
        per_page: params.perPage || 20,
        category: params.category,
        featured: params.featured,
        sort_by: params.sortBy || 'popular'
      }
    });
  },

  // 获取单个虚拟空间详情
  getSpace: (spaceId) => {
    return axios.get(`/metaverse/spaces/${spaceId}`);
  },

  // 创建虚拟空间
  createSpace: (spaceData) => {
    return axios.post('/metaverse/spaces', {
      name: spaceData.name,
      description: spaceData.description,
      category: spaceData.category,
      thumbnail: spaceData.thumbnail,
      settings: spaceData.settings,
      access_type: spaceData.accessType || 'public',
      max_users: spaceData.maxUsers || 50
    });
  },

  // 更新虚拟空间
  updateSpace: (spaceId, spaceData) => {
    return axios.put(`/metaverse/spaces/${spaceId}`, {
      name: spaceData.name,
      description: spaceData.description,
      category: spaceData.category,
      thumbnail: spaceData.thumbnail,
      settings: spaceData.settings,
      access_type: spaceData.accessType,
      max_users: spaceData.maxUsers
    });
  },

  // 删除虚拟空间
  deleteSpace: (spaceId) => {
    return axios.delete(`/metaverse/spaces/${spaceId}`);
  },

  // 加入虚拟空间
  joinSpace: (spaceId, options = {}) => {
    return axios.post(`/metaverse/spaces/${spaceId}/join`, {
      avatar_id: options.avatarId,
      position: options.position,
      password: options.password
    });
  },

  // 离开虚拟空间
  leaveSpace: (spaceId) => {
    return axios.post(`/metaverse/spaces/${spaceId}/leave`);
  },

  // 获取空间内用户列表
  getSpaceUsers: (spaceId) => {
    return axios.get(`/metaverse/spaces/${spaceId}/users`);
  },

  // 获取用户头像列表
  getUserAvatars: () => {
    return axios.get('/metaverse/avatars');
  },

  // 创建用户头像
  createAvatar: (avatarData) => {
    return axios.post('/metaverse/avatars', avatarData);
  },

  // 更新用户头像
  updateAvatar: (avatarId, avatarData) => {
    return axios.put(`/metaverse/avatars/${avatarId}`, avatarData);
  },

  // 删除用户头像
  deleteAvatar: (avatarId) => {
    return axios.delete(`/metaverse/avatars/${avatarId}`);
  },

  // 获取虚拟物品列表
  getItems: (params = {}) => {
    return axios.get('/metaverse/items', {
      params: {
        page: params.page || 1,
        per_page: params.perPage || 20,
        category: params.category,
        rarity: params.rarity,
        search: params.search
      }
    });
  },

  // 获取单个虚拟物品详情
  getItem: (itemId) => {
    return axios.get(`/metaverse/items/${itemId}`);
  },

  // 购买虚拟物品
  purchaseItem: (itemId) => {
    return axios.post(`/metaverse/items/${itemId}/purchase`);
  },

  // 使用虚拟物品
  useItem: (itemId, options = {}) => {
    return axios.post(`/metaverse/items/${itemId}/use`, options);
  },

  // 获取用户物品库存
  getUserInventory: () => {
    return axios.get('/metaverse/inventory');
  },

  // 获取虚拟活动列表
  getEvents: (params = {}) => {
    return axios.get('/metaverse/events', {
      params: {
        page: params.page || 1,
        per_page: params.perPage || 20,
        category: params.category,
        start_date: params.startDate,
        end_date: params.endDate
      }
    });
  },

  // 获取单个虚拟活动详情
  getEvent: (eventId) => {
    return axios.get(`/metaverse/events/${eventId}`);
  },

  // 创建虚拟活动
  createEvent: (eventData) => {
    return axios.post('/metaverse/events', eventData);
  },

  // 参加虚拟活动
  joinEvent: (eventId) => {
    return axios.post(`/metaverse/events/${eventId}/join`);
  },

  // 取消参加虚拟活动
  leaveEvent: (eventId) => {
    return axios.post(`/metaverse/events/${eventId}/leave`);
  },

  // 获取虚拟世界统计
  getMetaverseStats: () => {
    return axios.get('/metaverse/stats');
  },

  // 发送空间内消息
  sendSpaceMessage: (spaceId, message) => {
    return axios.post(`/metaverse/spaces/${spaceId}/messages`, {
      content: message.content,
      type: message.type || 'text',
      recipient_id: message.recipientId
    });
  },

  // 获取空间内消息历史
  getSpaceMessages: (spaceId, params = {}) => {
    return axios.get(`/metaverse/spaces/${spaceId}/messages`, {
      params: {
        page: params.page || 1,
        per_page: params.perPage || 50,
        start_time: params.startTime
      }
    });
  },

  // 更新用户在空间内的状态
  updateUserStatus: (spaceId, status) => {
    return axios.put(`/metaverse/spaces/${spaceId}/status`, {
      status: status.type,
      position: status.position,
      rotation: status.rotation,
      animation: status.animation
    });
  },

  // 获取空间内互动对象
  getSpaceObjects: (spaceId) => {
    return axios.get(`/metaverse/spaces/${spaceId}/objects`);
  },

  // 与空间内对象互动
  interactWithObject: (spaceId, objectId, action) => {
    return axios.post(`/metaverse/spaces/${spaceId}/objects/${objectId}/interact`, {
      action: action
    });
  },

  // 获取空间设置
  getSpaceSettings: (spaceId) => {
    return axios.get(`/metaverse/spaces/${spaceId}/settings`);
  },

  // 更新空间设置
  updateSpaceSettings: (spaceId, settings) => {
    return axios.put(`/metaverse/spaces/${spaceId}/settings`, settings);
  },

  // 获取空间访问控制列表
  getSpaceAccessList: (spaceId) => {
    return axios.get(`/metaverse/spaces/${spaceId}/access`);
  },

  // 更新空间访问控制
  updateSpaceAccess: (spaceId, accessData) => {
    return axios.put(`/metaverse/spaces/${spaceId}/access`, accessData);
  }
};
