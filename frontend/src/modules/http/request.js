/**
 * 统一请求方法
 */

import secureAxios from './secureAxios'
import crypto from './utils/crypto'

/**
 * 通用请求方法
 */
export const request = {
  /**
   * GET请求
   * @param {string} url - 请求地址
   * @param {Object} params - 请求参数
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  get: (url, params = {}, config = {}) => {
    return secureAxios.get(url, { params, ...config })
  },

  /**
   * POST请求
   * @param {string} url - 请求地址
   * @param {Object} data - 请求数据
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  post: (url, data = {}, config = {}) => {
    return secureAxios.post(url, data, config)
  },

  /**
   * PUT请求
   * @param {string} url - 请求地址
   * @param {Object} data - 请求数据
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  put: (url, data = {}, config = {}) => {
    return secureAxios.put(url, data, config)
  },

  /**
   * PATCH请求
   * @param {string} url - 请求地址
   * @param {Object} data - 请求数据
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  patch: (url, data = {}, config = {}) => {
    return secureAxios.patch(url, data, config)
  },

  /**
   * DELETE请求
   * @param {string} url - 请求地址
   * @param {Object} params - 请求参数
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  delete: (url, params = {}, config = {}) => {
    return secureAxios.delete(url, { params, ...config })
  },

  /**
   * 上传文件
   * @param {string} url - 请求地址
   * @param {FormData} formData - 表单数据
   * @param {Function} onProgress - 上传进度回调
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  upload: (url, formData, onProgress = null, config = {}) => {
    const uploadConfig = {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      ...config
    }

    if (onProgress) {
      uploadConfig.onUploadProgress = progressEvent => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(percentCompleted)
      }
    }

    return secureAxios.post(url, formData, uploadConfig)
  },

  /**
   * 下载文件
   * @param {string} url - 请求地址
   * @param {Object} params - 请求参数
   * @param {Function} onProgress - 下载进度回调
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  download: (url, params = {}, onProgress = null, config = {}) => {
    const downloadConfig = {
      responseType: 'blob',
      params,
      ...config
    }

    if (onProgress) {
      downloadConfig.onDownloadProgress = progressEvent => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(percentCompleted)
      }
    }

    return secureAxios.get(url, downloadConfig)
  },

  /**
   * 流式请求（用于 Server-Sent Events）
   * @param {string} url - 请求地址
   * @param {Object} params - 请求参数
   * @param {Function} onMessage - 消息回调
   * @param {Function} onError - 错误回调
   * @returns {EventSource} - 返回EventSource实例
   */
  stream: (url, params = {}, onMessage = null, onError = null) => {
    const queryString = new URLSearchParams(params).toString()
    const fullUrl = queryString ? `${url}?${queryString}` : url

    const eventSource = new EventSource(fullUrl)

    if (onMessage) {
      eventSource.onmessage = onMessage
    }

    if (onError) {
      eventSource.onerror = onError
    }

    return eventSource
  },

  /**
   * WebSocket 连接
   * @param {string} url - WebSocket地址
   * @param {Object} options - 连接选项
   * @returns {WebSocket} - 返回WebSocket实例
   */
  websocket: (url, options = {}) => {
    const {
      protocols = [],
      onOpen = null,
      onMessage = null,
      onError = null,
      onClose = null
    } = options

    const ws = new WebSocket(url, protocols)

    if (onOpen) ws.onopen = onOpen
    if (onMessage) ws.onmessage = onMessage
    if (onError) ws.onerror = onError
    if (onClose) ws.onclose = onClose

    return ws
  },

  /**
   * 加密数据
   * @param {Object|String} data - 要加密的数据
   * @param {Number} level - 加密级别
   * @returns {String} - 加密后的字符串
   */
  encrypt: (data, level = 2) => {
    return crypto.encrypt(data, level)
  },

  /**
   * 解密数据
   * @param {String} encryptedData - 加密的数据
   * @param {Number} level - 解密级别
   * @returns {Object|String} - 解密后的数据
   */
  decrypt: (encryptedData, level = 2) => {
    return crypto.decrypt(encryptedData, level)
  },

  /**
   * 设置加密级别
   * @param {Number} level - 加密级别
   */
  setEncryptLevel: (level) => {
    secureAxios.setEncryptLevel(level)
  },

  /**
   * 启用或禁用加密
   * @param {Boolean} enabled - 是否启用
   */
  setEncryption: (enabled) => {
    secureAxios.setEncryption(enabled)
  }
}

// 默认导出
export default request
