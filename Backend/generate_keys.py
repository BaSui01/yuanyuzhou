    #!/usr/bin/env python3
"""
安全密钥生成器
为元宇宙社交平台生成加密密钥
"""

import secrets
import string
import os
from datetime import datetime

def generate_key(length=64):
    """生成指定长度的安全随机密钥"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*()-_=+[]{}|;:,.<>?'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hex_key(length=32):
    """生成十六进制密钥"""
    return secrets.token_hex(length)

def generate_base64_key(length=32):
    """生成base64编码的密钥"""
    return secrets.token_urlsafe(length)

def generate_alphanumeric_key(length=16):
    """生成纯字母数字密钥（适用于IV）"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("🔐 元宇宙社交平台密钥生成器")
    print("=" * 50)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 生成各种密钥
    keys = {
        'CRYPTO_KEY': generate_key(64),
        'CRYPTO_IV': generate_alphanumeric_key(16),
        'TRANSPORT_KEY': generate_key(64),
        'LEGACY_CRYPTO_KEY': generate_key(64),
        'ENCRYPTION_CACHE_PREFIX': f"encrypt_{secrets.token_hex(4)}:",
        'SECRET_KEY': generate_key(50),  # Django SECRET_KEY
        'JWT_SECRET': generate_base64_key(32),
        'API_KEY': generate_hex_key(16),
        'WEBHOOK_SECRET': generate_key(32),
    }

    print("🎯 生成的密钥:")
    print("-" * 30)
    for key, value in keys.items():
        print(f"{key}={value}")

    print()
    print("🔧 完整的.env配置:")
    print("-" * 30)

    env_content = f"""# Django后端加密解密服务环境变量配置
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 警告: 请妥善保管这些密钥，不要泄露给他人

# ============================================
# 基础加密密钥配置
# ============================================
# 应用层加密主密钥 - 64字符强随机密钥
CRYPTO_KEY={keys['CRYPTO_KEY']}

# 应用层加密初始向量 - 16字符长度
CRYPTO_IV={keys['CRYPTO_IV']}

# 传输层加密主密钥 - 64字符强随机密钥
TRANSPORT_KEY={keys['TRANSPORT_KEY']}

# ============================================
# Django框架配置
# ============================================
# Django SECRET_KEY
SECRET_KEY={keys['SECRET_KEY']}

# JWT密钥
JWT_SECRET={keys['JWT_SECRET']}

# API密钥
API_KEY={keys['API_KEY']}

# ============================================
# 会话和安全配置
# ============================================
# 会话密钥生存时间（秒） - 生产环境建议300-600
SESSION_KEY_TTL=300

# 时间窗口容忍度（秒） - 生产环境建议15-30
TIME_WINDOW=30

# 启用防重放攻击保护
ANTI_REPLAY=True

# 启用数据完整性校验
INTEGRITY_CHECK=True

# 数据压缩阈值（字节）
COMPRESSION_THRESHOLD=1024

# RSA密钥长度（位）
RSA_KEY_SIZE=2048

# ============================================
# 中间件和路径配置
# ============================================
# 启用加密中间件
ENCRYPTION_MIDDLEWARE_ENABLED=True

# ============================================
# 性能和限制配置
# ============================================
# 最大请求大小（字节）- 10MB
ENCRYPTION_MAX_REQUEST_SIZE=10485760

# 加密操作超时时间（秒）
ENCRYPTION_TIMEOUT=30

# 最大并发会话数
ENCRYPTION_MAX_SESSIONS=1000

# ============================================
# Redis缓存配置
# ============================================
# 会话缓存数据库索引
ENCRYPTION_SESSION_CACHE_DB=1

# Nonce缓存数据库索引
ENCRYPTION_NONCE_CACHE_DB=2

# 缓存键前缀
ENCRYPTION_CACHE_PREFIX={keys['ENCRYPTION_CACHE_PREFIX']}

# ============================================
# 日志和调试配置
# ============================================
# 启用调试日志（生产环境请设为False）
ENCRYPTION_DEBUG_LOGS=False

# 日志级别 (DEBUG|INFO|WARNING|ERROR)
ENCRYPTION_LOG_LEVEL=INFO

# 加密日志文件路径（可选）
ENCRYPTION_LOG_FILE=

# ============================================
# 密钥轮换配置
# ============================================
# 启用自动密钥轮换
KEY_ROTATION_ENABLED=False

# 密钥轮换间隔（小时）
KEY_ROTATION_INTERVAL=24

# 备份密钥数量
KEY_BACKUP_COUNT=3

# ============================================
# 监控和告警配置
# ============================================
# 启用性能指标收集
ENCRYPTION_METRICS_ENABLED=True

# 启用失败告警
ENCRYPTION_ALERT_FAILURES=True

# 失败告警阈值
ENCRYPTION_FAILURE_THRESHOLD=10

# 告警webhook地址（可选）
ENCRYPTION_ALERT_WEBHOOK=

# Webhook签名密钥
WEBHOOK_SECRET={keys['WEBHOOK_SECRET']}

# ============================================
# 兼容性配置
# ============================================
# 支持旧版加密（向后兼容）
SUPPORT_LEGACY_ENCRYPTION=True

# 旧版加密密钥（用于数据迁移）
LEGACY_CRYPTO_KEY={keys['LEGACY_CRYPTO_KEY']}

# 加密迁移截止日期（可选）
ENCRYPTION_MIGRATION_DEADLINE=

# ============================================
# 环境特定配置
# ============================================
# 运行环境 (development|testing|production)
ENVIRONMENT=development

# 调试模式
DEBUG=True

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/yuanyuzhou_db

# Redis配置
REDIS_URL=redis://localhost:6379/0

# ============================================
# 第三方服务配置
# ============================================
# AI服务密钥
OPENAI_API_KEY=
BAIDU_API_KEY=
ALIBABA_API_KEY=

# 对象存储配置
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET_NAME=

# 邮件服务配置
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# ============================================
# 安全提醒
# ============================================
# 1. 立即将此文件重命名为 .env
# 2. 确保 .env 文件已添加到 .gitignore
# 3. 定期轮换密钥（建议每3-6个月）
# 4. 在生产环境中使用密钥管理服务
# 5. 监控异常的加密操作
# 6. 备份重要的密钥
"""

    print(env_content)

    # 保存到文件
    output_file = ".env.generated"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(env_content)

    print(f"✅ 配置文件已保存到: {output_file}")
    print()
    print("🚨 重要提醒:")
    print("1. 请将 .env.generated 重命名为 .env")
    print("2. 确保 .env 文件不会被提交到版本控制")
    print("3. 妥善保管这些密钥")
    print("4. 在生产环境中定期轮换密钥")

if __name__ == "__main__":
    main()
