import CryptoJS from 'crypto-js';
import { CRYPTO_CONFIG, ENCRYPT_LEVELS } from './cryptoConfig';

/**
 * 加密工具类
 * 提供数据加密解密功能
 */
export class CryptoUtil {
  constructor(options = {}) {
    // 默认加密配置
    this.config = {
      key: options.key || CRYPTO_CONFIG.KEY,
      iv: options.iv || CRYPTO_CONFIG.IV,
      iterations: options.iterations || CRYPTO_CONFIG.ITERATIONS,
      keySize: options.keySize || CRYPTO_CONFIG.KEY_SIZE,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    };
  }

  /**
   * 生成加密密钥
   * @returns {Object} 密钥对象
   */
  generateKey() {
    const salt = CryptoJS.lib.WordArray.random(128 / 8);
    const key = CryptoJS.PBKDF2(
      this.config.key,
      salt,
      {
        keySize: this.config.keySize,
        iterations: this.config.iterations
      }
    );
    const iv = CryptoJS.enc.Utf8.parse(this.config.iv);

    return { key, iv, salt };
  }

  /**
   * 加密数据
   * @param {Object|String} data - 要加密的数据
   * @param {Number} level - 加密嵌套层级（默认为1）
   * @returns {String} 加密后的字符串
   */
  encrypt(data, level = ENCRYPT_LEVELS.LOW) {
    try {
      // 检查加密级别是否有效
      if (level > CRYPTO_CONFIG.MAX_LEVEL) {
        level = CRYPTO_CONFIG.MAX_LEVEL;
      } else if (level < 0) {
        level = 0;
      }

      // 如果加密级别为0，则不加密
      if (level === ENCRYPT_LEVELS.NONE) {
        return typeof data === 'object' ? JSON.stringify(data) : String(data);
      }

      // 将对象转为JSON字符串
      const jsonStr = typeof data === 'object' ? JSON.stringify(data) : String(data);

      // 根据嵌套层级进行多次加密
      let encrypted = jsonStr;
      for (let i = 0; i < level; i++) {
        const { key, iv, salt } = this.generateKey();

        // 加密数据
        const ciphertext = CryptoJS.AES.encrypt(encrypted, key, {
          iv: iv,
          mode: this.config.mode,
          padding: this.config.padding
        }).toString();

        // 将salt和密文组合，以便解密时使用
        const saltHex = CryptoJS.enc.Hex.stringify(salt);
        encrypted = `${saltHex}:${ciphertext}`;
      }

      return encrypted;
    } catch (error) {
      console.error('加密失败:', error);
      return data;
    }
  }

  /**
   * 解密数据
   * @param {String} encryptedData - 加密的数据
   * @param {Number} level - 解密嵌套层级（默认为1）
   * @returns {Object|String} 解密后的数据
   */
  decrypt(encryptedData, level = ENCRYPT_LEVELS.LOW) {
    try {
      if (!encryptedData) return null;

      // 检查加密级别是否有效
      if (level > CRYPTO_CONFIG.MAX_LEVEL) {
        level = CRYPTO_CONFIG.MAX_LEVEL;
      } else if (level < 0) {
        level = 0;
      }

      // 如果加密级别为0，则不解密
      if (level === ENCRYPT_LEVELS.NONE) {
        try {
          return JSON.parse(encryptedData);
        } catch (e) {
          return encryptedData;
        }
      }

      // 根据嵌套层级进行多次解密
      let decrypted = encryptedData;
      for (let i = 0; i < level; i++) {
        // 分离salt和密文
        const [saltHex, ciphertext] = decrypted.split(':');
        if (!saltHex || !ciphertext) {
          throw new Error('加密数据格式不正确');
        }

        // 从十六进制字符串恢复salt
        const salt = CryptoJS.enc.Hex.parse(saltHex);

        // 生成解密密钥
        const key = CryptoJS.PBKDF2(
          this.config.key,
          salt,
          {
            keySize: this.config.keySize,
            iterations: this.config.iterations
          }
        );
        const iv = CryptoJS.enc.Utf8.parse(this.config.iv);

        // 解密
        decrypted = CryptoJS.AES.decrypt(ciphertext, key, {
          iv: iv,
          mode: this.config.mode,
          padding: this.config.padding
        }).toString(CryptoJS.enc.Utf8);
      }

      // 尝试解析JSON
      try {
        return JSON.parse(decrypted);
      } catch (e) {
        // 如果不是JSON，则返回字符串
        return decrypted;
      }
    } catch (error) {
      console.error('解密失败:', error);
      return encryptedData;
    }
  }

  /**
   * 生成请求签名
   * @param {Object} params - 请求参数
   * @param {String} timestamp - 时间戳
   * @param {String} nonce - 随机字符串
   * @returns {String} 签名
   */
  generateSignature(params, timestamp, nonce) {
    // 排序所有参数
    const sortedKeys = Object.keys(params).sort();
    let signStr = '';

    // 拼接参数
    sortedKeys.forEach(key => {
      if (params[key] !== undefined && params[key] !== null) {
        signStr += `${key}=${params[key]}&`;
      }
    });

    // 添加时间戳和随机字符串
    signStr += `timestamp=${timestamp}&nonce=${nonce}&key=${this.config.key}`;

    // 生成签名
    return CryptoJS.MD5(signStr).toString();
  }

  /**
   * 生成随机字符串
   * @param {Number} length - 字符串长度
   * @returns {String} 随机字符串
   */
  generateNonce(length = 16) {
    return CryptoJS.lib.WordArray.random(length).toString();
  }

  /**
   * 获取当前时间戳
   * @returns {String} 时间戳
   */
  getTimestamp() {
    return Math.floor(Date.now() / 1000).toString();
  }

  /**
   * 使用SHA256哈希算法
   * @param {String} data - 要哈希的数据
   * @returns {String} 哈希结果
   */
  sha256(data) {
    return CryptoJS.SHA256(data).toString();
  }

  /**
   * 使用MD5哈希算法
   * @param {String} data - 要哈希的数据
   * @returns {String} 哈希结果
   */
  md5(data) {
    return CryptoJS.MD5(data).toString();
  }
}

// 默认导出
export default new CryptoUtil();
