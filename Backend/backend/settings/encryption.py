"""
加密相关配置
"""

from decouple import config
import os

# 基础加密配置
CRYPTO_KEY = config('CRYPTO_KEY', default='yuanyuzhou-metaverse-platform-secure-key')
CRYPTO_IV = config('CRYPTO_IV', default='metaverse-iv-16ch')

# 传输层加密配置
TRANSPORT_KEY = config('TRANSPORT_KEY', default='transport-layer-secure-key-2024')

# 会话密钥配置
SESSION_KEY_TTL = config('SESSION_KEY_TTL', default=300, cast=int)  # 5分钟

# 时间窗口配置（秒）
TIME_WINDOW = config('TIME_WINDOW', default=30, cast=int)

# 防重放攻击
ANTI_REPLAY = config('ANTI_REPLAY', default=True, cast=bool)

# 完整性校验
INTEGRITY_CHECK = config('INTEGRITY_CHECK', default=True, cast=bool)

# 压缩阈值（字节）
COMPRESSION_THRESHOLD = config('COMPRESSION_THRESHOLD', default=1024, cast=int)

# RSA密钥长度
RSA_KEY_SIZE = config('RSA_KEY_SIZE', default=2048, cast=int)

# 加密中间件配置
ENCRYPTION_MIDDLEWARE_ENABLED = config('ENCRYPTION_MIDDLEWARE_ENABLED', default=True, cast=bool)

# 排除路径（不进行加密处理的路径）
ENCRYPTION_EXCLUDED_PATHS = [
    '/admin/',
    '/api/docs/',
    '/api/schema/',
    '/health/',
    '/api/v1/core/encryption/session/create/',  # 会话创建不需要解密
    '/api/v1/core/encryption/api/session/create/',
    '/static/',
    '/media/',
    '/favicon.ico',
]

# 高安全级别路径（使用最高级别加密）
HIGH_SECURITY_PATHS = [
    '/api/v1/auth/password',
    '/api/v1/users/password',
    '/api/v1/auth/2fa',
    '/api/v1/payment/',
    '/api/v1/billing/',
    '/api/v1/subscription/',
    '/api/v1/user/identity/',
    '/api/v1/admin/users/',
]

# 日志配置
ENCRYPTION_LOGGING = {
    'enable_debug_logs': config('ENCRYPTION_DEBUG_LOGS', default=False, cast=bool),
    'log_level': config('ENCRYPTION_LOG_LEVEL', default='INFO'),
    'log_file': config('ENCRYPTION_LOG_FILE', default=None),
}

# 性能配置
ENCRYPTION_PERFORMANCE = {
    'max_request_size': config('ENCRYPTION_MAX_REQUEST_SIZE', default=10485760, cast=int),  # 10MB
    'timeout': config('ENCRYPTION_TIMEOUT', default=30, cast=int),  # 30秒
    'max_concurrent_sessions': config('ENCRYPTION_MAX_SESSIONS', default=1000, cast=int),
}

# Redis缓存配置（用于会话和nonce存储）
ENCRYPTION_CACHE_CONFIG = {
    'session_cache_db': config('ENCRYPTION_SESSION_CACHE_DB', default=1, cast=int),
    'nonce_cache_db': config('ENCRYPTION_NONCE_CACHE_DB', default=2, cast=int),
    'cache_prefix': config('ENCRYPTION_CACHE_PREFIX', default='encrypt:'),
}

# 开发模式配置
if config('DEBUG', default=False, cast=bool):
    # 开发环境下的宽松配置
    TIME_WINDOW = 300  # 5分钟
    SESSION_KEY_TTL = 3600  # 1小时
    ENCRYPTION_LOGGING['enable_debug_logs'] = True
    ENCRYPTION_LOGGING['log_level'] = 'DEBUG'

# 密钥轮换配置
KEY_ROTATION = {
    'enabled': config('KEY_ROTATION_ENABLED', default=False, cast=bool),
    'interval_hours': config('KEY_ROTATION_INTERVAL', default=24, cast=int),
    'backup_count': config('KEY_BACKUP_COUNT', default=3, cast=int),
}

# 监控和告警配置
MONITORING = {
    'enable_metrics': config('ENCRYPTION_METRICS_ENABLED', default=True, cast=bool),
    'alert_on_failures': config('ENCRYPTION_ALERT_FAILURES', default=True, cast=bool),
    'failure_threshold': config('ENCRYPTION_FAILURE_THRESHOLD', default=10, cast=int),
    'alert_webhook': config('ENCRYPTION_ALERT_WEBHOOK', default=None),
}

# 加密算法配置
ENCRYPTION_ALGORITHMS = {
    'transport_encryption': 'AES-256-GCM',
    'application_encryption': 'AES-256-CBC',
    'key_derivation': 'PBKDF2-SHA256',
    'digital_signature': 'HMAC-SHA256',
    'asymmetric_encryption': 'RSA-2048-OAEP',
}

# 环境特定配置
ENVIRONMENT = config('ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    # 生产环境严格配置
    TIME_WINDOW = 15  # 15秒
    SESSION_KEY_TTL = 300  # 5分钟
    ANTI_REPLAY = True
    INTEGRITY_CHECK = True
    ENCRYPTION_LOGGING['enable_debug_logs'] = False
    ENCRYPTION_LOGGING['log_level'] = 'WARNING'

elif ENVIRONMENT == 'testing':
    # 测试环境配置
    TIME_WINDOW = 60  # 1分钟
    SESSION_KEY_TTL = 600  # 10分钟
    ENCRYPTION_LOGGING['log_level'] = 'ERROR'

# 兼容性配置
BACKWARD_COMPATIBILITY = {
    'support_legacy_encryption': config('SUPPORT_LEGACY_ENCRYPTION', default=True, cast=bool),
    'legacy_key': config('LEGACY_CRYPTO_KEY', default=None),
    'migration_deadline': config('ENCRYPTION_MIGRATION_DEADLINE', default=None),
}

# 导出所有配置
__all__ = [
    'CRYPTO_KEY',
    'CRYPTO_IV',
    'TRANSPORT_KEY',
    'SESSION_KEY_TTL',
    'TIME_WINDOW',
    'ANTI_REPLAY',
    'INTEGRITY_CHECK',
    'COMPRESSION_THRESHOLD',
    'RSA_KEY_SIZE',
    'ENCRYPTION_MIDDLEWARE_ENABLED',
    'ENCRYPTION_EXCLUDED_PATHS',
    'HIGH_SECURITY_PATHS',
    'ENCRYPTION_LOGGING',
    'ENCRYPTION_PERFORMANCE',
    'ENCRYPTION_CACHE_CONFIG',
    'KEY_ROTATION',
    'MONITORING',
    'ENCRYPTION_ALGORITHMS',
    'BACKWARD_COMPATIBILITY',
]
