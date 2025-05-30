# 开发环境配置指南

## 概述

本项目已经优化了 VS Code 的启动配置，支持快速启动前端和后端开发环境。

## 项目结构

```
yuanyuzhou/
├── Backend/          # Django 后端
├── frontend/         # Vue.js 前端
├── scripts/          # 开发脚本
├── .vscode/          # VS Code 配置
│   ├── launch.json   # 调试配置
│   ├── tasks.json    # 任务配置
│   └── settings.json # 编辑器设置
└── docs/             # 文档
```

## 快速启动

### 方法一：使用 VS Code 调试面板

1. 打开 VS Code
2. 按 `F5` 或点击调试面板
3. 选择以下配置之一：
   - `🔥 前后端同时启动` - 同时启动 Django 和 Vue.js
   - `🚀 Django 开发服务器` - 仅启动后端
   - `🌐 前端开发服务器 (Vite)` - 仅启动前端

### 方法二：使用 VS Code 任务

1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 `Tasks: Run Task`
3. 选择所需任务：
   - `🚀 启动完整开发环境` - 同时启动前后端
   - `🔄 启动 Django + Celery` - 启动后端和后台任务
   - `📊 初始化项目数据库` - 初始化数据库

### 方法三：使用启动脚本

```bash
# 启动前后端
node scripts/start-dev.js

# 启动前后端 + Celery
node scripts/start-dev.js --celery
```

## 可用的调试配置

### Django 后端配置

| 配置名称 | 描述 | 端口 |
|---------|------|------|
| 🚀 Django 开发服务器 | 标准开发服务器 | 8000 |
| 🐛 Django 调试模式 | 详细日志调试模式 | 8001 |
| 📊 Django 数据库迁移 | 执行数据库迁移 | - |
| 📝 Django 创建迁移文件 | 创建新的迁移文件 | - |
| 👤 Django 创建超级用户 | 创建管理员用户 | - |
| 🧪 Django 运行测试 | 运行后端测试 | - |
| 🔄 Celery Worker | 后台任务处理器 | - |
| ⏰ Celery Beat | 定时任务调度器 | - |
| 📚 Django Shell | Django 交互式 Shell | - |

### Vue.js 前端配置

| 配置名称 | 描述 | 端口 |
|---------|------|------|
| 🌐 前端开发服务器 (Vite) | 开发服务器 | 通常 5173 |
| 🔨 前端构建项目 | 生产构建 | - |
| 👀 前端预览构建 | 预览构建结果 | 通常 4173 |
| 🔧 前端代码检查 | ESLint 检查 | - |
| ✨ 前端代码格式化 | Prettier 格式化 | - |

### 组合配置

| 配置名称 | 描述 |
|---------|------|
| 🔥 前后端同时启动 | 同时启动 Django + Vue.js |
| 🔄 Django + Celery 完整后端 | Django + Celery Worker + Beat |

## 常用开发命令

### Django 后端命令

```bash
cd Backend

# 启动开发服务器
python manage.py runserver

# 数据库操作
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行测试
python manage.py test

# 交互式 Shell
python manage.py shell

# 收集静态文件
python manage.py collectstatic

# Celery 相关
python manage.py celery worker --loglevel=info
python manage.py celery beat --loglevel=info
```

### Vue.js 前端命令

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview

# 代码检查
npm run lint

# 代码格式化
npm run format
```

## 访问地址

### 开发环境

- **前端应用**: http://localhost:5173 (Vite 默认端口)
- **后端 API**: http://127.0.0.1:8000
- **Django Admin**: http://127.0.0.1:8000/admin
- **API 文档**: http://127.0.0.1:8000/api/docs/
- **调试模式后端**: http://127.0.0.1:8001 (如果启用)

### 生产环境

- **前端应用**: http://localhost:4173 (预览模式)
- **后端 API**: 根据部署配置

## 环境变量配置

### 后端环境变量 (.env)

在 `Backend/` 目录下创建 `.env` 文件：

```env
# 基本配置
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置
DB_NAME=backend_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

# Redis 配置
REDIS_URL=redis://127.0.0.1:6379/1
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# CORS 配置
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173

# 邮件配置
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@example.com

# 日志级别
DJANGO_LOG_LEVEL=INFO
```

## 调试技巧

### VS Code 调试功能

1. **断点调试**: 在代码中设置断点，使用 F5 启动调试
2. **变量监视**: 在调试面板中监视变量值
3. **调用堆栈**: 查看函数调用链
4. **条件断点**: 设置条件断点，只在特定条件下暂停

### 日志查看

- **Django 日志**: 查看 `Backend/logs/django.log`
- **控制台日志**: VS Code 集成终端显示实时日志
- **Celery 日志**: Celery Worker 和 Beat 的日志输出

### 性能监控

- **Django Debug Toolbar**: 在开发模式下自动启用
- **Vue DevTools**: 浏览器扩展，用于调试 Vue.js 应用

## 故障排除

### 常见问题

1. **端口占用**
   ```bash
   # 查看端口占用
   netstat -ano | findstr :8000
   # 或使用 lsof (macOS/Linux)
   lsof -ti:8000
   ```

2. **数据库连接错误**
   - 检查 MySQL 服务是否启动
   - 验证数据库配置和凭据
   - 确保数据库已创建

3. **Redis 连接错误**
   - 检查 Redis 服务是否启动
   - 验证 Redis 配置

4. **前端依赖问题**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

5. **Python 依赖问题**
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

### 性能优化建议

1. **开发时关闭不必要的服务**
   - 如果不需要后台任务，不要启动 Celery
   - 使用调试模式时注意性能影响

2. **数据库优化**
   - 定期清理开发数据库
   - 使用合适的索引

3. **前端优化**
   - 开发时使用 HMR (热模块替换)
   - 避免不必要的重新渲染

## 团队协作

### 代码风格

- **后端**: 遵循 PEP 8，使用 Black 和 isort 格式化
- **前端**: 使用 ESLint 和 Prettier 保持代码一致性

### Git 工作流

1. 功能开发在独立分支
2. 提交前运行测试和代码检查
3. 使用有意义的提交消息

### 代码审查

- 使用 Pull Request 进行代码审查
- 确保测试通过
- 检查代码风格和最佳实践

## 更多资源

- [Django 文档](https://docs.djangoproject.com/)
- [Vue.js 文档](https://vuejs.org/)
- [Vite 文档](https://vitejs.dev/)
- [VS Code 调试指南](https://code.visualstudio.com/docs/editor/debugging)
