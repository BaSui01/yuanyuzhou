import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import crypto from './utils/crypto';
import { CRYPTO_CONFIG, ENCRYPT_LEVELS, HEADERS } from './utils/cryptoConfig';
import { transportEncryption } from './transportEncryption';

/**
 * 安全的Axios实例
 * 自动处理传输层加密解密
 */
class SecureAxios {
  constructor() {
    // 创建axios实例
    this.instance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });

    // 加密配置
    this.encryptConfig = {
      enabled: true,
      defaultLevel: ENCRYPT_LEVELS.MEDIUM,
      excludePaths: CRYPTO_CONFIG.EXCLUDE_PATHS,
      highSecurityPaths: CRYPTO_CONFIG.HIGH_SECURITY_PATHS
    };

    // 设置拦截器
    this.setupInterceptors();
  }

  /**
   * 设置请求和响应拦截器
   */
  setupInterceptors() {
    // 请求拦截器
    this.instance.interceptors.request.use(
      async (config) => this.requestInterceptor(config),
      (error) => this.requestErrorHandler(error)
    );

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response) => this.responseInterceptor(response),
      (error) => this.responseErrorHandler(error)
    );
  }

  /**
   * 请求拦截器处理
   */
  async requestInterceptor(config) {
    try {
      // 获取认证store
      const authStore = useAuthStore();
      const token = authStore.token;

      // 添加认证token
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }

      // 生成请求标识
      const timestamp = crypto.getTimestamp();
      const nonce = crypto.generateNonce();

      // 添加时间戳和随机字符串
      config.headers[HEADERS.TIMESTAMP] = timestamp;
      config.headers[HEADERS.NONCE] = nonce;

      // 确定加密级别
      const encryptLevel = this.determineEncryptLevel(config.url);
      config.headers[HEADERS.ENCRYPT_LEVEL] = encryptLevel;
      config.headers[HEADERS.ENCRYPT_METHOD] = CRYPTO_CONFIG.METHODS.AES;

      // 如果启用加密且不在排除列表中
      if (this.encryptConfig.enabled && !this.isExcludedPath(config.url)) {
        // 确保会话有效
        if (!transportEncryption.isSessionValid()) {
          await transportEncryption.createSession();
        }

        // 获取请求数据
        const data = config.data || {};

        // 加密数据
        const encryptedPacket = await transportEncryption.encryptTransport(data);

        // 更新请求配置
        config.data = encryptedPacket;
        config.headers['X-Transport-Encrypted'] = 'true';
      }

      // 添加请求ID用于调试
      config.metadata = {
        requestId: crypto.generateNonce(8),
        timestamp: timestamp,
        encryptLevel: encryptLevel
      };

      console.log(`[安全请求] ${config.method?.toUpperCase()} ${config.url}`, {
        requestId: config.metadata.requestId,
        encryptLevel: encryptLevel,
        encrypted: this.encryptConfig.enabled && !this.isExcludedPath(config.url)
      });

      return config;
    } catch (error) {
      console.error('请求加密失败:', error);
      return Promise.reject(error);
    }
  }

  /**
   * 响应拦截器处理
   */
  responseInterceptor(response) {
    try {
      const config = response.config;
      const encryptLevel = parseInt(config.headers[HEADERS.ENCRYPT_LEVEL]) || 0;

      console.log(`[安全响应] ${response.status} ${config.url}`, {
        requestId: config.metadata?.requestId,
        encrypted: response.data.encrypted_data ? true : false
      });

      // 如果响应数据被加密，进行解密
      if (response.data && response.data.encrypted_data) {
        const decryptedData = crypto.decrypt(response.data.encrypted_data, encryptLevel);
        response.data = decryptedData;
      }

      // 检查是否需要解密
      if (response.headers['x-transport-encrypted'] === 'true') {
        // 解密响应数据
        const encryptedPacket = response.data;
        const decryptedData = transportEncryption.decryptTransport(encryptedPacket);

        // 更新响应数据
        response.data = decryptedData.payload;
      }

      return response.data;
    } catch (error) {
      console.error('响应解密失败:', error);
      return response.data;
    }
  }

  /**
   * 请求错误处理
   */
  requestErrorHandler(error) {
    console.error('请求配置错误:', error);
    return Promise.reject(error);
  }

  /**
   * 响应错误处理
   */
  responseErrorHandler(error) {
    const authStore = useAuthStore();

    if (error.response) {
      const { status, data } = error.response;
      const config = error.config;

      console.error(`[安全请求错误] ${status} ${config?.url}`, {
        requestId: config?.metadata?.requestId,
        error: data
      });

      // 处理401未授权错误
      if (status === 401) {
        console.warn('认证失败，清除本地token');
        authStore.logout();

        // 重定向到登录页面（避免无限循环）
        if (!window.location.pathname.includes('/auth/')) {
          window.location.href = '/auth/login';
        }
      }

      // 处理403权限不足错误
      if (status === 403) {
        console.warn('权限不足，无法访问该资源');
      }

      // 处理422表单验证错误
      if (status === 422 && data.errors) {
        console.warn('表单验证失败:', data.errors);
      }

      // 处理429频率限制错误
      if (status === 429) {
        console.warn('请求频率过高，请稍后再试');
      }

      // 处理500服务器错误
      if (status >= 500) {
        console.error('服务器内部错误');
      }

      return Promise.reject({
        status,
        message: data?.message || this.getStatusMessage(status),
        errors: data?.errors || {},
        data: data
      });
    }

    // 处理网络错误
    if (error.code === 'ECONNABORTED') {
      return Promise.reject({
        status: 408,
        message: '请求超时，请检查网络连接',
        code: 'TIMEOUT'
      });
    }

    if (!window.navigator.onLine) {
      return Promise.reject({
        status: -1,
        message: '网络连接已断开，请检查网络设置',
        code: 'OFFLINE'
      });
    }

    return Promise.reject({
      status: -1,
      message: error.message || '未知网络错误',
      code: 'UNKNOWN'
    });
  }

  /**
   * 确定加密级别
   */
  determineEncryptLevel(url) {
    if (!this.encryptConfig.enabled) {
      return ENCRYPT_LEVELS.NONE;
    }

    // 检查是否是高安全级别路径
    if (this.isHighSecurityPath(url)) {
      return ENCRYPT_LEVELS.HIGH;
    }

    // 检查是否是排除路径
    if (this.isExcludedPath(url)) {
      return ENCRYPT_LEVELS.LOW;
    }

    return this.encryptConfig.defaultLevel;
  }

  /**
   * 检查是否是排除路径
   */
  isExcludedPath(url) {
    return this.encryptConfig.excludePaths.some(path =>
      url.includes(path)
    );
  }

  /**
   * 检查是否是高安全级别路径
   */
  isHighSecurityPath(url) {
    return this.encryptConfig.highSecurityPaths.some(path =>
      url.includes(path)
    );
  }

  /**
   * 获取状态码对应的消息
   */
  getStatusMessage(status) {
    const messages = {
      400: '请求参数错误',
      401: '认证失败，请重新登录',
      403: '权限不足，无法访问',
      404: '请求的资源不存在',
      405: '请求方法不被允许',
      408: '请求超时',
      422: '表单验证失败',
      429: '请求频率过高，请稍后再试',
      500: '服务器内部错误',
      502: '网关错误',
      503: '服务暂时不可用',
      504: '网关超时'
    };

    return messages[status] || '请求失败';
  }

  /**
   * 设置加密级别
   */
  setEncryptLevel(level) {
    this.encryptConfig.defaultLevel = level;
  }

  /**
   * 启用或禁用加密
   */
  setEncryption(enabled) {
    this.encryptConfig.enabled = enabled;
  }

  /**
   * GET请求
   */
  get(url, config = {}) {
    return this.instance.get(url, config);
  }

  /**
   * POST请求
   */
  post(url, data = {}, config = {}) {
    return this.instance.post(url, data, config);
  }

  /**
   * PUT请求
   */
  put(url, data = {}, config = {}) {
    return this.instance.put(url, data, config);
  }

  /**
   * DELETE请求
   */
  delete(url, config = {}) {
    return this.instance.delete(url, config);
  }

  /**
   * PATCH请求
   */
  patch(url, data = {}, config = {}) {
    return this.instance.patch(url, data, config);
  }

  /**
   * 获取原始axios实例
   */
  getInstance() {
    return this.instance;
  }
}

// 创建并导出默认实例
const secureAxios = new SecureAxios();
export default secureAxios;
