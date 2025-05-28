# API 加密通信模块

本模块实现了前后端通信加密功能，提供多层嵌套加密、请求签名验证、数据完整性保护等安全特性。

## 功能特点

- 多层嵌套加密：支持1-3层AES-256加密
- 智能加密级别：根据数据敏感度自动选择加密级别
- 请求签名验证：防止请求被篡改
- 灵活的加密配置：可以针对不同API设置不同加密级别
- 自动加解密：无需手动处理加密解密过程
- 兼容原有API：可以平滑过渡到加密通信

## 加密级别策略

系统根据数据敏感度自动应用不同的加密级别：

- **3级加密**（高级）：用于密码、支付信息等高敏感数据
  - 自动检测请求中的密码字段
  - 指定的高安全API路径
  - 包含敏感信息的请求

- **1级加密**（低级）：用于普通数据传输
  - 一般性API请求
  - 非敏感信息

- **0级加密**（无加密）：用于公开信息
  - 登录、注册等身份验证API
  - 公开资源访问

## 使用方法

### 基础使用

```javascript
import api from '@/api';

// 使用加密API发送请求
api.auth.login({
  email: 'user@example.com',
  password: '123456'  // 密码字段会自动使用3级加密
}).then(response => {
  console.log('登录成功', response);
}).catch(error => {
  console.error('登录失败', error);
});
```

### 按需导入

```javascript
import { authAPI } from '@/api';

// 使用特定API模块
authAPI.login({
  email: 'user@example.com',
  password: '123456'  // 密码字段会自动使用3级加密
}).then(response => {
  console.log('登录成功', response);
});
```

### 使用通用请求方法

```javascript
import { request } from '@/api';

// 使用通用请求方法
request.post('/auth/login', {
  email: 'user@example.com',
  password: '123456'  // 密码字段会自动使用3级加密
}).then(response => {
  console.log('登录成功', response);
});
```

### 手动加密/解密数据

```javascript
import { request, crypto } from '@/api';

// 手动加密数据
const encryptedData = request.encrypt({
  username: 'test',
  password: '123456'
}, 3); // 强制使用3级加密

console.log('加密后数据:', encryptedData);

// 手动解密数据
const decryptedData = request.decrypt(encryptedData, 3);
console.log('解密后数据:', decryptedData);
```

### 调整加密级别

```javascript
import { request } from '@/api';

// 设置全局加密级别
request.setEncryptLevel(3); // 使用3级加密（最高级别）

// 禁用加密
request.setEncryption(false);

// 重新启用加密
request.setEncryption(true);
```

## 加密级别说明

- **0级**：不加密，明文传输
- **1级**：单层AES-256加密（默认普通数据）
- **2级**：双层AES-256加密（中等敏感数据）
- **3级**：三层AES-256加密（高敏感数据，如密码）

## 自动高级加密的字段

系统会自动检测以下字段并使用3级加密：

- password, pwd, pass
- secret
- current_password, new_password
- password_confirmation, passwordConfirmation
- currentPassword, newPassword

## 高安全级别API路径

以下API路径会自动使用3级加密：

- /auth/change-password
- /auth/reset-password
- /auth/password
- /auth/2fa
- /users/password
- /payment, /billing, /subscription
- /user/identity, /user/verification
- /admin/users

## 注意事项

1. 登录、注册等身份验证API默认不加密，以确保系统可用性
2. 文件上传/下载API使用特殊处理，不对文件内容本身加密
3. 加密级别越高，性能开销越大，请根据实际需求设置
4. 生产环境中应通过环境变量配置加密密钥，不要硬编码

## 后端集成

后端需要实现对应的解密逻辑，处理加密请求和返回加密响应。具体实现可参考后端文档。

## 安全建议

1. 定期更换加密密钥
2. 敏感数据传输使用3级加密
3. 结合HTTPS传输，提供双重保护
4. 实现请求防重放机制（时间戳验证）
