/**
 * 加密配置常量
 */
export const CRYPTO_CONFIG = {
  // 加密密钥（生产环境应从环境变量获取）
  KEY: import.meta.env.VITE_CRYPTO_KEY || 'yuanyuzhou-metaverse-platform-secure-key',

  // 初始化向量（生产环境应从环境变量获取）
  IV: import.meta.env.VITE_CRYPTO_IV || 'metaverse-iv-16ch',

  // 传输层密钥（不同于应用层密钥）
  TRANSPORT_KEY: import.meta.env.VITE_TRANSPORT_KEY || 'transport-layer-secure-key-2024',

  // 密钥迭代次数
  ITERATIONS: 1000,

  // 密钥大小（256位）
  KEY_SIZE: 256 / 32,

  // 默认加密级别
  DEFAULT_LEVEL: 1,

  // 最大加密级别
  MAX_LEVEL: 3,

  // 加密方法
  METHODS: {
    AES: 'AES',
    DES: 'DES',
    TRIPLE_DES: '3DES'
  },

  // 签名方法
  SIGN_METHODS: {
    MD5: 'MD5',
    SHA1: 'SHA1',
    SHA256: 'SHA256'
  },

  // 默认不加密的路径
  EXCLUDE_PATHS: [
    '/auth/login',
    '/auth/register',
    '/auth/refresh',
    '/auth/logout',
    '/public/'
  ],

  // 高安全级别路径（使用3级加密）
  HIGH_SECURITY_PATHS: [
    // 密码相关
    '/auth/change-password',
    '/auth/reset-password',
    '/auth/password',
    '/auth/2fa',
    '/users/password',
    // 支付相关
    '/payment',
    '/billing',
    '/subscription',
    // 敏感信息相关
    '/user/identity',
    '/user/verification',
    '/admin/users'
  ]
};

/**
 * 加密级别配置
 */
export const ENCRYPT_LEVELS = {
  // 不加密
  NONE: 0,

  // 低级加密（单层加密）
  LOW: 1,

  // 中级加密（双层加密）
  MEDIUM: 2,

  // 高级加密（三层加密）
  HIGH: 3
};

/**
 * 请求头常量
 */
export const HEADERS = {
  // 时间戳请求头
  TIMESTAMP: 'X-Timestamp',

  // 随机字符串请求头
  NONCE: 'X-Nonce',

  // 签名请求头
  SIGNATURE: 'X-Signature',

  // 加密级别请求头
  ENCRYPT_LEVEL: 'X-Encrypt-Level',

  // 加密方法请求头
  ENCRYPT_METHOD: 'X-Encrypt-Method'
};

export default {
  CRYPTO_CONFIG,
  ENCRYPT_LEVELS,
  HEADERS
};
