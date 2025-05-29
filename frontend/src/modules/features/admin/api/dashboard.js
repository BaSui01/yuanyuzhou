/**
 * 管理后台仪表盘 API
 */
import { request } from '@/modules/http/request'

// 基础路径
const BASE_PATH = '/api/admin/dashboard'

/**
 * 管理后台仪表盘 API 服务
 */
export const dashboard = {
  /**
   * 获取仪表盘统计数据
   * @returns {Promise} - 返回 Promise
   */
  getStats: () => {
    return request.get(`${BASE_PATH}/stats`)
  },

  /**
   * 获取用户增长趋势数据
   * @param {Object} params - 查询参数
   * @param {string} params.period - 时间周期 (7d, 30d, 90d, 1y)
   * @returns {Promise} - 返回 Promise
   */
  getUserGrowthTrend: (params = {}) => {
    return request.get(`${BASE_PATH}/user-growth`, params)
  },

  /**
   * 获取活跃用户分布数据
   * @returns {Promise} - 返回 Promise
   */
  getActiveUsersDistribution: () => {
    return request.get(`${BASE_PATH}/active-users`)
  },

  /**
   * 获取最近注册用户
   * @param {Object} params - 查询参数
   * @param {number} params.limit - 返回数量
   * @returns {Promise} - 返回 Promise
   */
  getRecentUsers: (params = {}) => {
    return request.get(`${BASE_PATH}/recent-users`, params)
  },

  /**
   * 获取系统通知
   * @param {Object} params - 查询参数
   * @param {number} params.limit - 返回数量
   * @returns {Promise} - 返回 Promise
   */
  getSystemNotifications: (params = {}) => {
    return request.get(`${BASE_PATH}/notifications`, params)
  },

  /**
   * 获取所有仪表盘数据
   * @returns {Promise} - 返回 Promise
   */
  getAllDashboardData: () => {
    return request.get(BASE_PATH)
  },

  /**
   * 创建系统通知
   * @param {Object} data - 通知数据
   * @returns {Promise} - 返回 Promise
   */
  createNotification: (data) => {
    return request.post(`${BASE_PATH}/notifications`, data)
  },

  /**
   * 查看系统通知详情
   * @param {string|number} notificationId - 通知ID
   * @returns {Promise} - 返回 Promise
   */
  getNotificationDetail: (notificationId) => {
    return request.get(`${BASE_PATH}/notifications/${notificationId}`)
  },

  /**
   * 编辑系统通知
   * @param {string|number} notificationId - 通知ID
   * @param {Object} data - 通知数据
   * @returns {Promise} - 返回 Promise
   */
  updateNotification: (notificationId, data) => {
    return request.put(`${BASE_PATH}/notifications/${notificationId}`, data)
  },

  /**
   * 删除系统通知
   * @param {string|number} notificationId - 通知ID
   * @returns {Promise} - 返回 Promise
   */
  deleteNotification: (notificationId) => {
    return request.delete(`${BASE_PATH}/notifications/${notificationId}`)
  }
}
