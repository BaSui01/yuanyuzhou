import axios from './axios';
import crypto from './utils/crypto';
import { CRYPTO_CONFIG, ENCRYPT_LEVELS, HEADERS } from './utils/cryptoConfig';

/**
 * 加密请求类
 * 继承原有axios实例，实现请求和响应加密
 */
class SecureAxios {
  constructor(axiosInstance, cryptoUtil, options = {}) {
    this.axios = axiosInstance;
    this.crypto = cryptoUtil;
    this.options = {
      // 默认加密级别
      encryptLevel: options.encryptLevel || CRYPTO_CONFIG.DEFAULT_LEVEL,
      // 是否启用加密
      enableEncryption: options.enableEncryption !== false,
      // 是否启用签名
      enableSignature: options.enableSignature !== false,
      // 是否加密URL参数
      encryptParams: options.encryptParams !== false,
      // 需要加密的请求方法
      encryptMethods: options.encryptMethods || ['post', 'put', 'patch'],
      // 不需要加密的URL路径
      excludePaths: options.excludePaths || CRYPTO_CONFIG.EXCLUDE_PATHS,
      // 响应数据解密字段
      responseDataField: options.responseDataField || 'data',
      // 高级加密路径（使用3级加密）
      highSecurityPaths: options.highSecurityPaths || CRYPTO_CONFIG.HIGH_SECURITY_PATHS
    };

    // 创建拦截器
    this._setupInterceptors();
  }

  /**
   * 设置拦截器
   * @private
   */
  _setupInterceptors() {
    // 请求拦截器
    this.axios.interceptors.request.use(
      config => this._handleRequest(config),
      error => Promise.reject(error)
    );

    // 响应拦截器
    this.axios.interceptors.response.use(
      response => this._handleResponse(response),
      error => Promise.reject(error)
    );
  }

  /**
   * 处理请求配置
   * @param {Object} config - 请求配置
   * @returns {Object} 处理后的请求配置
   * @private
   */
  _handleRequest(config) {
    // 检查是否需要加密
    if (!this.options.enableEncryption || this._shouldExclude(config.url)) {
      return config;
    }

    // 生成时间戳和随机字符串
    const timestamp = this.crypto.getTimestamp();
    const nonce = this.crypto.generateNonce();

    // 确定加密级别
    const encryptLevel = this._getEncryptLevelForPath(config.url);

    // 添加安全头信息
    config.headers = config.headers || {};
    config.headers[HEADERS.TIMESTAMP] = timestamp;
    config.headers[HEADERS.NONCE] = nonce;
    config.headers[HEADERS.ENCRYPT_LEVEL] = encryptLevel;

    // 检查请求数据是否包含密码字段
    const hasPasswordField = config.data && this._containsPasswordField(config.data);
    const finalEncryptLevel = hasPasswordField ? ENCRYPT_LEVELS.HIGH : encryptLevel;

    // 处理请求数据加密
    if (config.data && this.options.encryptMethods.includes(config.method)) {
      // 加密请求数据
      const encryptedData = this.crypto.encrypt(config.data, finalEncryptLevel);
      config.data = { encrypted: encryptedData };

      // 添加签名
      if (this.options.enableSignature) {
        const signature = this.crypto.generateSignature(config.data, timestamp, nonce);
        config.headers[HEADERS.SIGNATURE] = signature;
      }

      // 如果包含密码字段，更新加密级别头信息
      if (hasPasswordField) {
        config.headers[HEADERS.ENCRYPT_LEVEL] = finalEncryptLevel;
      }
    }

    // 处理URL参数加密
    if (config.params && this.options.encryptParams) {
      const paramsEncryptLevel = this._containsPasswordField(config.params) ?
        ENCRYPT_LEVELS.HIGH : encryptLevel;
      const encryptedParams = this.crypto.encrypt(config.params, paramsEncryptLevel);
      config.params = { encrypted: encryptedParams };
    }

    return config;
  }

  /**
   * 处理响应数据
   * @param {Object} response - 响应对象
   * @returns {Object} 处理后的响应对象
   * @private
   */
  _handleResponse(response) {
    // 检查是否需要解密
    if (!this.options.enableEncryption || this._shouldExclude(response.config.url)) {
      return response;
    }

    // 从响应头获取加密级别
    const encryptLevel = response.headers && response.headers[HEADERS.ENCRYPT_LEVEL.toLowerCase()]
      ? parseInt(response.headers[HEADERS.ENCRYPT_LEVEL.toLowerCase()])
      : this._getEncryptLevelForPath(response.config.url);

    // 检查响应数据是否加密
    if (response.data && response.data.encrypted) {
      // 解密响应数据
      const decryptedData = this.crypto.decrypt(response.data.encrypted, encryptLevel);

      // 替换加密数据
      if (decryptedData !== null) {
        response.data = decryptedData;
      }
    } else if (response.data && response.data[this.options.responseDataField] &&
               typeof response.data[this.options.responseDataField] === 'string') {
      // 如果响应数据中的特定字段是字符串，尝试解密
      try {
        const decryptedData = this.crypto.decrypt(
          response.data[this.options.responseDataField],
          encryptLevel
        );

        if (decryptedData !== null) {
          response.data[this.options.responseDataField] = decryptedData;
        }
      } catch (error) {
        console.warn('响应数据解密失败，返回原始数据', error);
      }
    }

    return response;
  }

  /**
   * 检查URL是否在排除列表中
   * @param {String} url - 请求URL
   * @returns {Boolean} 是否排除
   * @private
   */
  _shouldExclude(url) {
    if (!url) return false;
    return this.options.excludePaths.some(path => url.includes(path));
  }

  /**
   * 获取URL对应的加密级别
   * @param {String} url - 请求URL
   * @returns {Number} 加密级别
   * @private
   */
  _getEncryptLevelForPath(url) {
    if (!url) return this.options.encryptLevel;

    // 检查是否是高安全级别路径
    if (this.options.highSecurityPaths.some(path => url.includes(path))) {
      return ENCRYPT_LEVELS.HIGH;
    }

    return ENCRYPT_LEVELS.LOW; // 默认使用1级加密
  }

  /**
   * 检查对象是否包含密码相关字段
   * @param {Object} data - 要检查的数据
   * @returns {Boolean} 是否包含密码字段
   * @private
   */
  _containsPasswordField(data) {
    if (!data || typeof data !== 'object') return false;

    const passwordFields = [
      'password', 'pwd', 'pass', 'secret',
      'current_password', 'new_password',
      'password_confirmation', 'passwordConfirmation',
      'currentPassword', 'newPassword'
    ];

    return Object.keys(data).some(key => {
      // 检查键名是否包含密码关键词
      if (passwordFields.some(field => key.toLowerCase().includes(field.toLowerCase()))) {
        return true;
      }

      // 递归检查嵌套对象
      if (data[key] && typeof data[key] === 'object' && !Array.isArray(data[key])) {
        return this._containsPasswordField(data[key]);
      }

      return false;
    });
  }

  /**
   * 设置加密选项
   * @param {Object} options - 加密选项
   */
  setOptions(options) {
    this.options = { ...this.options, ...options };
  }

  /**
   * 启用或禁用加密
   * @param {Boolean} enabled - 是否启用
   */
  setEncryption(enabled) {
    this.options.enableEncryption = enabled;
  }

  /**
   * 设置加密级别
   * @param {Number} level - 加密级别
   */
  setEncryptLevel(level) {
    if (level > CRYPTO_CONFIG.MAX_LEVEL) {
      level = CRYPTO_CONFIG.MAX_LEVEL;
    } else if (level < 0) {
      level = ENCRYPT_LEVELS.NONE;
    }
    this.options.encryptLevel = level;
  }

  // 代理原始axios方法
  get(url, config) {
    return this.axios.get(url, config);
  }

  post(url, data, config) {
    return this.axios.post(url, data, config);
  }

  put(url, data, config) {
    return this.axios.put(url, data, config);
  }

  delete(url, config) {
    return this.axios.delete(url, config);
  }

  patch(url, data, config) {
    return this.axios.patch(url, data, config);
  }

  head(url, config) {
    return this.axios.head(url, config);
  }

  options(url, config) {
    return this.axios.options(url, config);
  }

  request(config) {
    return this.axios.request(config);
  }
}

// 创建加密请求实例
const secureAxios = new SecureAxios(axios, crypto, {
  encryptLevel: ENCRYPT_LEVELS.LOW, // 默认使用1级加密
  highSecurityPaths: CRYPTO_CONFIG.HIGH_SECURITY_PATHS, // 使用配置文件中的高安全路径
  excludePaths: CRYPTO_CONFIG.EXCLUDE_PATHS // 使用配置文件中的排除路径
});

export default secureAxios;
