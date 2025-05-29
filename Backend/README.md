# Django 后端项目

一个功能完整的模块化Django后端框架，支持MySQL数据库。

## 项目概述

这是一个现代化的Django后端项目，采用模块化架构设计，包含用户管理、身份认证、AI功能、元宇宙和社交功能等模块。

## 主要特性

- ✅ **模块化架构**: 按功能划分的应用模块
- ✅ **MySQL数据库**: 生产级数据库支持
- ✅ **RESTful API**: Django REST Framework
- ✅ **用户认证**: 完整的认证系统
- ✅ **权限管理**: 基于角色的访问控制
- ✅ **缓存支持**: Redis缓存
- ✅ **异步任务**: Celery支持
- ✅ **API文档**: 自动生成文档
- ✅ **安全性**: 多重安全防护
- ✅ **AI集成**: 多模型AI功能支持
- ✅ **元宇宙体验**: 虚拟世界和交互系统
- ✅ **社交网络**: 完整的社交功能

## 项目结构

```
Backend/
├── manage.py                    # Django管理脚本
├── requirements.txt             # 项目依赖
├── README.md                   # 项目说明
├── backend/                    # 主配置目录
│   ├── __init__.py
│   ├── settings.py             # 项目设置 ✅
│   ├── urls.py                 # 主URL配置 ✅
│   ├── wsgi.py                 # WSGI配置
│   ├── asgi.py                 # ASGI配置
│   └── celery.py               # Celery配置
└── apps/                       # 应用模块
    ├── users/                  # 用户管理 ✅
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py           # 用户模型
    │   ├── serializers.py      # 序列化器
    │   ├── views.py            # 视图
    │   ├── urls.py             # URL配置
    │   ├── admin.py            # 管理界面
    │   └── signals.py          # 信号处理
    ├── authentication/         # 身份认证 ✅
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py           # 认证模型
    │   ├── serializers.py      # 认证序列化器
    │   ├── views.py            # 认证视图 ✅
    │   ├── urls.py             # 认证URL ✅
    │   └── admin.py            # 管理界面 ✅
    ├── core/                   # 核心功能 ✅
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py           # 核心模型
    │   ├── views.py            # 核心视图
    │   ├── urls.py             # 核心URL
    │   ├── admin.py            # 管理界面
    │   └── exceptions.py       # 异常处理
    ├── ai/                     # AI功能 ✅
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py           # AI模型
    │   ├── serializers.py      # AI序列化器
    │   ├── views.py            # AI视图
    │   ├── urls.py             # AI URL
    │   ├── admin.py            # 管理界面
    │   └── signals.py          # 信号处理
    ├── metaverse/              # 元宇宙功能 ✅
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py           # 元宇宙模型
    │   ├── urls.py             # 元宇宙URL
    │   ├── serializers.py      # 序列化器 (待创建)
    │   ├── views.py            # 视图 (待创建)
    │   └── admin.py            # 管理界面 (待创建)
    └── social/                 # 社交功能 ✅
        ├── __init__.py
        ├── apps.py
        ├── urls.py             # 社交URL
        ├── models.py           # 社交模型 (待创建)
        ├── serializers.py      # 序列化器 (待创建)
        ├── views.py            # 视图 (待创建)
        └── admin.py            # 管理界面 (待创建)
```

## 已完成的功能

### 用户管理模块 (apps/users)
- ✅ 扩展用户模型 (User, UserProfile, UserLoginLog)
- ✅ 用户管理界面 (Django Admin)
- ✅ 用户API (注册、登录、个人资料管理)
- ✅ 用户权限和统计
- ✅ 信号处理 (自动创建用户档案、登录日志)

### 身份认证模块 (apps/authentication)
- ✅ 认证模型 (邮箱验证、密码重置、API密钥等)
- ✅ 认证序列化器 (登录、注册、密码重置等)
- ✅ 认证视图 (完整的认证功能)
- ✅ 认证URL配置 (完整的路由)
- ✅ 管理界面 (Django Admin)

### 核心功能模块 (apps/core)
- ✅ 核心模型 (系统日志、标签、附件等)
- ✅ 核心视图 (系统状态、健康检查)
- ✅ 核心URL配置
- ✅ 管理界面和异常处理

### AI功能模块 (apps/ai)
- ✅ AI模型管理 (多种AI模型支持)
- ✅ 聊天对话系统 (完整的对话管理)
- ✅ AI模板系统 (提示模板管理)
- ✅ 使用统计 (详细的使用追踪)
- ✅ OpenAI兼容接口
- ✅ 完整的API端点和管理界面

### 元宇宙功能模块 (apps/metaverse)
- ✅ 虚拟世界模型 (世界、形象、会话)
- ✅ 虚拟物品系统 (物品和实例管理)
- ✅ 活动系统 (事件和参与者)
- ✅ 权限管理 (世界访问控制)
- ✅ URL路由配置
- ⏳ 序列化器、视图和管理界面 (待完成)

### 社交功能模块 (apps/social)
- ✅ URL路由配置 (完整的社交功能端点)
- ⏳ 社交模型 (好友、群组、动态等) (待完成)
- ⏳ 序列化器、视图和管理界面 (待完成)

## 核心模型

### 用户模型 (User)
- 扩展Django默认用户模型
- 支持头像、生日、性别、简介等字段
- 社交媒体链接 (网站、GitHub)
- 账户设置 (验证状态、高级用户)
- 隐私设置 (JSON字段)

### 认证模型
- **EmailVerificationToken**: 邮箱验证令牌
- **PasswordResetToken**: 密码重置令牌
- **LoginAttempt**: 登录尝试记录
- **TwoFactorAuth**: 双因子认证
- **APIKey**: API密钥管理

### AI模型
- **AIModel**: AI模型管理
- **AIRequest**: AI请求记录
- **ChatConversation**: 聊天对话
- **ChatMessage**: 聊天消息
- **AITemplate**: AI模板
- **AIUsageStats**: 使用统计

### 元宇宙模型
- **VirtualWorld**: 虚拟世界
- **Avatar**: 虚拟形象
- **UserSession**: 用户会话
- **VirtualObject**: 虚拟物品
- **Event**: 活动事件
- **WorldPermission**: 世界权限

## 数据库配置

项目配置为使用MySQL数据库：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='backend_db'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}
```

## API端点

### 用户相关 API (/api/v1/users/)
- `GET/POST /api/v1/users/` - 用户列表/创建
- `GET/PUT/DELETE /api/v1/users/{id}/` - 用户详情
- `GET/PUT /api/v1/users/me/profile/` - 当前用户资料
- `PUT /api/v1/users/me/settings/` - 用户设置
- `POST /api/v1/users/me/password/` - 修改密码
- `GET /api/v1/users/search/` - 用户搜索

### 认证相关 API (/api/v1/auth/)
- `POST /api/v1/auth/login/` - 用户登录
- `POST /api/v1/auth/register/` - 用户注册
- `POST /api/v1/auth/logout/` - 用户登出
- `POST /api/v1/auth/password-reset/` - 密码重置
- `POST /api/v1/auth/verify-email/` - 邮箱验证
- `POST /api/v1/auth/refresh-token/` - 刷新令牌
- `POST /api/v1/auth/2fa/enable/` - 启用双因子认证

### AI功能 API (/api/v1/ai/)
- `GET /api/v1/ai/models/` - AI模型列表
- `GET /api/v1/ai/conversations/` - 对话列表
- `POST /api/v1/ai/chat/send/` - 发送消息
- `GET /api/v1/ai/templates/` - 模板列表
- `POST /api/v1/ai/chat/completions/` - OpenAI兼容接口
- `GET /api/v1/ai/stats/user/` - 用户统计

### 元宇宙 API (/api/v1/metaverse/)
- `GET /api/v1/metaverse/worlds/` - 虚拟世界列表
- `GET /api/v1/metaverse/avatars/` - 虚拟形象列表
- `POST /api/v1/metaverse/worlds/{id}/enter/` - 进入世界
- `GET /api/v1/metaverse/events/` - 活动列表
- `GET /api/v1/metaverse/objects/` - 虚拟物品列表

### 社交功能 API (/api/v1/social/)
- `GET /api/v1/social/friends/` - 好友列表
- `GET /api/v1/social/groups/` - 群组列表
- `GET /api/v1/social/posts/` - 动态列表
- `GET /api/v1/social/messages/` - 消息列表
- `GET /api/v1/social/notifications/` - 通知列表

### 核心功能 API (/api/v1/core/)
- `GET /api/v1/core/system/health/` - 系统健康检查
- `GET /api/v1/core/system/status/` - 系统状态
- `GET /api/v1/core/logs/` - 系统日志
- `GET /api/v1/core/tags/` - 标签管理

## 安装和运行

### 1. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 安装依赖
```bash
cd Backend
pip install -r requirements.txt
```

### 3. 配置环境变量
创建 `.env` 文件：
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=backend_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
REDIS_URL=redis://127.0.0.1:6379/1
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
```

### 4. 配置数据库
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE backend_db CHARACTER SET utf8mb4;
```

### 5. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级用户
```bash
python manage.py createsuperuser
```

### 7. 运行开发服务器
```bash
python manage.py runserver
```

### 8. 启动Celery (可选)
```bash
# 启动Celery Worker
celery -A backend worker -l info

# 启动Celery Beat (定时任务)
celery -A backend beat -l info
```

## 技术栈

- **Web框架**: Django 4.2.7
- **API框架**: Django REST Framework 3.14.0
- **数据库**: MySQL (mysqlclient 2.2.0)
- **缓存**: Redis (django-redis 5.4.0)
- **任务队列**: Celery 5.3.4
- **身份验证**: Token认证 + Session认证
- **CORS**: django-cors-headers 4.3.1
- **过滤**: django-filter 23.3
- **图像处理**: Pillow 10.1.0
- **API文档**: drf-spectacular 0.26.5
- **环境配置**: python-decouple 3.8

## 开发规范

- 遵循Django编码规范 (PEP 8)
- 使用类型提示
- 完整的文档字符串
- 单元测试覆盖
- 安全最佳实践
- 模块化设计
- RESTful API设计

## 项目特色功能

### AI集成
- 多种AI模型支持 (文本、图像、语音等)
- 聊天对话管理
- AI模板系统
- OpenAI兼容接口
- 使用统计和成本追踪

### 元宇宙体验
- 虚拟世界创建和管理
- 虚拟形象系统
- 实时会话管理
- 虚拟物品系统
- 活动和事件管理

### 社交网络
- 好友关系管理
- 群组功能
- 动态发布和互动
- 私信系统
- 通知系统
- 关注功能

## 下一步计划

1. ✅ 完成认证模块的视图和URL配置
2. ✅ 创建核心功能模块 (core)
3. ✅ 创建AI功能模块 (ai)
4. ✅ 创建元宇宙功能模块 (metaverse) - 基础架构
5. ✅ 创建社交功能模块 (social) - 基础架构
6. ⏳ 完善元宇宙模块的序列化器、视图和管理界面
7. ⏳ 完善社交模块的模型、序列化器、视图和管理界面
8. 📋 添加单元测试
9. 📋 完善API文档
10. 📋 部署配置

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
