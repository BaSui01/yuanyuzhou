/**
 * 管理后台设置 API
 */
import { request } from '@/modules/http/request'

// 基础路径
const BASE_PATH = '/api/admin/settings'

/**
 * 管理后台设置 API 服务
 */
export const settings = {
  /**
   * 获取系统设置
   * @returns {Promise} - 返回 Promise
   */
  getSystemSettings: () => {
    return request.get(`${BASE_PATH}/system`)
  },

  /**
   * 更新系统设置
   * @param {Object} data - 系统设置数据
   * @returns {Promise} - 返回 Promise
   */
  updateSystemSettings: (data) => {
    return request.put(`${BASE_PATH}/system`, data)
  },

  /**
   * 获取安全设置
   * @returns {Promise} - 返回 Promise
   */
  getSecuritySettings: () => {
    return request.get(`${BASE_PATH}/security`)
  },

  /**
   * 更新安全设置
   * @param {Object} data - 安全设置数据
   * @returns {Promise} - 返回 Promise
   */
  updateSecuritySettings: (data) => {
    return request.put(`${BASE_PATH}/security`, data)
  },

  /**
   * 获取邮件设置
   * @returns {Promise} - 返回 Promise
   */
  getEmailSettings: () => {
    return request.get(`${BASE_PATH}/email`)
  },

  /**
   * 更新邮件设置
   * @param {Object} data - 邮件设置数据
   * @returns {Promise} - 返回 Promise
   */
  updateEmailSettings: (data) => {
    return request.put(`${BASE_PATH}/email`, data)
  },

  /**
   * 发送测试邮件
   * @param {Object} data - 测试邮件数据
   * @returns {Promise} - 返回 Promise
   */
  sendTestEmail: (data) => {
    return request.post(`${BASE_PATH}/email/test`, data)
  },

  /**
   * 获取存储设置
   * @returns {Promise} - 返回 Promise
   */
  getStorageSettings: () => {
    return request.get(`${BASE_PATH}/storage`)
  },

  /**
   * 更新存储设置
   * @param {Object} data - 存储设置数据
   * @returns {Promise} - 返回 Promise
   */
  updateStorageSettings: (data) => {
    return request.put(`${BASE_PATH}/storage`, data)
  },

  /**
   * 获取AI设置
   * @returns {Promise} - 返回 Promise
   */
  getAISettings: () => {
    return request.get(`${BASE_PATH}/ai`)
  },

  /**
   * 更新AI设置
   * @param {Object} data - AI设置数据
   * @returns {Promise} - 返回 Promise
   */
  updateAISettings: (data) => {
    return request.put(`${BASE_PATH}/ai`, data)
  },

  /**
   * 获取所有设置
   * @returns {Promise} - 返回 Promise
   */
  getAllSettings: () => {
    return request.get(BASE_PATH)
  },

  /**
   * 备份系统设置
   * @returns {Promise} - 返回 Promise
   */
  backupSettings: () => {
    return request.post(`${BASE_PATH}/backup`, {}, { responseType: 'blob' })
  },

  /**
   * 恢复系统设置
   * @param {FormData} formData - 包含备份文件的表单数据
   * @returns {Promise} - 返回 Promise
   */
  restoreSettings: (formData) => {
    return request.post(`${BASE_PATH}/restore`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}
