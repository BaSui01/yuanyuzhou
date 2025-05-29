/**
 * 安全传输层整合模块
 * 将传输层加密与HTTP请求无缝集成
 */

import axios from 'axios';
import { TransportEncryption } from './transportEncryption';
import { CryptoUtil } from './utils/crypto';
import { CRYPTO_CONFIG, ENCRYPT_LEVELS } from './utils/cryptoConfig';

/**
 * 安全传输层类
 * 提供端到端加密的HTTP传输功能
 */
export class SecureTransport {
  constructor(options = {}) {
    this.config = {
      baseURL: options.baseURL || '/api',
      timeout: options.timeout || 30000,
      enableTransportEncryption: options.enableTransportEncryption !== false,
      enableApplicationEncryption: options.enableApplicationEncryption !== false,
      defaultEncryptLevel: options.defaultEncryptLevel || ENCRYPT_LEVELS.MEDIUM,
      clientId: options.clientId || this.generateClientId(),
      retryAttempts: options.retryAttempts || 3,
      retryDelay: options.retryDelay || 1000
    };

    // 传输层加密实例
    this.transportEncryption = new TransportEncryption(options.transportOptions);

    // 应用层加密实例
    this.crypto = new CryptoUtil();

    // 当前会话信息
    this.sessionInfo = null;

    // 请求序列号
    this.sequenceNumber = 0;

    // 创建axios实例
    this.httpClient = axios.create({
      baseURL: this.config.baseURL,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
        'X-Client-ID': this.config.clientId
      }
    });

    // 设置请求和响应拦截器
    this.setupInterceptors();

    // 初始化会话
    this.initializeSession();
  }

  /**
   * 生成客户端ID
   * @returns {String} 客户端ID
   */
  generateClientId() {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2);
    return `client_${timestamp}_${random}`;
  }

  /**
   * 初始化安全会话
   */
  async initializeSession() {
    if (!this.config.enableTransportEncryption) {
      return;
    }

    try {
      // 生成客户端临时密钥对
      const clientPrivateKey = CryptoJS.lib.WordArray.random(32);
      const clientPublicKey = CryptoJS.SHA256(clientPrivateKey.toString()).toString();

      // 执行密钥交换
      const sessionInfo = this.transportEncryption.keyExchange(clientPublicKey, this.config.clientId);

      this.sessionInfo = {
        ...sessionInfo,
        clientPrivateKey,
        clientPublicKey
      };

      console.log(`[安全传输] 会话已建立`, {
        sessionId: this.sessionInfo.sessionId.substring(0, 8) + '...',
        expiresAt: new Date(this.sessionInfo.expiresAt).toLocaleString()
      });

    } catch (error) {
      console.error('会话初始化失败:', error);
    }
  }

  /**
   * 设置请求和响应拦截器
   */
  setupInterceptors() {
    // 请求拦截器
    this.httpClient.interceptors.request.use(
      async (config) => {
        return await this.encryptRequest(config);
      },
      (error) => {
        console.error('请求配置错误:', error);
        return Promise.reject(error);
      }
    );

    // 响应拦截器
    this.httpClient.interceptors.response.use(
      async (response) => {
        return await this.decryptResponse(response);
      },
      async (error) => {
        return await this.handleResponseError(error);
      }
    );
  }

  /**
   * 加密请求数据
   * @param {Object} config - axios配置对象
   * @returns {Object} 加密后的配置对象
   */
  async encryptRequest(config) {
    try {
      // 添加请求元数据
      const requestId = this.crypto.generateNonce(8);
      const timestamp = this.crypto.getTimestamp();
      this.sequenceNumber++;

      config.metadata = {
        requestId,
        timestamp,
        sequence: this.sequenceNumber,
        clientId: this.config.clientId
      };

      // 设置请求头
      config.headers['X-Request-ID'] = requestId;
      config.headers['X-Timestamp'] = timestamp;
      config.headers['X-Sequence'] = this.sequenceNumber;

      // 应用层加密（如果启用且有数据）
      if (this.config.enableApplicationEncryption && config.data) {
        const encryptLevel = config.encryptLevel || this.config.defaultEncryptLevel;

        if (encryptLevel > ENCRYPT_LEVELS.NONE) {
          config.data = {
            encrypted_data: this.crypto.encrypt(config.data, encryptLevel),
            encrypt_level: encryptLevel,
            encrypted: true
          };

          console.log(`[应用加密] 数据已加密`, {
            requestId,
            level: encryptLevel,
            originalSize: JSON.stringify(config.data).length
          });
        }
      }

      // 传输层加密（如果启用且有会话）
      if (this.config.enableTransportEncryption && this.sessionInfo) {
        const payload = {
          url: config.url,
          method: config.method,
          headers: config.headers,
          data: config.data,
          params: config.params
        };

        const transportPacket = this.transportEncryption.encryptTransport(
          payload,
          this.sessionInfo.sessionId,
          { sequence: this.sequenceNumber }
        );

        // 将传输包作为请求体
        config.data = transportPacket;
        config.headers['X-Transport-Encrypted'] = 'true';
        config.headers['X-Session-ID'] = this.sessionInfo.sessionId;
      }

      return config;

    } catch (error) {
      console.error('请求加密失败:', error);
      throw error;
    }
  }

  /**
   * 解密响应数据
   * @param {Object} response - axios响应对象
   * @returns {Object} 解密后的响应对象
   */
  async decryptResponse(response) {
    try {
      const { config } = response;

      // 传输层解密
      if (this.config.enableTransportEncryption &&
          response.headers['x-transport-encrypted'] === 'true') {

        const decryptedResult = this.transportEncryption.decryptTransport(response.data);
        response.data = decryptedResult.payload;

        console.log(`[传输解密] 响应已解密`, {
          requestId: config.metadata?.requestId,
          sequence: decryptedResult.metadata?.sequence
        });
      }

      // 应用层解密
      if (this.config.enableApplicationEncryption &&
          response.data &&
          response.data.encrypted === true) {

        const { encrypted_data, encrypt_level } = response.data;
        const decryptedData = this.crypto.decrypt(encrypted_data, encrypt_level);

        response.data = decryptedData;

        console.log(`[应用解密] 响应已解密`, {
          requestId: config.metadata?.requestId,
          level: encrypt_level
        });
      }

      return response;

    } catch (error) {
      console.error('响应解密失败:', error);
      throw error;
    }
  }

  /**
   * 处理响应错误
   * @param {Object} error - 错误对象
   * @returns {Promise} 处理后的错误
   */
  async handleResponseError(error) {
    const { config } = error;

    // 如果是会话过期错误，尝试重新建立会话
    if (error.response && error.response.status === 401 &&
        error.response.data && error.response.data.code === 'SESSION_EXPIRED') {

      console.log('[安全传输] 会话已过期，正在重新建立会话...');

      try {
        await this.initializeSession();

        // 重试请求（最多重试指定次数）
        if (!config._retryCount) {
          config._retryCount = 0;
        }

        if (config._retryCount < this.config.retryAttempts) {
          config._retryCount++;

          // 延迟后重试
          await new Promise(resolve => setTimeout(resolve, this.config.retryDelay));

          return this.httpClient.request(config);
        }
      } catch (retryError) {
        console.error('会话重建失败:', retryError);
      }
    }

    return Promise.reject(error);
  }

  /**
   * GET 请求
   * @param {String} url - 请求URL
   * @param {Object} params - 查询参数
   * @param {Object} options - 请求选项
   * @returns {Promise} 响应Promise
   */
  async get(url, params = {}, options = {}) {
    return this.httpClient.get(url, {
      params,
      ...options
    });
  }

  /**
   * POST 请求
   * @param {String} url - 请求URL
   * @param {Object} data - 请求数据
   * @param {Object} options - 请求选项
   * @returns {Promise} 响应Promise
   */
  async post(url, data = {}, options = {}) {
    return this.httpClient.post(url, data, options);
  }

  /**
   * PUT 请求
   * @param {String} url - 请求URL
   * @param {Object} data - 请求数据
   * @param {Object} options - 请求选项
   * @returns {Promise} 响应Promise
   */
  async put(url, data = {}, options = {}) {
    return this.httpClient.put(url, data, options);
  }

  /**
   * PATCH 请求
   * @param {String} url - 请求URL
   * @param {Object} data - 请求数据
   * @param {Object} options - 请求选项
   * @returns {Promise} 响应Promise
   */
  async patch(url, data = {}, options = {}) {
    return this.httpClient.patch(url, data, options);
  }

  /**
   * DELETE 请求
   * @param {String} url - 请求URL
   * @param {Object} params - 查询参数
   * @param {Object} options - 请求选项
   * @returns {Promise} 响应Promise
   */
  async delete(url, params = {}, options = {}) {
    return this.httpClient.delete(url, {
      params,
      ...options
    });
  }

  /**
   * 文件上传
   * @param {String} url - 上传URL
   * @param {File|FormData} file - 文件或FormData
   * @param {Object} options - 上传选项
   * @returns {Promise} 上传Promise
   */
  async upload(url, file, options = {}) {
    const formData = file instanceof FormData ? file : new FormData();

    if (!(file instanceof FormData)) {
      formData.append('file', file);
    }

    return this.httpClient.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: options.onProgress,
      ...options
    });
  }

  /**
   * 设置加密级别
   * @param {Number} level - 加密级别
   */
  setEncryptLevel(level) {
    this.config.defaultEncryptLevel = level;
  }

  /**
   * 启用/禁用传输层加密
   * @param {Boolean} enabled - 是否启用
   */
  setTransportEncryption(enabled) {
    this.config.enableTransportEncryption = enabled;

    if (enabled && !this.sessionInfo) {
      this.initializeSession();
    }
  }

  /**
   * 启用/禁用应用层加密
   * @param {Boolean} enabled - 是否启用
   */
  setApplicationEncryption(enabled) {
    this.config.enableApplicationEncryption = enabled;
  }

  /**
   * 获取会话信息
   * @returns {Object|null} 会话信息
   */
  getSessionInfo() {
    return this.sessionInfo;
  }

  /**
   * 重置会话
   */
  async resetSession() {
    if (this.sessionInfo) {
      this.transportEncryption.revokeSession(this.sessionInfo.sessionId);
    }

    this.sessionInfo = null;
    this.sequenceNumber = 0;

    await this.initializeSession();
  }

  /**
   * 获取传输统计信息
   * @returns {Object} 统计信息
   */
  getStatistics() {
    return {
      ...this.transportEncryption.getStatistics(),
      sessionInfo: this.sessionInfo ? {
        sessionId: this.sessionInfo.sessionId,
        expiresAt: this.sessionInfo.expiresAt,
        isValid: Date.now() < this.sessionInfo.expiresAt
      } : null,
      sequenceNumber: this.sequenceNumber,
      config: {
        enableTransportEncryption: this.config.enableTransportEncryption,
        enableApplicationEncryption: this.config.enableApplicationEncryption,
        defaultEncryptLevel: this.config.defaultEncryptLevel
      }
    };
  }
}

// 创建默认实例
const secureTransport = new SecureTransport();

// 导出类和默认实例
export { SecureTransport };
export default secureTransport;
