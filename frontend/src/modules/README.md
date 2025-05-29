# 模块系统架构

本项目采用模块化架构，将功能按照职责分离到不同的模块中，提高代码的可维护性和可扩展性。

## 📁 目录结构

```
src/modules/
├── core/           # 核心模块
│   ├── config.js   # 全局配置
│   ├── constants.js # 常量定义
│   ├── utils.js    # 工具函数
│   └── index.js    # 统一导出
├── http/           # HTTP 客户端模块
│   ├── api.js      # API 管理器
│   ├── axios.js    # Axios 实例
│   ├── request.js  # 请求方法
│   ├── modules/    # API 模块
│   │   ├── auth.js
│   │   ├── user.js
│   │   ├── ai.js
│   │   └── metaverse.js
│   ├── utils/      # HTTP 工具
│   │   ├── crypto.js
│   │   └── cryptoConfig.js
│   └── index.js    # 统一导出
├── navigation/     # 导航模块
│   ├── router.js   # Vue Router 配置
│   ├── routes.js   # 路由定义
│   ├── guards.js   # 路由守卫
│   ├── utils.js    # 导航工具
│   └── index.js    # 统一导出
├── features/       # 功能模块
│   ├── ai/         # AI 功能
│   │   ├── api/
│   │   ├── composables/
│   │   ├── components/
│   │   ├── stores/
│   │   └── index.js
│   ├── user/       # 用户功能
│   ├── metaverse/  # 元宇宙功能
│   └── index.js
├── testing/        # 测试模块
│   ├── mocks/      # Mock 数据
│   ├── fixtures/   # 测试数据
│   ├── utils.js    # 测试工具
│   └── index.js    # 统一导出
├── setup/          # 应用设置模块
│   ├── init.js     # 应用初始化
│   ├── config.js   # 配置设置
│   ├── plugins.js  # 插件设置
│   ├── services.js # 服务设置
│   └── index.js    # 统一导出
└── index.js        # 主入口文件
```

## 🎯 模块职责

### 1. Core 模块 (`core/`)
**职责**：提供全局配置、常量定义和通用工具函数
- `config.js`: 应用配置、API配置、路由配置等
- `constants.js`: 全局常量定义
- `utils.js`: 通用工具函数（格式化、验证、存储等）

### 2. HTTP 模块 (`http/`)
**职责**：处理所有 HTTP 请求和 API 通信
- `api.js`: API 管理器，提供统一的 API 接口
- `axios.js`: 基础 Axios 实例配置
- `request.js`: 封装的请求方法（GET、POST、上传、下载等）
- `modules/`: 按功能分组的 API 模块

### 3. Navigation 模块 (`navigation/`)
**职责**：管理应用的路由和导航
- `router.js`: Vue Router 实例配置
- `routes.js`: 路由定义，按功能分组
- `guards.js`: 路由守卫（认证、权限等）

### 4. Features 模块 (`features/`)
**职责**：业务功能模块，每个子目录代表一个业务域
- 采用领域驱动设计（DDD）思想
- 每个功能模块包含：API、组合式函数、组件、状态管理

### 5. Testing 模块 (`testing/`)
**职责**：测试支持和 Mock 数据
- `mocks/`: Mock Service Worker 配置
- `fixtures/`: 测试数据
- `utils.js`: 测试工具函数

### 6. Setup 模块 (`setup/`)
**职责**：应用初始化和配置
- `init.js`: 应用启动流程
- 插件配置和服务注册

## 🚀 使用方式

### 基础导入
```javascript
// 导入核心模块
import { config, constants, utils } from '@/modules/core'

// 导入 HTTP 客户端
import { api, request } from '@/modules/http'

// 导入路由
import { router } from '@/modules/navigation'

// 导入功能模块
import { ai, user, metaverse } from '@/modules/features'
```

### 模块注册器
```javascript
import { moduleRegistry, initModules } from '@/modules'

// 初始化所有模块
await initModules()

// 获取特定模块
const coreModule = moduleRegistry.get('core')
```

### API 使用
```javascript
import { api } from '@/modules/http'

// 使用 API 管理器
const response = await api.user.getProfile()

// 使用原始请求方法
const data = await api.request.get('/api/users')
```

### 路由使用
```javascript
import { router, routerUtils } from '@/modules/navigation'

// 编程式导航
routerUtils.navigate('/dashboard')

// 检查路由权限
if (guardUtils.canAccess(route, user)) {
  // 允许访问
}
```

## 🔧 扩展指南

### 添加新的功能模块
1. 在 `features/` 下创建新目录
2. 按照标准结构组织文件：
   ```
   features/newFeature/
   ├── api/
   ├── composables/
   ├── components/
   ├── stores/
   └── index.js
   ```
3. 在 `features/index.js` 中导出新模块

### 添加新的 API 模块
1. 在 `http/modules/` 下创建新文件
2. 导出 API 函数
3. 在 `http/modules/index.js` 中注册

### 添加路由
1. 在 `navigation/routes.js` 中添加路由定义
2. 按功能分组组织路由
3. 设置适当的 meta 信息

## 🛠️ 开发规范

### 1. 文件命名
- 使用小驼峰命名法：`userService.js`
- 目录使用小写：`features/ai/`

### 2. 导出规范
- 每个模块必须有 `index.js` 统一导出
- 使用命名导出，避免默认导出混乱

### 3. 依赖管理
- 模块间依赖应该明确
- 避免循环依赖
- 优先使用依赖注入

### 4. 文档要求
- 每个模块必须有清晰的 JSDoc 注释
- 复杂功能需要使用示例

## 🎯 最佳实践

1. **单一职责**：每个模块只负责一个特定的功能域
2. **松耦合**：模块间通过明确的接口通信
3. **可测试性**：每个模块都应该易于单元测试
4. **可扩展性**：新功能应该能够轻松添加新模块
5. **性能优化**：使用动态导入进行代码分割

## 💡 常见用法示例

### 初始化应用
```javascript
import { initModules } from '@/modules'

// 在 main.js 中初始化模块系统
async function bootstrap() {
  await initModules()
  // 继续应用初始化...
}
```

### 使用配置
```javascript
import { config } from '@/modules/core'

const apiUrl = config.API_CONFIG.baseURL
```

### 发起 API 请求
```javascript
import { api } from '@/modules/http'

// 登录
const loginResult = await api.auth.login({
  email: 'user@example.com',
  password: 'password'
})

// 获取用户信息
const userInfo = await api.user.getProfile()
```

### 路由导航
```javascript
import { router } from '@/modules/navigation'

// 编程式导航
router.push('/dashboard')

// 路由守卫中使用
router.beforeEach((to, from, next) => {
  // 路由守卫逻辑
})
```

## 🔍 调试和监控

### 模块状态检查
```javascript
import { moduleRegistry } from '@/modules'

// 检查模块是否已注册
console.log(moduleRegistry.has('core')) // true

// 获取所有模块
console.log(moduleRegistry.getAll())
```

### 错误处理
所有模块都包含完善的错误处理机制，错误会被统一捕获和记录。

这种模块化架构提供了清晰的代码组织、良好的可维护性和强大的扩展能力，支持大型 Vue.js 应用的开发需求。
