# 传输层加密使用指南

## 概述

传输层加密模块提供了端到端的数据传输安全保障，包括会话管理、数据加密、完整性校验和防重放攻击等功能。本指南将详细介绍如何使用传输层加密功能。

## 核心特性

### 1. 双层加密架构
- **应用层加密**：使用 CryptoUtil 对业务数据进行加密
- **传输层加密**：使用 TransportEncryption 对整个请求包进行加密

### 2. 安全特性
- **会话密钥管理**：动态生成和管理会话密钥
- **防重放攻击**：使用 nonce 和时间戳防止重放攻击
- **完整性校验**：使用 HMAC 确保数据完整性
- **密钥交换**：安全的密钥协商协议

### 3. 性能优化
- **数据压缩**：大于阈值的数据自动压缩
- **会话缓存**：缓存会话密钥减少计算开销
- **自动清理**：定期清理过期会话和 nonce

## 基础使用

### 1. 导入模块

```javascript
import { SecureTransport } from '@/modules/http/secureTransport'
import { TransportEncryption } from '@/modules/http/transportEncryption'
import { ENCRYPT_LEVELS } from '@/modules/http/utils/cryptoConfig'
```

### 2. 创建安全传输实例

```javascript
// 使用默认配置
const secureTransport = new SecureTransport()

// 使用自定义配置
const secureTransport = new SecureTransport({
  baseURL: 'https://api.example.com',
  enableTransportEncryption: true,
  enableApplicationEncryption: true,
  defaultEncryptLevel: ENCRYPT_LEVELS.MEDIUM,
  clientId: 'my-client-app',
  timeout: 30000
})
```

### 3. 基本请求

```javascript
// GET 请求
const userData = await secureTransport.get('/users/profile')

// POST 请求（自动加密）
const result = await secureTransport.post('/users/update', {
  name: '用户名',
  email: 'user@example.com'
})

// 指定加密级别的请求
const sensitiveData = await secureTransport.post('/payment/create', paymentData, {
  encryptLevel: ENCRYPT_LEVELS.HIGH
})
```

## 高级配置

### 1. 传输层加密配置

```javascript
const transportOptions = {
  // 传输层密钥
  transportKey: 'your-transport-key',
  // 会话密钥生存时间（毫秒）
  sessionKeyTTL: 300000, // 5分钟
  // 时间窗口容忍度（秒）
  timeWindow: 30,
  // 启用防重放攻击
  antiReplay: true,
  // 启用完整性校验
  integrityCheck: true,
  // 压缩阈值（字节）
  compressionThreshold: 1024
}

const secureTransport = new SecureTransport({
  enableTransportEncryption: true,
  transportOptions
})
```

### 2. 应用层加密配置

```javascript
// 设置全局加密级别
secureTransport.setEncryptLevel(ENCRYPT_LEVELS.HIGH)

// 启用/禁用应用层加密
secureTransport.setApplicationEncryption(true)

// 启用/禁用传输层加密
secureTransport.setTransportEncryption(true)
```

## 会话管理

### 1. 会话信息查看

```javascript
// 获取当前会话信息
const sessionInfo = secureTransport.getSessionInfo()
console.log('会话ID:', sessionInfo?.sessionId)
console.log('过期时间:', new Date(sessionInfo?.expiresAt))

// 获取统计信息
const stats = secureTransport.getStatistics()
console.log('活跃会话数:', stats.activeSessions)
console.log('使用的nonce数:', stats.usedNonces)
```

### 2. 会话重置

```javascript
// 重置当前会话
await secureTransport.resetSession()

// 手动撤销会话
const { sessionId } = secureTransport.getSessionInfo()
transportEncryption.revokeSession(sessionId)
```

## 错误处理

### 1. 会话过期处理

```javascript
try {
  const response = await secureTransport.post('/api/data', requestData)
} catch (error) {
  if (error.response?.status === 401 &&
      error.response?.data?.code === 'SESSION_EXPIRED') {
    console.log('会话已过期，正在自动重新建立...')
    // SecureTransport 会自动处理会话重建和重试
  }
}
```

### 2. 加密失败处理

```javascript
try {
  const response = await secureTransport.post('/api/secure-data', data)
} catch (error) {
  if (error.message.includes('加密失败')) {
    console.error('数据加密失败:', error)
    // 处理加密错误
  } else if (error.message.includes('解密失败')) {
    console.error('数据解密失败:', error)
    // 处理解密错误
  }
}
```

## 文件上传

### 1. 安全文件上传

```javascript
// 单文件上传
const fileInput = document.getElementById('file-input')
const file = fileInput.files[0]

const response = await secureTransport.upload('/files/upload', file, {
  onProgress: (progressEvent) => {
    const percentCompleted = Math.round(
      (progressEvent.loaded * 100) / progressEvent.total
    )
    console.log(`上传进度: ${percentCompleted}%`)
  }
})

// 多文件上传
const formData = new FormData()
formData.append('file1', file1)
formData.append('file2', file2)
formData.append('description', '文件描述')

const response = await secureTransport.upload('/files/batch-upload', formData)
```

## 批量请求

```javascript
// 使用 API 管理器进行批量请求
import api from '@/modules/http/api'

const requests = [
  { method: 'GET', url: '/users/1' },
  { method: 'POST', url: '/users', data: { name: '新用户' } },
  { method: 'PUT', url: '/users/2', data: { name: '更新用户' } }
]

const results = await api.batch(requests)
results.forEach((result, index) => {
  if (result.status === 'fulfilled') {
    console.log(`请求 ${index} 成功:`, result.value.data)
  } else {
    console.error(`请求 ${index} 失败:`, result.reason)
  }
})
```

## 性能优化建议

### 1. 会话重用

```javascript
// 避免频繁创建新的传输实例
// 推荐：使用全局单例
import secureTransport from '@/modules/http/secureTransport'

// 不推荐：每次请求都创建新实例
// const newTransport = new SecureTransport()
```

### 2. 加密级别选择

```javascript
// 根据数据敏感度选择合适的加密级别

// 公开数据 - 不加密
const publicData = await secureTransport.get('/public/news', {}, {
  encryptLevel: ENCRYPT_LEVELS.NONE
})

// 一般数据 - 低级加密
const userData = await secureTransport.get('/users/profile', {}, {
  encryptLevel: ENCRYPT_LEVELS.LOW
})

// 敏感数据 - 高级加密
const paymentData = await secureTransport.post('/payment/process', data, {
  encryptLevel: ENCRYPT_LEVELS.HIGH
})
```

### 3. 数据压缩

```javascript
// 自动压缩配置
const secureTransport = new SecureTransport({
  transportOptions: {
    // 超过 1KB 的数据自动压缩
    compressionThreshold: 1024
  }
})
```

## 调试和监控

### 1. 启用调试日志

```javascript
// 开发环境下查看详细日志
if (import.meta.env.DEV) {
  // 传输层加密的日志会自动输出到控制台
  console.log('传输加密调试模式已启用')
}
```

### 2. 监控会话状态

```javascript
// 定期检查会话状态
setInterval(() => {
  const stats = secureTransport.getStatistics()
  if (stats.sessionInfo && !stats.sessionInfo.isValid) {
    console.warn('会话即将过期或已过期')
  }
}, 60000) // 每分钟检查一次
```

## 安全注意事项

### 1. 密钥管理

```javascript
// 生产环境中使用环境变量
// .env 文件
VITE_CRYPTO_KEY=your-super-secure-application-key
VITE_TRANSPORT_KEY=your-super-secure-transport-key
VITE_CRYPTO_IV=your-16-char-iv-string
```

### 2. HTTPS 配置

```javascript
// 确保在 HTTPS 环境下使用
if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
  console.warn('传输层加密建议在 HTTPS 环境下使用')
}
```

### 3. 时间同步

```javascript
// 确保客户端时间同步
const serverTime = response.headers['x-server-time']
const clientTime = Date.now()
const timeDiff = Math.abs(clientTime - parseInt(serverTime))

if (timeDiff > 30000) { // 30秒
  console.warn('客户端时间与服务器时间差异过大，可能影响加密功能')
}
```

## 与现有项目集成

### 1. 替换现有 HTTP 客户端

```javascript
// 旧代码
import axios from 'axios'
const response = await axios.post('/api/data', requestData)

// 新代码
import secureTransport from '@/modules/http/secureTransport'
const response = await secureTransport.post('/api/data', requestData)
```

### 2. Vue 组件中使用

```vue
<template>
  <div>
    <button @click="fetchData">获取安全数据</button>
    <button @click="submitForm">提交表单</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import secureTransport from '@/modules/http/secureTransport'

const data = ref(null)
const loading = ref(false)

const fetchData = async () => {
  loading.value = true
  try {
    const response = await secureTransport.get('/api/secure-data')
    data.value = response.data
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

const submitForm = async () => {
  const formData = {
    name: 'Test User',
    email: 'test@example.com'
  }

  try {
    const response = await secureTransport.post('/api/users', formData, {
      encryptLevel: ENCRYPT_LEVELS.MEDIUM
    })
    console.log('表单提交成功:', response.data)
  } catch (error) {
    console.error('表单提交失败:', error)
  }
}
</script>
```

## 故障排除

### 1. 常见错误

| 错误信息 | 可能原因 | 解决方案 |
|---------|---------|---------|
| "无效的会话ID或会话已过期" | 会话过期或无效 | 调用 `resetSession()` 重新建立会话 |
| "传输包时间戳超出允许窗口" | 客户端时间不同步 | 同步客户端时间 |
| "检测到重放攻击" | 重复的 nonce | 检查网络连接，避免重复请求 |
| "数据完整性校验失败" | 数据在传输中被篡改 | 检查网络环境和密钥配置 |

### 2. 调试步骤

1. 检查控制台日志中的加密/解密信息
2. 验证会话状态和过期时间
3. 确认加密配置和密钥设置
4. 检查网络请求的响应头信息
5. 验证服务器端对应的解密实现

## 总结

传输层加密模块提供了完整的端到端加密解决方案，通过双层加密架构和多重安全机制，确保数据传输的安全性。合理使用本模块可以显著提升应用的安全等级，同时保持良好的性能表现。

在实际使用中，建议根据数据的敏感程度选择合适的加密级别，并在生产环境中妥善管理密钥和配置信息。
