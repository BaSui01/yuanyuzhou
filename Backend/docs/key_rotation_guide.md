# 密钥定时轮换系统使用指南

## 概述

本系统提供了一个完整的密钥自动轮换解决方案，包括密钥生成、定时轮换、备份恢复、监控告警等功能。系统支持多种使用方式，从简单的手动执行到完全自动化的定时轮换。

## 系统架构

```
密钥轮换系统
├── key_rotation_manager.py    # 核心密钥管理器
├── key_scheduler.py          # 定时任务调度器
├── apps/core/tasks.py        # Celery后台任务
├── apps/core/management/commands/rotate_keys.py  # Django管理命令
└── docs/key_rotation_guide.md  # 使用指南
```

## 功能特性

### ✨ 核心功能
- 🔄 **自动密钥轮换**: 基于时间间隔的自动轮换
- 🔐 **多种密钥类型**: 支持随机、十六进制、Base64等多种密钥格式
- 💾 **自动备份**: 轮换前自动创建备份文件
- 📊 **详细日志**: 完整的操作日志和轮换历史
- ✅ **密钥验证**: 自动验证密钥格式和有效性
- 🗂️ **备份管理**: 自动清理旧备份，保持指定数量

### 🛠️ 管理功能
- 📋 **Django管理命令**: 集成到Django项目中
- ⏰ **Celery定时任务**: 支持后台异步执行
- 🎯 **灵活调度**: 支持间隔调度和Cron表达式
- 📈 **监控报告**: 自动生成轮换报告
- 🔧 **命令行工具**: 独立的命令行管理界面

## 快速开始

### 1. 环境配置

确保已安装必要的依赖：

```bash
pip install celery redis django-celery-beat
```

### 2. 启用密钥轮换

在 `.env` 文件中启用密钥轮换：

```env
# 启用自动密钥轮换
KEY_ROTATION_ENABLED=True

# 密钥轮换间隔（小时）
KEY_ROTATION_INTERVAL=24

# 备份密钥数量
KEY_BACKUP_COUNT=3
```

### 3. 手动轮换测试

```bash
# 验证当前密钥
python manage.py rotate_keys --validate-only

# 模拟轮换（不实际执行）
python manage.py rotate_keys --dry-run

# 执行完整轮换
python manage.py rotate_keys --force
```

## 使用方法

### 方法一：Django 管理命令

#### 基本命令

```bash
# 验证密钥有效性
python manage.py rotate_keys --validate-only

# 模拟轮换
python manage.py rotate_keys --dry-run

# 强制轮换所有密钥
python manage.py rotate_keys --force

# 轮换指定密钥
python manage.py rotate_keys --keys CRYPTO_KEY JWT_SECRET --force

# 使用自定义环境文件
python manage.py rotate_keys --env-file /path/to/.env --backup-dir /path/to/backups
```

#### 输出示例

```
验证密钥有效性...

密钥验证结果:
  ✓ CRYPTO_KEY
  ✓ CRYPTO_IV
  ✓ TRANSPORT_KEY
  ✓ SECRET_KEY
  ✓ JWT_SECRET
  ✓ API_KEY
  ✗ WEBHOOK_SECRET

存在无效密钥，建议执行轮换
```

### 方法二：Python 脚本直接调用

```python
from key_rotation_manager import KeyRotationManager

# 创建管理器实例
manager = KeyRotationManager()

# 验证密钥
validation_results = manager.validate_keys()
print("验证结果:", validation_results)

# 生成新密钥
new_keys = manager.generate_new_keys(['CRYPTO_KEY', 'JWT_SECRET'])
print("新密钥:", new_keys)

# 执行轮换
success = manager.rotate_keys(force=True)
print("轮换结果:", success)
```

### 方法三：命令行工具

```bash
# 生成新密钥并输出到控制台
python key_rotation_manager.py generate

# 生成指定密钥
python key_rotation_manager.py generate --keys CRYPTO_KEY JWT_SECRET

# 保存到文件
python key_rotation_manager.py generate --output new_keys.env

# 执行轮换
python key_rotation_manager.py rotate --force

# 创建备份
python key_rotation_manager.py backup

# 查看备份列表
python key_rotation_manager.py list-backups

# 从备份恢复
python key_rotation_manager.py restore backup_file.env
```

### 方法四：Celery 后台任务

#### 启动 Celery 服务

```bash
# 启动 Celery Worker
celery -A backend worker -l info

# 启动 Celery Beat（定时任务）
celery -A backend beat -l info
```

#### 手动触发任务

```python
from apps.core.tasks import rotate_encryption_keys, validate_encryption_keys

# 异步执行密钥轮换
task = rotate_encryption_keys.delay()
print(f"任务ID: {task.id}")

# 获取任务结果
result = task.get()
print("轮换结果:", result)

# 验证密钥
validation_task = validate_encryption_keys.delay()
validation_result = validation_task.get()
print("验证结果:", validation_result)
```

## 定时任务配置

### 设置默认调度

```bash
# 设置开发环境定时任务
python key_scheduler.py setup-default

# 设置生产环境定时任务
python key_scheduler.py setup-production

# 查看当前任务
python key_scheduler.py list
```

### 自定义调度

```bash
# 创建间隔任务（每6小时执行一次密钥验证）
python key_scheduler.py create --task-name key_validation --interval 6 --interval-type hours

# 创建Cron任务（每天凌晨2点执行备份清理）
python key_scheduler.py create --task-name backup_cleanup --hour 2 --minute 0

# 禁用所有任务
python key_scheduler.py disable-all

# 启用所有任务
python key_scheduler.py enable-all
```

### 默认调度配置

| 任务 | 默认调度 | 描述 |
|-----|---------|------|
| `key_rotation_check` | 每小时 | 检查是否需要轮换密钥 |
| `key_validation` | 每6小时 | 验证密钥有效性 |
| `backup_cleanup` | 每天凌晨2点 | 清理旧备份文件 |
| `generate_report` | 每周一上午9点 | 生成轮换报告 |

## 高级配置

### 密钥配置

系统支持以下类型的密钥：

```python
key_configs = {
    'CRYPTO_KEY': KeyConfig('CRYPTO_KEY', 64, 'random', '应用层加密主密钥', True),
    'CRYPTO_IV': KeyConfig('CRYPTO_IV', 16, 'alphanumeric', '应用层加密初始向量', True),
    'TRANSPORT_KEY': KeyConfig('TRANSPORT_KEY', 64, 'random', '传输层加密主密钥', True),
    'SECRET_KEY': KeyConfig('SECRET_KEY', 50, 'random', 'Django SECRET_KEY', True),
    'JWT_SECRET': KeyConfig('JWT_SECRET', 32, 'base64', 'JWT密钥', True),
    'API_KEY': KeyConfig('API_KEY', 16, 'hex', 'API密钥', False),
    'WEBHOOK_SECRET': KeyConfig('WEBHOOK_SECRET', 32, 'random', 'Webhook签名密钥', False),
}
```

### 环境变量配置

```env
# 基础配置
KEY_ROTATION_ENABLED=True              # 启用密钥轮换
KEY_ROTATION_INTERVAL=24               # 轮换间隔（小时）
KEY_BACKUP_COUNT=3                     # 保留备份数量

# 安全配置
ENCRYPTION_DEBUG_LOGS=False            # 调试日志（生产环境设为False）
ENCRYPTION_LOG_LEVEL=INFO              # 日志级别
ENCRYPTION_ALERT_FAILURES=True         # 启用失败告警
ENCRYPTION_FAILURE_THRESHOLD=10        # 失败告警阈值

# 性能配置
ENCRYPTION_MAX_SESSIONS=1000           # 最大并发会话数
ENCRYPTION_TIMEOUT=30                  # 操作超时时间
```

## 监控和报告

### 生成报告

```python
from apps.core.tasks import generate_key_rotation_report

# 生成详细报告
report_task = generate_key_rotation_report.delay()
report = report_task.get()

print("密钥概况:", report['key_summary'])
print("验证结果:", report['validation_results'])
print("备份信息:", report['backup_info'])
print("轮换历史:", report['rotation_history'])
```

### 报告内容

报告包含以下信息：
- 密钥概况统计
- 密钥验证结果
- 备份文件信息
- 轮换历史记录
- 系统配置信息

### 日志监控

系统会记录详细的操作日志：

```
2025-05-29 22:00:00 - key_rotation - INFO - 开始密钥轮换操作
2025-05-29 22:00:01 - key_rotation - INFO - 生成新密钥: CRYPTO_KEY
2025-05-29 22:00:01 - key_rotation - INFO - 生成新密钥: JWT_SECRET
2025-05-29 22:00:02 - key_rotation - INFO - 创建备份: key_backups/env_backup_20250529_220002.env
2025-05-29 22:00:03 - key_rotation - INFO - 成功更新环境文件: .env
2025-05-29 22:00:03 - key_rotation - INFO - 密钥轮换完成
```

## 安全注意事项

### 🔒 安全最佳实践

1. **文件权限**: 确保 `.env` 文件和备份文件有适当的权限
   ```bash
   chmod 600 .env
   chmod 700 key_backups/
   ```

2. **备份安全**: 备份文件包含敏感信息，应安全存储
   ```bash
   # 加密备份文件
   gpg --cipher-algo AES256 --compress-algo 1 --s2k-mode 3 \
       --s2k-digest-algo SHA512 --s2k-count 65536 --symmetric \
       --output backup.env.gpg backup.env
   ```

3. **网络安全**: 在生产环境中，考虑使用密钥管理服务（如AWS KMS、Azure Key Vault）

4. **访问控制**: 限制对密钥轮换功能的访问权限

### ⚠️ 重要提醒

1. **服务重启**: 密钥轮换后需要重启Django应用以加载新密钥
2. **数据一致性**: 确保在轮换前没有正在进行的加密操作
3. **备份验证**: 定期验证备份文件的完整性
4. **监控告警**: 设置适当的监控和告警机制

## 故障排除

### 常见问题

#### 1. 密钥验证失败
```bash
# 检查密钥格式
python manage.py rotate_keys --validate-only

# 强制重新生成问题密钥
python manage.py rotate_keys --keys PROBLEMATIC_KEY --force
```

#### 2. 备份文件损坏
```bash
# 列出可用备份
python key_rotation_manager.py list-backups

# 从最近的有效备份恢复
python key_rotation_manager.py restore backup_file.env
```

#### 3. 定时任务不执行
```bash
# 检查Celery服务状态
celery -A backend inspect active

# 检查定时任务配置
python key_scheduler.py list

# 重新设置定时任务
python key_scheduler.py setup-default
```

#### 4. 权限问题
```bash
# 检查文件权限
ls -la .env key_backups/

# 修复权限
chmod 600 .env
chmod -R 700 key_backups/
```

### 调试模式

启用调试日志来诊断问题：

```env
# 在 .env 文件中启用调试
ENCRYPTION_DEBUG_LOGS=True
ENCRYPTION_LOG_LEVEL=DEBUG
```

### 紧急恢复

如果密钥轮换导致系统问题：

1. **立即停止轮换任务**:
   ```python
   from django_celery_beat.models import PeriodicTask
   PeriodicTask.objects.filter(name__startswith='key_rotation_').update(enabled=False)
   ```

2. **从备份恢复**:
   ```bash
   python key_rotation_manager.py restore key_backups/env_backup_YYYYMMDD_HHMMSS.env
   ```

3. **重启服务**:
   ```bash
   # 重启Django应用
   systemctl restart your-django-app

   # 重启Celery服务
   systemctl restart celery-worker
   systemctl restart celery-beat
   ```

## 性能优化

### 大规模部署

对于大规模部署，考虑以下优化：

1. **分布式轮换**: 将不同类型的密钥分配到不同的任务队列
2. **错峰执行**: 避免在业务高峰期执行轮换
3. **批量操作**: 合并多个密钥的轮换操作
4. **异步通知**: 使用异步方式通知相关服务

### 监控指标

建议监控以下指标：

- 轮换成功率
- 轮换执行时间
- 密钥验证通过率
- 备份文件大小和数量
- 任务队列长度

## 版本升级

### 升级注意事项

1. **备份当前配置**: 升级前创建完整备份
2. **测试兼容性**: 在测试环境验证新版本
3. **逐步部署**: 使用蓝绿部署或滚动更新
4. **监控升级**: 密切监控升级后的系统状态

### 迁移脚本

如果需要迁移现有的密钥格式：

```python
# 迁移示例
from key_rotation_manager import KeyRotationManager

manager = KeyRotationManager()

# 备份当前配置
backup_file = manager.create_backup()

# 生成新格式密钥
new_keys = manager.generate_new_keys()

# 更新配置
manager.update_env_file(new_keys)
```

## 支持和反馈

如果遇到问题或需要新功能，请：

1. 查看日志文件 `key_rotation.log`
2. 检查轮换历史 `key_update_history.json`
3. 运行诊断命令验证系统状态
4. 提供详细的错误信息和环境配置

---

**注意**: 本系统涉及敏感的安全操作，请在生产环境使用前充分测试，并确保有适当的备份和恢复计划。
