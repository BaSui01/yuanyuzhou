/**
 * 传输层加密模块
 * 实现与后端对应的加密解密功能
 */

import CryptoJS from 'crypto-js'
import { v4 as uuidv4 } from 'uuid'
import JSEncrypt from 'jsencrypt'
import pako from 'pako'

/**
 * 传输加密配置
 */
export const TransportEncryptionConfig = {
  // 会话密钥生存时间（秒）
  SESSION_KEY_TTL: 300, // 5分钟

  // 时间窗口容忍度（秒）
  TIME_WINDOW: 30,

  // 启用防重放攻击
  ANTI_REPLAY: true,

  // 启用完整性校验
  INTEGRITY_CHECK: true,

  // 压缩阈值（字节）
  COMPRESSION_THRESHOLD: 1024,

  // 客户端ID（随机生成）
  CLIENT_ID: localStorage.getItem('client_id') || (() => {
    const id = uuidv4()
    localStorage.setItem('client_id', id)
    return id
  })()
}

/**
 * 高级加密工具类
 */
export class AdvancedCryptoUtils {
  /**
   * RSA加密
   * @param {string} data - 要加密的数据
   * @param {string} publicKey - PEM格式的公钥
   * @returns {string} - Base64编码的加密数据
   */
  static rsaEncrypt(data, publicKey) {
    const encrypt = new JSEncrypt()
    encrypt.setPublicKey(publicKey)
    return encrypt.encrypt(data)
  }

  /**
   * RSA解密
   * @param {string} encryptedData - Base64编码的加密数据
   * @param {string} privateKey - PEM格式的私钥
   * @returns {string} - 解密后的数据
   */
  static rsaDecrypt(encryptedData, privateKey) {
    const decrypt = new JSEncrypt()
    decrypt.setPrivateKey(privateKey)
    return decrypt.decrypt(encryptedData)
  }

  /**
   * 生成随机字节
   * @param {number} length - 字节长度
   * @returns {string} - Base64编码的随机字节
   */
  static generateRandomBytes(length) {
    const array = new Uint8Array(length)
    window.crypto.getRandomValues(array)
    return this.arrayBufferToBase64(array.buffer)
  }

  /**
   * 派生密钥
   * @param {string} password - 密码
   * @param {string} salt - Base64编码的盐
   * @param {number} iterations - 迭代次数
   * @param {number} keySize - 密钥大小（字节）
   * @returns {string} - 派生的密钥（Hex格式）
   */
  static deriveKey(password, salt, iterations = 100000, keySize = 32) {
    const saltBytes = this.base64ToArrayBuffer(salt)
    const key = CryptoJS.PBKDF2(password, CryptoJS.lib.WordArray.create(saltBytes), {
      keySize: keySize / 4, // 转换为32位字长度
      iterations: iterations,
      hasher: CryptoJS.algo.SHA256
    })
    return key.toString(CryptoJS.enc.Hex)
  }

  /**
   * AES-GCM加密
   * @param {string|object} data - 要加密的数据
   * @param {string} key - Hex格式的密钥
   * @returns {object} - 加密结果，包含密文、IV和认证标签
   */
  static aesEncryptGCM(data, key) {
    // 准备数据
    const dataString = typeof data === 'string' ? data : JSON.stringify(data)
    const iv = this.generateRandomBytes(12)
    const ivWordArray = CryptoJS.enc.Base64.parse(iv)
    const keyWordArray = CryptoJS.enc.Hex.parse(key)

    // 加密
    const encrypted = CryptoJS.AES.encrypt(dataString, keyWordArray, {
      iv: ivWordArray,
      mode: CryptoJS.mode.GCM,
      padding: CryptoJS.pad.NoPadding
    })

    // 获取密文和认证标签
    const ciphertext = encrypted.ciphertext.toString(CryptoJS.enc.Base64)
    const tag = encrypted.tag.toString(CryptoJS.enc.Base64)

    return {
      ciphertext: ciphertext,
      iv: iv,
      tag: tag
    }
  }

  /**
   * AES-GCM解密
   * @param {object} encryptedData - 加密数据，包含密文、IV和认证标签
   * @param {string} key - Hex格式的密钥
   * @returns {string|object} - 解密后的数据
   */
  static aesDecryptGCM(encryptedData, key) {
    const { ciphertext, iv, tag } = encryptedData
    const keyWordArray = CryptoJS.enc.Hex.parse(key)
    const ivWordArray = CryptoJS.enc.Base64.parse(iv)
    const ciphertextWordArray = CryptoJS.enc.Base64.parse(ciphertext)

    // 创建加密对象
    const encrypted = CryptoJS.lib.CipherParams.create({
      ciphertext: ciphertextWordArray,
      iv: ivWordArray,
      tag: CryptoJS.enc.Base64.parse(tag)
    })

    // 解密
    const decrypted = CryptoJS.AES.decrypt(encrypted, keyWordArray, {
      iv: ivWordArray,
      mode: CryptoJS.mode.GCM,
      padding: CryptoJS.pad.NoPadding
    })

    // 转换为字符串
    const decryptedString = decrypted.toString(CryptoJS.enc.Utf8)

    // 尝试解析JSON
    try {
      return JSON.parse(decryptedString)
    } catch (e) {
      return decryptedString
    }
  }

  /**
   * 生成HMAC签名
   * @param {string} data - 要签名的数据
   * @param {string} key - Hex格式的密钥
   * @returns {string} - 签名（Hex格式）
   */
  static generateHmac(data, key) {
    const keyWordArray = CryptoJS.enc.Hex.parse(key)
    return CryptoJS.HmacSHA256(data, keyWordArray).toString(CryptoJS.enc.Hex)
  }

  /**
   * 验证HMAC签名
   * @param {string} data - 要验证的数据
   * @param {string} signature - Hex格式的签名
   * @param {string} key - Hex格式的密钥
   * @returns {boolean} - 验证结果
   */
  static verifyHmac(data, signature, key) {
    const expectedSignature = this.generateHmac(data, key)
    return expectedSignature === signature
  }

  /**
   * ArrayBuffer转Base64
   * @param {ArrayBuffer} buffer - ArrayBuffer
   * @returns {string} - Base64编码的字符串
   */
  static arrayBufferToBase64(buffer) {
    const binary = String.fromCharCode.apply(null, new Uint8Array(buffer))
    return window.btoa(binary)
  }

  /**
   * Base64转ArrayBuffer
   * @param {string} base64 - Base64编码的字符串
   * @returns {ArrayBuffer} - ArrayBuffer
   */
  static base64ToArrayBuffer(base64) {
    const binary = window.atob(base64)
    const bytes = new Uint8Array(binary.length)
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i)
    }
    return bytes.buffer
  }
}

/**
 * 传输层加密服务
 */
export class TransportEncryptionService {
  constructor() {
    this.config = TransportEncryptionConfig
    this.sessionInfo = null
    this.sequence = 0
  }

  /**
   * 创建加密会话
   * @returns {Promise<object>} - 会话信息
   */
  async createSession() {
    try {
      // 请求创建会话
      const response = await fetch('/api/v1/core/encryption/session/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          client_id: this.config.CLIENT_ID,
          timestamp: Math.floor(Date.now() / 1000)
        })
      })

      if (!response.ok) {
        throw new Error(`创建会话失败: ${response.status}`)
      }

      // 解析会话信息
      const sessionData = await response.json()
      this.sessionInfo = {
        session_id: sessionData.session_id,
        server_public_key: sessionData.server_public_key,
        expires_at: sessionData.expires_at,
        key_hash: sessionData.key_hash,
        created_at: Math.floor(Date.now() / 1000)
      }

      console.log('加密会话已创建:', this.sessionInfo.session_id)
      return this.sessionInfo
    } catch (error) {
      console.error('创建加密会话失败:', error)
      throw error
    }
  }

  /**
   * 加密传输数据
   * @param {object} payload - 要加密的数据
   * @returns {Promise<object>} - 加密后的传输包
   */
  async encryptTransport(payload) {
    // 检查会话是否有效
    if (!this.isSessionValid()) {
      await this.createSession()
    }

    // 增加序列号
    this.sequence += 1

    // 生成传输包元数据
    const timestamp = Math.floor(Date.now() / 1000)
    const nonce = AdvancedCryptoUtils.generateRandomBytes(12)

    // 准备传输数据
    const transportData = {
      payload,
      timestamp,
      nonce,
      sequence: this.sequence,
      version: '2.0'
    }

    // 序列化数据
    const serializedData = JSON.stringify(transportData)
    let dataToEncrypt
    let compressed = false

    // 数据压缩（如果需要）
    if (serializedData.length > this.config.COMPRESSION_THRESHOLD) {
      const compressedData = pako.deflate(serializedData)
      dataToEncrypt = AdvancedCryptoUtils.arrayBufferToBase64(compressedData.buffer)
      compressed = true
    } else {
      dataToEncrypt = serializedData
    }

    // 使用会话密钥加密
    const sessionKey = this.deriveSessionKey()
    const encryptedResult = AdvancedCryptoUtils.aesEncryptGCM(dataToEncrypt, sessionKey)

    // 生成完整性校验
    let hmacSignature = ''
    if (this.config.INTEGRITY_CHECK) {
      const hmacData = `${encryptedResult.ciphertext}:${encryptedResult.iv}:${timestamp}:${nonce}`
      const hmacKey = CryptoJS.SHA256(CryptoJS.enc.Hex.parse(sessionKey) + 'hmac').toString(CryptoJS.enc.Hex)
      hmacSignature = AdvancedCryptoUtils.generateHmac(hmacData, hmacKey)
    }

    // 构造传输包
    const transportPacket = {
      session_id: this.sessionInfo.session_id,
      data: encryptedResult.ciphertext,
      iv: encryptedResult.iv,
      tag: encryptedResult.tag,
      timestamp,
      nonce,
      sequence: this.sequence,
      hmac: hmacSignature,
      version: '2.0',
      compressed
    }

    return transportPacket
  }

  /**
   * 解密传输数据
   * @param {object} transportPacket - 加密的传输包
   * @returns {object} - 解密后的数据
   */
  decryptTransport(transportPacket) {
    // 检查会话ID是否匹配
    if (transportPacket.session_id !== this.sessionInfo?.session_id) {
      throw new Error('会话ID不匹配')
    }

    // 提取传输包数据
    const { data: ciphertext, iv, tag, timestamp, nonce, sequence, hmac, compressed } = transportPacket

    // 时间窗口验证
    const currentTime = Math.floor(Date.now() / 1000)
    if (Math.abs(currentTime - timestamp) > this.config.TIME_WINDOW) {
      throw new Error('传输包时间戳超出允许窗口')
    }

    // 完整性校验
    if (this.config.INTEGRITY_CHECK && hmac) {
      const sessionKey = this.deriveSessionKey()
      const hmacData = `${ciphertext}:${iv}:${timestamp}:${nonce}`
      const hmacKey = CryptoJS.SHA256(CryptoJS.enc.Hex.parse(sessionKey) + 'hmac').toString(CryptoJS.enc.Hex)

      if (!AdvancedCryptoUtils.verifyHmac(hmacData, hmac, hmacKey)) {
        throw new Error('数据完整性校验失败')
      }
    }

    // 解密数据
    const encryptedData = {
      ciphertext,
      iv,
      tag
    }

    const sessionKey = this.deriveSessionKey()
    const decryptedData = AdvancedCryptoUtils.aesDecryptGCM(encryptedData, sessionKey)

    // 数据解压缩
    if (compressed) {
      try {
        const compressedData = AdvancedCryptoUtils.base64ToArrayBuffer(decryptedData)
        const decompressedData = pako.inflate(new Uint8Array(compressedData), { to: 'string' })
        const transportData = JSON.parse(decompressedData)
        return {
          payload: transportData.payload,
          metadata: {
            timestamp: transportData.timestamp,
            nonce: transportData.nonce,
            sequence: transportData.sequence,
            version: transportData.version
          }
        }
      } catch (error) {
        throw new Error(`解压缩数据失败: ${error.message}`)
      }
    } else {
      return {
        payload: decryptedData.payload,
        metadata: {
          timestamp: decryptedData.timestamp,
          nonce: decryptedData.nonce,
          sequence: decryptedData.sequence,
          version: decryptedData.version
        }
      }
    }
  }

  /**
   * 派生会话密钥
   * @returns {string} - 会话密钥（Hex格式）
   */
  deriveSessionKey() {
    if (!this.sessionInfo) {
      throw new Error('会话未初始化')
    }

    // 使用与后端相同的密钥派生算法
    const keyMaterial = `transport-layer-secure-key-2024:${this.config.CLIENT_ID}:${this.sessionInfo.session_id}:${this.sessionInfo.created_at}`
    const salt = AdvancedCryptoUtils.generateRandomBytes(16)
    return AdvancedCryptoUtils.deriveKey(keyMaterial, salt)
  }

  /**
   * 检查会话是否有效
   * @returns {boolean} - 会话是否有效
   */
  isSessionValid() {
    if (!this.sessionInfo) {
      return false
    }

    const currentTime = Math.floor(Date.now() / 1000)
    return currentTime < this.sessionInfo.expires_at
  }

  /**
   * 撤销会话
   * @returns {Promise<boolean>} - 是否成功撤销
   */
  async revokeSession() {
    if (!this.sessionInfo) {
      return false
    }

    try {
      const response = await fetch(`/api/v1/core/encryption/session/${this.sessionInfo.session_id}/revoke/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        this.sessionInfo = null
        this.sequence = 0
        return true
      }
      return false
    } catch (error) {
      console.error('撤销会话失败:', error)
      return false
    }
  }
}

// 导出单例实例
export const transportEncryption = new TransportEncryptionService()

export default transportEncryption
