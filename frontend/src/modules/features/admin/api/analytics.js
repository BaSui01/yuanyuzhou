/**
 * 管理后台数据分析 API
 */
import { request } from '@/modules/http/request'

// 基础路径
const BASE_PATH = '/api/admin/analytics'

/**
 * 管理后台数据分析 API 服务
 */
export const analytics = {
  /**
   * 获取分析数据
   * @param {Object} params - 查询参数
   * @param {string} params.period - 时间周期 (today, yesterday, this_week, this_month, this_quarter, this_year)
   * @param {string} params.start_date - 开始日期
   * @param {string} params.end_date - 结束日期
   * @param {string} params.metrics - 指标列表，逗号分隔
   * @returns {Promise} - 返回 Promise
   */
  getAnalyticsData: (params = {}) => {
    return request.get(BASE_PATH, params)
  },

  /**
   * 获取用户活跃度趋势
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回 Promise
   */
  getUserActivityTrend: (params = {}) => {
    return request.get(`${BASE_PATH}/user-activity`, params)
  },

  /**
   * 获取设备使用分布
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回 Promise
   */
  getDeviceUsage: (params = {}) => {
    return request.get(`${BASE_PATH}/device-usage`, params)
  },

  /**
   * 获取AI助手使用情况
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回 Promise
   */
  getAIUsage: (params = {}) => {
    return request.get(`${BASE_PATH}/ai-usage`, params)
  },

  /**
   * 获取用户留存率
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回 Promise
   */
  getUserRetention: (params = {}) => {
    return request.get(`${BASE_PATH}/user-retention`, params)
  },

  /**
   * 获取热门对话主题
   * @param {Object} params - 查询参数
   * @param {number} params.limit - 返回数量
   * @returns {Promise} - 返回 Promise
   */
  getTopConversationTopics: (params = {}) => {
    return request.get(`${BASE_PATH}/top-topics`, params)
  },

  /**
   * 获取热门空间场景
   * @param {Object} params - 查询参数
   * @param {number} params.limit - 返回数量
   * @returns {Promise} - 返回 Promise
   */
  getTopSpaceScenes: (params = {}) => {
    return request.get(`${BASE_PATH}/top-scenes`, params)
  },

  /**
   * 导出分析报告
   * @param {Object} params - 查询参数
   * @param {string} params.format - 导出格式 (pdf, excel, csv)
   * @returns {Promise} - 返回 Promise
   */
  exportReport: (params = {}) => {
    return request.get(`${BASE_PATH}/export`, params, { responseType: 'blob' })
  },

  /**
   * 获取所有主题分析
   * @returns {Promise} - 返回 Promise
   */
  getAllTopics: () => {
    return request.get(`${BASE_PATH}/topics`)
  },

  /**
   * 获取所有场景分析
   * @returns {Promise} - 返回 Promise
   */
  getAllScenes: () => {
    return request.get(`${BASE_PATH}/scenes`)
  },

  /**
   * 获取自定义分析数据
   * @param {Object} data - 查询数据
   * @returns {Promise} - 返回 Promise
   */
  getCustomAnalytics: (data) => {
    return request.post(`${BASE_PATH}/custom`, data)
  }
}
