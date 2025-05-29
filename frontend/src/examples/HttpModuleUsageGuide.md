# HTTP模块使用指南

本文档详细说明了前端HTTP模块的使用方法和加密通信策略。

## 系统架构概览

这个HTTP模块采用了**多层加密策略**，支持0-3级的AES-256加密，并不是所有通信都经过加密，而是根据数据敏感度智能选择加密级别。

## 加密级别策略

### 1. 加密级别分类

```javascript
// 来自 cryptoConfig.js
export const ENCRYPT_LEVELS = {
  NONE: 0,     // 不加密 - 公开信息
  LOW: 1,      // 单层加密 - 普通数据
  MEDIUM: 2,   // 双层加密 - 中等敏感数据
  HIGH: 3      // 三层加密 - 高敏感数据（密码等）
}
```

### 2. 自动加密级别判断

系统会根据以下规则自动判断加密级别：

- **0级（不加密）**：登录、注册、公开资源
- **1级（低级）**：普通API请求
- **3级（高级）**：密码相关、支付信息、敏感数据

## 使用方法

### 1. 基础使用 - 推荐方式

```javascript
// 导入API模块
import api from '@/modules/http/api'

// 使用认证API（密码字段自动3级加密）
const loginResult = await api.auth.login({
  email: 'user@example.com',
  password: '123456'  // 自动检测并使用3级加密
})

// 使用AI API（普通数据1级加密）
const chatResult = await api.ai.chat({
  message: '你好',
  model: 'gpt-3.5'
})

// 使用元宇宙API
const spaces = await api.metaverse.getSpaces({
  page: 1,
  category: 'public'
})
```

### 2. 按需导入特定模块

```javascript
// 只导入需要的API模块
import { authAPI, aiAPI, metaverseAPI } from '@/modules/http'

// 使用特定API
const user = await authAPI.me()
const pets = await aiAPI.getUserPets()
const inventory = await metaverseAPI.getUserInventory()
```

### 3. 使用通用请求方法

```javascript
import { request } from '@/modules/http'

// GET请求
const users = await request.get('/users', { page: 1 })

// POST请求（数据自动加密）
const result = await request.post('/auth/change-password', {
  current_password: 'old123',  // 自动3级加密
  new_password: 'new456'       // 自动3级加密
})

// 文件上传
const uploadResult = await request.upload('/upload', formData, (progress) => {
  console.log(`上传进度: ${progress}%`)
})
```

### 4. 手动控制加密

```javascript
import { request } from '@/modules/http'

// 手动设置全局加密级别
request.setEncryptLevel(3)  // 强制使用3级加密

// 临时禁用加密
request.setEncryption(false)

// 重新启用加密
request.setEncryption(true)

// 手动加密/解密数据
const encrypted = request.encrypt({ sensitive: 'data' }, 3)
const decrypted = request.decrypt(encrypted, 3)
```

## 是否全部通信都加密？

**答案：不是**。系统采用智能加密策略：

### 不加密的情况
```javascript
// 排除路径（来自 cryptoConfig.js）
EXCLUDE_PATHS: [
  '/auth/login',      // 登录
  '/auth/register',   // 注册
  '/auth/refresh',    // 刷新token
  '/auth/logout',     // 登出
  '/public/'          // 公开资源
]
```

### 自动高级加密的情况

#### 1. 敏感字段自动检测
```javascript
// 这些字段会自动使用3级加密
const sensitiveFields = [
  'password', 'pwd', 'pass',
  'secret',
  'current_password', 'new_password',
  'password_confirmation'
]
```

#### 2. 高安全级别API路径
```javascript
HIGH_SECURITY_PATHS: [
  '/auth/change-password',    // 修改密码
  '/auth/reset-password',     // 重置密码
  '/auth/2fa',               // 两步验证
  '/payment',                // 支付相关
  '/billing',                // 账单相关
  '/admin/users'             // 管理员用户管理
]
```

## 实际加密流程

### 请求加密过程

1. **自动检测**：根据URL路径和数据内容判断加密级别
2. **数据加密**：使用AES-256对请求数据进行多层加密
3. **签名生成**：生成请求签名防止篡改
4. **请求发送**：添加加密头信息发送请求

```javascript
// secureAxios.js 中的关键代码
if (this.encryptConfig.enabled && !this.isExcludedPath(config.url)) {
  // 加密请求数据
  if (config.data && typeof config.data === 'object') {
    config.data = {
      encrypted_data: crypto.encrypt(config.data, encryptLevel)
    };
  }
}
```

### 响应解密过程

1. **检测加密**：检查响应是否包含加密数据
2. **自动解密**：根据加密级别自动解密
3. **返回数据**：返回解密后的原始数据

## 实用示例

### 示例1：用户登录（混合加密）
```javascript
// 登录请求不加密，但密码字段会被特殊处理
const result = await api.auth.login({
  email: 'user@example.com',     // 明文
  password: '123456',            // 3级加密
  remember: true                 // 明文
})
```

### 示例2：修改密码（高级加密）
```javascript
// 整个请求都使用3级加密
const result = await api.auth.changePassword({
  current_password: 'old123',
  new_password: 'new456',
  password_confirmation: 'new456'
})
```

### 示例3：普通聊天（标准加密）
```javascript
// 使用1级加密
const result = await api.ai.chat({
  message: '今天天气怎么样？',
  model: 'gpt-3.5'
})
```

## 模块结构说明

### 核心模块 (`frontend/src/modules/core/`)
- `config.js`: 应用配置、API配置、路由配置、存储配置和加密配置
- `constants.js`: 定义各种全局常量
- `utils.js`: 通用工具函数（深度克隆、防抖、节流、日期格式化等）
- `index.js`: 统一导出核心模块

### HTTP模块 (`frontend/src/modules/http/`)
- `api.js`: API统一入口，包含APIManager类
- `axios.js`: 基础axios实例
- `secureAxios.js`: 安全加密的axios实例，支持数据加密传输
- `request.js`: 统一请求方法
- `index.js`: 导出HTTP相关功能
- `modules/`: 包含各个API模块（auth, ai, user, metaverse）
- `utils/`: 包含加密工具（crypto.js, cryptoConfig.js）

### API模块说明

#### 认证模块 (`modules/auth.js`)
```javascript
// 使用secureAxios，支持敏感数据加密
import secureAxios from '../secureAxios';

// 所有认证相关API，如登录、注册、密码管理等
export const authAPI = {
  login: (credentials) => secureAxios.post('/auth/login', credentials),
  register: (userData) => secureAxios.post('/auth/register', userData),
  // ...更多API方法
}
```

#### AI模块 (`modules/ai.js`)
```javascript
// 使用普通axios实例
import axios from '../axios';

// AI相关API，如聊天、语音、图像生成等
export const aiAPI = {
  chat: (data) => axios.post('/ai/chat', data),
  textToSpeech: (data) => axios.post('/ai/tts', data),
  // ...更多AI功能
}
```

## 配置建议

在 `config.js` 中可以调整加密配置：

```javascript
// 加密配置
export const CRYPTO_CONFIG = {
  defaultLevel: 2,    // 默认加密级别
  enabled: true       // 启用加密
}
```

## 安全特性

1. **多层嵌套加密**：支持1-3层AES-256加密
2. **智能加密级别**：根据数据敏感度自动选择加密级别
3. **请求签名验证**：防止请求被篡改
4. **时间戳验证**：防止重放攻击
5. **自动token管理**：自动添加和刷新认证token

## 性能考虑

- 加密级别越高，性能开销越大
- 公开数据不加密，确保系统响应速度
- 敏感数据使用最高级别加密，确保安全性
- 支持批量请求，减少网络开销

这个系统提供了**安全性**和**性能**的良好平衡，确保敏感数据得到最高级别保护，同时避免对所有数据进行不必要的加密处理。
