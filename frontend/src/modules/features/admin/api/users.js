/**
 * 管理后台用户管理 API
 */
import { request } from '@/modules/http/request'

// 基础路径
const BASE_PATH = '/api/admin/users'

/**
 * 管理后台用户管理 API 服务
 */
export const users = {
  /**
   * 获取用户列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.pageSize - 每页数量
   * @param {string} params.search - 搜索关键词
   * @param {string} params.status - 用户状态
   * @param {string} params.role - 用户角色
   * @returns {Promise} - 返回 Promise
   */
  getUsers: (params = {}) => {
    return request.get(BASE_PATH, params)
  },

  /**
   * 获取用户详情
   * @param {string|number} userId - 用户ID
   * @returns {Promise} - 返回 Promise
   */
  getUserDetail: (userId) => {
    return request.get(`${BASE_PATH}/${userId}`)
  },

  /**
   * 创建用户
   * @param {Object} data - 用户数据
   * @returns {Promise} - 返回 Promise
   */
  createUser: (data) => {
    return request.post(BASE_PATH, data)
  },

  /**
   * 更新用户信息
   * @param {string|number} userId - 用户ID
   * @param {Object} data - 用户数据
   * @returns {Promise} - 返回 Promise
   */
  updateUser: (userId, data) => {
    return request.put(`${BASE_PATH}/${userId}`, data)
  },

  /**
   * 删除用户
   * @param {string|number} userId - 用户ID
   * @returns {Promise} - 返回 Promise
   */
  deleteUser: (userId) => {
    return request.delete(`${BASE_PATH}/${userId}`)
  },

  /**
   * 批量删除用户
   * @param {Array} userIds - 用户ID数组
   * @returns {Promise} - 返回 Promise
   */
  batchDeleteUsers: (userIds) => {
    return request.post(`${BASE_PATH}/batch-delete`, { ids: userIds })
  },

  /**
   * 更新用户状态
   * @param {string|number} userId - 用户ID
   * @param {string} status - 用户状态
   * @returns {Promise} - 返回 Promise
   */
  updateUserStatus: (userId, status) => {
    return request.patch(`${BASE_PATH}/${userId}/status`, { status })
  },

  /**
   * 获取用户登录历史
   * @param {string|number} userId - 用户ID
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回 Promise
   */
  getUserLoginHistory: (userId, params = {}) => {
    return request.get(`${BASE_PATH}/${userId}/login-history`, params)
  },

  /**
   * 获取用户活动记录
   * @param {string|number} userId - 用户ID
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回 Promise
   */
  getUserActivityLog: (userId, params = {}) => {
    return request.get(`${BASE_PATH}/${userId}/activity-log`, params)
  },

  /**
   * 重置用户密码
   * @param {string|number} userId - 用户ID
   * @returns {Promise} - 返回 Promise
   */
  resetUserPassword: (userId) => {
    return request.post(`${BASE_PATH}/${userId}/reset-password`)
  }
}
