/**
 * API模块
 * 提供与后端API通信的功能
 */

import axios from './axios'
import secureAxios from './secureAxios'

/**
 * API基础类
 */
export class API {
  /**
   * 构造函数
   * @param {String} baseURL - API基础URL
   * @param {Boolean} secure - 是否使用安全传输
   */
  constructor(baseURL = '/api', secure = false) {
    this.baseURL = baseURL
    this.client = secure ? secureAxios : axios
  }

  /**
   * GET请求
   * @param {String} url - 请求路径
   * @param {Object} params - 请求参数
   * @param {Object} config - 额外配置
   * @returns {Promise} - 请求Promise
   */
  async get(url, params = {}, config = {}) {
    try {
      const response = await this.client.get(url, {
        params,
        ...config
      })
      return response.data
    } catch (error) {
      this.handleError(error)
      throw error
    }
  }

  /**
   * POST请求
   * @param {String} url - 请求路径
   * @param {Object} data - 请求数据
   * @param {Object} config - 额外配置
   * @returns {Promise} - 请求Promise
   */
  async post(url, data = {}, config = {}) {
    try {
      const response = await this.client.post(url, data, config)
      return response.data
    } catch (error) {
      this.handleError(error)
      throw error
    }
  }

  /**
   * PUT请求
   * @param {String} url - 请求路径
   * @param {Object} data - 请求数据
   * @param {Object} config - 额外配置
   * @returns {Promise} - 请求Promise
   */
  async put(url, data = {}, config = {}) {
    try {
      const response = await this.client.put(url, data, config)
      return response.data
    } catch (error) {
      this.handleError(error)
      throw error
    }
  }

  /**
   * DELETE请求
   * @param {String} url - 请求路径
   * @param {Object} config - 额外配置
   * @returns {Promise} - 请求Promise
   */
  async delete(url, config = {}) {
    try {
      const response = await this.client.delete(url, config)
      return response.data
    } catch (error) {
      this.handleError(error)
      throw error
    }
  }

  /**
   * PATCH请求
   * @param {String} url - 请求路径
   * @param {Object} data - 请求数据
   * @param {Object} config - 额外配置
   * @returns {Promise} - 请求Promise
   */
  async patch(url, data = {}, config = {}) {
    try {
      const response = await this.client.patch(url, data, config)
      return response.data
    } catch (error) {
      this.handleError(error)
      throw error
    }
  }

  /**
   * 错误处理
   * @param {Error} error - 错误对象
   */
  handleError(error) {
    if (error.response) {
      // 服务器返回错误状态码
      console.error('API错误:', error.response.status, error.response.data)
    } else if (error.request) {
      // 请求发送但没有收到响应
      console.error('API请求无响应:', error.request)
    } else {
      // 请求设置出错
      console.error('API请求错误:', error.message)
    }
  }
}

/**
 * 安全API类
 * 使用加密传输的API
 */
export class SecureAPI extends API {
  constructor(baseURL = '/api') {
    super(baseURL, true)
  }
}

// 导出API实例
export const api = new API()
export const secureApi = new SecureAPI()

export default api
