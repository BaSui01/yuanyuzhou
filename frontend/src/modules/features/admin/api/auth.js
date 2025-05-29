/**
 * 管理后台认证 API
 */
import { request } from '@/modules/http/request'

// 基础路径
const BASE_PATH = '/api/admin'

/**
 * 管理后台认证 API 服务
 */
export const auth = {
  /**
   * 管理员登录
   * @param {Object} data - 登录数据
   * @param {string} data.username - 用户名
   * @param {string} data.password - 密码
   * @returns {Promise} - 返回 Promise
   */
  login: (data) => {
    return request.post(`${BASE_PATH}/auth/login`, data)
  },

  /**
   * 管理员退出登录
   * @returns {Promise} - 返回 Promise
   */
  logout: () => {
    return request.post(`${BASE_PATH}/auth/logout`)
  },

  /**
   * 获取管理员个人资料
   * @returns {Promise} - 返回 Promise
   */
  getProfile: () => {
    return request.get(`${BASE_PATH}/profile`)
  },

  /**
   * 更新管理员个人资料
   * @param {Object} data - 个人资料数据
   * @returns {Promise} - 返回 Promise
   */
  updateProfile: (data) => {
    return request.put(`${BASE_PATH}/profile`, data)
  },

  /**
   * 更改管理员密码
   * @param {Object} data - 密码数据
   * @param {string} data.oldPassword - 旧密码
   * @param {string} data.newPassword - 新密码
   * @param {string} data.confirmPassword - 确认新密码
   * @returns {Promise} - 返回 Promise
   */
  changePassword: (data) => {
    return request.post(`${BASE_PATH}/change-password`, data)
  },

  /**
   * 刷新令牌
   * @returns {Promise} - 返回 Promise
   */
  refreshToken: () => {
    return request.post(`${BASE_PATH}/auth/refresh-token`)
  },

  /**
   * 验证令牌
   * @returns {Promise} - 返回 Promise
   */
  validateToken: () => {
    return request.get(`${BASE_PATH}/auth/validate-token`)
  }
}
