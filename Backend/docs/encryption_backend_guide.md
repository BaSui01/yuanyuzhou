# Django后端加密解密服务指南

## 概述

本文档详细介绍了Django后端的双层加密解密服务实现，包括传输层加密和应用层加密的完整解决方案。

## 架构设计

### 双层加密架构

1. **应用层加密**
   - 使用多级嵌套AES加密
   - 支持1-3级加密强度
   - 基于PBKDF2密钥派生
   - 使用Fernet对称加密

2. **传输层加密**
   - RSA + AES混合加密
   - AES-256-GCM认证加密
   - 完整性校验(HMAC-SHA256)
   - 防重放攻击保护

## 核心组件

### 1. 加密中间件 (`apps/core/middleware/encryption.py`)

```python
class EncryptionMiddleware(MiddlewareMixin):
    """
    自动处理请求和响应的加密/解密
    支持传输层和应用层双重加密
    """
```

**主要功能：**
- 自动解密入站请求
- 自动加密出站响应
- 会话管理和验证
- 错误处理和日志记录

**处理流程：**
```
请求 -> 传输层解密 -> 应用层解密 -> 业务逻辑 -> 应用层加密 -> 传输层加密 -> 响应
```

### 2. 传输层加密服务 (`TransportEncryptionService`)

**特性：**
- RSA-2048密钥对生成
- AES-256-GCM对称加密
- PBKDF2密钥派生(100,000轮)
- 会话密钥管理(5分钟TTL)
- 防重放攻击(时间窗口+nonce)
- 数据完整性校验(HMAC)
- 自动数据压缩(>1KB)

**API方法：**
```python
# 生成会话密钥
session_info = service.generate_session_key(client_id)

# 加密传输数据
transport_packet = service.encrypt_transport(payload, session_id)

# 解密传输数据
decrypted_result = service.decrypt_transport(transport_packet)
```

### 3. 应用层加密工具 (`ApplicationCryptoUtils`)

**特性：**
- 多级嵌套加密(1-3级)
- Fernet对称加密
- 随机盐生成
- PBKDF2密钥派生(1,000轮)
- JSON数据序列化

**加密级别：**
- Level 0: 无加密
- Level 1: 单层加密
- Level 2: 双层加密
- Level 3: 三层加密

### 4. 高级加密工具 (`AdvancedCryptoUtils`)

**特性：**
- RSA非对称加密
- AES-GCM认证加密
- HMAC数字签名
- 密钥派生函数
- 数据压缩支持

## API端点

### 会话管理

```http
# 创建加密会话
POST /api/v1/core/encryption/api/session/create/
{
    "client_id": "client_123456",
    "client_public_key": "-----BEGIN PUBLIC KEY-----..."
}

# 获取会话状态
GET /api/v1/core/encryption/api/session/{session_id}/status/

# 撤销会话
DELETE /api/v1/core/encryption/api/session/{session_id}/revoke/
```

### 测试和监控

```http
# 加密功能测试
POST /api/v1/core/encryption/api/test/
{
    "data": {"message": "test data"},
    "level": 2
}

# 健康检查
GET /api/v1/core/encryption/api/health/

# 统计信息
GET /api/v1/core/encryption/stats/
```

## 配置说明

### 环境变量配置

```env
# 基础加密密钥
CRYPTO_KEY=yuanyuzhou-metaverse-platform-secure-key
CRYPTO_IV=metaverse-iv-16ch
TRANSPORT_KEY=transport-layer-secure-key-2024

# 会话配置
SESSION_KEY_TTL=300
TIME_WINDOW=30
ANTI_REPLAY=True
INTEGRITY_CHECK=True

# 性能配置
COMPRESSION_THRESHOLD=1024
RSA_KEY_SIZE=2048
ENCRYPTION_MAX_REQUEST_SIZE=10485760

# 环境特定配置
ENVIRONMENT=development  # development|testing|production
```

### 中间件配置

在 `settings.py` 中启用加密中间件：

```python
MIDDLEWARE = [
    # ... 其他中间件
    'apps.core.middleware.encryption.EncryptionMiddleware',
    # ... 其他中间件
]

# 导入加密配置
from .settings.encryption import *
```

## 使用示例

### 1. 前端会话建立

```javascript
// 创建加密会话
const sessionResponse = await axios.post('/api/v1/core/encryption/api/session/create/', {
    client_id: 'my_client_id',
    client_public_key: clientPublicKey
});

const { session_id, server_public_key } = sessionResponse.data.data;
```

### 2. 加密请求发送

```javascript
// 发送加密请求
const response = await secureTransport.post('/api/v1/users/', userData, {
    encryptLevel: ENCRYPT_LEVELS.HIGH
});
```

### 3. 手动加密/解密

```python
from apps.core.middleware.encryption import ApplicationCryptoUtils

crypto = ApplicationCryptoUtils()

# 加密数据
encrypted = crypto.encrypt(data, level=2)

# 解密数据
decrypted = crypto.decrypt(encrypted, level=2)
```

## 安全特性

### 1. 多层防护

- **传输层加密**: RSA + AES-GCM混合加密
- **应用层加密**: 多级嵌套AES加密
- **完整性校验**: HMAC-SHA256签名验证
- **防重放攻击**: 时间戳 + nonce验证

### 2. 密钥管理

- **会话密钥**: 动态生成，定期过期
- **密钥派生**: PBKDF2高强度派生
- **密钥轮换**: 支持定期密钥更新
- **分离存储**: 传输层和应用层密钥分离

### 3. 访问控制

- **路径过滤**: 可配置的加密路径
- **级别控制**: 根据API敏感度调整加密级别
- **会话验证**: 严格的会话有效性检查

## 性能优化

### 1. 缓存机制

- **会话缓存**: Redis存储会话密钥
- **nonce缓存**: 防重放攻击nonce存储
- **定期清理**: 自动清理过期数据

### 2. 数据压缩

- **自动压缩**: 超过阈值自动压缩
- **gzip压缩**: 高效的数据压缩算法
- **大小优化**: 减少网络传输开销

### 3. 算法优化

- **硬件加速**: 支持AES-NI指令集
- **内存优化**: 流式处理大数据
- **并发处理**: 支持高并发加密操作

## 监控和日志

### 1. 日志记录

```python
# 加密操作日志
logger.info(f"[传输加密] 数据包已加密 - 会话: {session_id[:8]}...")
logger.info(f"[应用加密] 数据已加密 - 级别: {level}")
```

### 2. 性能监控

- **加密耗时**: 记录加密/解密处理时间
- **会话统计**: 活跃会话数量监控
- **错误率**: 加密失败率统计

### 3. 安全审计

- **异常检测**: 异常加密请求告警
- **攻击防护**: 重放攻击检测记录
- **访问审计**: 敏感数据访问日志

## 故障排除

### 常见问题

1. **会话过期错误**
   ```json
   {
       "error": "SESSION_EXPIRED",
       "message": "会话已过期或不存在"
   }
   ```
   **解决方案**: 重新创建会话或增加会话TTL

2. **解密失败错误**
   ```json
   {
       "error": "DECRYPTION_FAILED",
       "message": "请求解密失败"
   }
   ```
   **解决方案**: 检查加密级别和密钥配置

3. **时间窗口错误**
   ```json
   {
       "error": "TIME_WINDOW_EXCEEDED",
       "message": "传输包时间戳超出允许窗口"
   }
   ```
   **解决方案**: 同步客户端时间或调整TIME_WINDOW

### 调试工具

```python
# 启用调试日志
ENCRYPTION_LOGGING = {
    'enable_debug_logs': True,
    'log_level': 'DEBUG'
}

# 测试加密功能
response = requests.post('/api/v1/core/encryption/api/test/', {
    'data': {'test': 'data'},
    'level': 1
})
```

## 部署建议

### 1. 生产环境

```env
ENVIRONMENT=production
TIME_WINDOW=15
SESSION_KEY_TTL=300
ENCRYPTION_DEBUG_LOGS=False
```

### 2. 密钥管理

- 使用环境变量存储密钥
- 定期轮换加密密钥
- 安全备份密钥材料

### 3. 性能调优

- 配置Redis缓存集群
- 启用数据压缩
- 监控系统资源使用

## 扩展功能

### 1. 密钥轮换

```python
KEY_ROTATION = {
    'enabled': True,
    'interval_hours': 24,
    'backup_count': 3
}
```

### 2. 多环境支持

- 开发环境：宽松配置，详细日志
- 测试环境：中等安全，错误日志
- 生产环境：严格安全，警告日志

### 3. 监控集成

```python
MONITORING = {
    'enable_metrics': True,
    'alert_on_failures': True,
    'failure_threshold': 10
}
```

## 总结

Django后端加密解密服务提供了企业级的数据安全保护：

- **双层加密**: 传输层 + 应用层双重保护
- **高级算法**: RSA + AES + HMAC混合加密
- **自动化处理**: 中间件自动加密/解密
- **灵活配置**: 多环境、多级别配置支持
- **性能优化**: 缓存、压缩、并发优化
- **安全审计**: 完整的日志和监控机制

该解决方案确保了前后端数据传输的绝对安全，同时保持了良好的性能和开发体验。
