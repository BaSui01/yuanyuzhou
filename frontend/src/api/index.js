import secureAxios from './secureAxios';
import crypto from './utils/crypto';

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
    return secureAxios.get(url, { params, ...config });
  },

  /**
   * POST请求
   * @param {string} url - 请求地址
   * @param {Object} data - 请求数据
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  post: (url, data = {}, config = {}) => {
    return secureAxios.post(url, data, config);
  },

  /**
   * PUT请求
   * @param {string} url - 请求地址
   * @param {Object} data - 请求数据
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  put: (url, data = {}, config = {}) => {
    return secureAxios.put(url, data, config);
  },

  /**
   * DELETE请求
   * @param {string} url - 请求地址
   * @param {Object} params - 请求参数
   * @param {Object} config - 额外配置
   * @returns {Promise} - 返回Promise
   */
  delete: (url, params = {}, config = {}) => {
    return secureAxios.delete(url, { params, ...config });
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
    };

    if (onProgress) {
      uploadConfig.onUploadProgress = progressEvent => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(percentCompleted);
      };
    }

    return secureAxios.post(url, formData, uploadConfig);
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
    };

    if (onProgress) {
      downloadConfig.onDownloadProgress = progressEvent => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(percentCompleted);
      };
    }

    return secureAxios.get(url, downloadConfig);
  },

  /**
   * 加密数据
   * @param {Object|String} data - 要加密的数据
   * @param {Number} level - 加密级别
   * @returns {String} - 加密后的字符串
   */
  encrypt: (data, level = 2) => {
    return crypto.encrypt(data, level);
  },

  /**
   * 解密数据
   * @param {String} encryptedData - 加密的数据
   * @param {Number} level - 解密级别
   * @returns {Object|String} - 解密后的数据
   */
  decrypt: (encryptedData, level = 2) => {
    return crypto.decrypt(encryptedData, level);
  },

  /**
   * 设置加密级别
   * @param {Number} level - 加密级别
   */
  setEncryptLevel: (level) => {
    secureAxios.setEncryptLevel(level);
  },

  /**
   * 启用或禁用加密
   * @param {Boolean} enabled - 是否启用
   */
  setEncryption: (enabled) => {
    secureAxios.setEncryption(enabled);
  }
};

// 导入API模块
import { authAPI } from './modules/auth';
import { userAPI } from './modules/user';
import { aiAPI } from './modules/ai';
import { metaverseAPI } from './modules/metaverse';

// 导出API模块
export { authAPI, userAPI, aiAPI, metaverseAPI, crypto };

// 默认导出
export default {
  request,
  auth: authAPI,
  user: userAPI,
  ai: aiAPI,
  metaverse: metaverseAPI,
  crypto
};
