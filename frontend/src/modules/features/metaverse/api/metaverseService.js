import axios from '@/api/axios';

/**
 * 元宇宙功能相关的API服务
 */
export const metaverseService = {
  // 获取可用的元宇宙空间列表
  getSpaces: (params = {}) => {
    return axios.get('/metaverse/spaces', { params });
  },

  // 获取单个元宇宙空间详情
  getSpaceDetails: (spaceId) => {
    return axios.get(`/metaverse/spaces/${spaceId}`);
  },

  // 创建元宇宙空间
  createSpace: (spaceData) => {
    return axios.post('/metaverse/spaces', spaceData);
  },

  // 更新元宇宙空间
  updateSpace: (spaceId, spaceData) => {
    return axios.put(`/metaverse/spaces/${spaceId}`, spaceData);
  },

  // 删除元宇宙空间
  deleteSpace: (spaceId) => {
    return axios.delete(`/metaverse/spaces/${spaceId}`);
  },

  // 加入元宇宙空间
  joinSpace: (spaceId) => {
    return axios.post(`/metaverse/spaces/${spaceId}/join`);
  },

  // 离开元宇宙空间
  leaveSpace: (spaceId) => {
    return axios.post(`/metaverse/spaces/${spaceId}/leave`);
  },

  // 获取元宇宙空间成员
  getSpaceMembers: (spaceId, params = {}) => {
    return axios.get(`/metaverse/spaces/${spaceId}/members`, { params });
  },

  // 获取用户的虚拟形象
  getAvatar: () => {
    return axios.get('/metaverse/avatar');
  },

  // 更新用户的虚拟形象
  updateAvatar: (avatarData) => {
    return axios.put('/metaverse/avatar', avatarData);
  },

  // 获取可用的虚拟物品
  getItems: (params = {}) => {
    return axios.get('/metaverse/items', { params });
  },

  // 获取单个虚拟物品详情
  getItemDetails: (itemId) => {
    return axios.get(`/metaverse/items/${itemId}`);
  },

  // 购买虚拟物品
  purchaseItem: (itemId) => {
    return axios.post(`/metaverse/items/${itemId}/purchase`);
  },

  // 获取用户拥有的虚拟物品
  getUserItems: () => {
    return axios.get('/metaverse/user/items');
  },

  // 获取元宇宙活动列表
  getEvents: (params = {}) => {
    return axios.get('/metaverse/events', { params });
  },

  // 获取单个元宇宙活动详情
  getEventDetails: (eventId) => {
    return axios.get(`/metaverse/events/${eventId}`);
  },

  // 创建元宇宙活动
  createEvent: (eventData) => {
    return axios.post('/metaverse/events', eventData);
  },

  // 参加元宇宙活动
  joinEvent: (eventId) => {
    return axios.post(`/metaverse/events/${eventId}/join`);
  },

  // 取消参加元宇宙活动
  leaveEvent: (eventId) => {
    return axios.post(`/metaverse/events/${eventId}/leave`);
  }
};

export default metaverseService;
