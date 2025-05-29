# 密钥管理指南

## 概述

本文档描述了元宇宙社交平台的密钥管理最佳实践和安全指南。

## 密钥类型

### 1. 加密密钥
- **CRYPTO_KEY**: 应用层数据加密主密钥（64字符）
- **CRYPTO_IV**: 加密初始向量（16字符）
- **TRANSPORT_KEY**: 传输层加密密钥（64字符）

### 2. 框架密钥
- **SECRET_KEY**: Django框架密钥
- **JWT_SECRET**: JWT令牌签名密钥
- **API_KEY**: API访问密钥

### 3. 第三方服务密钥
- **OPENAI_API_KEY**: OpenAI API密钥
- **BAIDU_API_KEY**: 百度API密钥
- **AWS_ACCESS_KEY_ID**: AWS访问密钥
- **EMAIL_HOST_PASSWORD**: 邮件服务密码

## 密钥生成

### 自动生成
使用提供的密钥生成脚本：

```bash
cd Backend
python generate_keys.py
```

### 手动生成
使用Python生成安全密钥：

```python
import secrets
import string

def generate_key(length=64):
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# 生成64字符密钥
crypto_key = generate_key(64)
print(f"CRYPTO_KEY={crypto_key}")
```

## 安全存储

### 开发环境
1. 使用 `.env` 文件存储密钥
2. 确保 `.env` 文件已添加到 `.gitignore`
3. 不要在代码中硬编码密钥

### 生产环境
1. **推荐**: 使用云密钥管理服务
   - AWS KMS (Key Management Service)
   - Azure Key Vault
   - Google Cloud KMS
   - 阿里云KMS

2. **备选**: 环境变量
   - 在服务器上设置环境变量
   - 使用Docker secrets
   - 使用Kubernetes secrets

3. **不推荐**: 配置文件
   - 避免在配置文件中存储明文密钥

## 密钥轮换

### 轮换周期
- **高风险密钥**: 每月轮换（API密钥、数据库密码）
- **中风险密钥**: 每季度轮换（加密密钥、JWT密钥）
- **低风险密钥**: 每半年轮换（内部通信密钥）

### 轮换步骤
1. 生成新密钥
2. 更新应用配置
3. 测试应用功能
4. 逐步部署到生产环境
5. 验证新密钥正常工作
6. 废止旧密钥

### 自动轮换
在 `.env` 中启用自动轮换：

```bash
KEY_ROTATION_ENABLED=True
KEY_ROTATION_INTERVAL=24  # 小时
KEY_BACKUP_COUNT=3
```

## 密钥备份

### 备份策略
1. **冗余存储**: 在多个安全位置存储密钥备份
2. **加密备份**: 使用独立的密钥加密备份数据
3. **版本控制**: 保留历史版本的密钥用于数据恢复
4. **定期测试**: 定期验证备份的完整性和可用性

### 备份位置
- 云存储服务（加密）
- 离线安全存储
- 密钥管理服务
- 企业保险箱

## 访问控制

### 最小权限原则
1. 只给予必要的密钥访问权限
2. 定期审查密钥访问权限
3. 使用角色基础的访问控制

### 访问审计
1. 记录所有密钥访问操作
2. 监控异常的密钥使用
3. 定期审查访问日志

## 安全检查清单

### 部署前检查
- [ ] 所有密钥都已从代码中移除
- [ ] `.env` 文件已添加到 `.gitignore`
- [ ] 使用强随机密钥生成器生成的密钥
- [ ] 密钥长度符合安全要求
- [ ] 启用了传输层加密 (HTTPS/TLS)

### 运行时监控
- [ ] 启用密钥使用监控
- [ ] 设置异常告警
- [ ] 定期检查密钥有效性
- [ ] 监控密钥泄露风险

### 定期维护
- [ ] 按计划轮换密钥
- [ ] 更新密钥备份
- [ ] 审查访问权限
- [ ] 测试密钥恢复流程

## 应急响应

### 密钥泄露处理
1. **立即行动**:
   - 禁用泄露的密钥
   - 生成新密钥
   - 更新应用配置

2. **影响评估**:
   - 确定泄露范围
   - 评估潜在损失
   - 通知相关人员

3. **恢复操作**:
   - 部署新密钥
   - 验证系统功能
   - 监控异常活动

4. **事后分析**:
   - 分析泄露原因
   - 改进安全措施
   - 更新应急预案

## 合规性

### 法规要求
- 遵守GDPR、CCPA等数据保护法规
- 符合行业安全标准（ISO 27001、SOC 2）
- 满足金融级安全要求（如果适用）

### 审计准备
1. 维护密钥生命周期文档
2. 保留访问日志和审计记录
3. 准备密钥管理政策文档
4. 定期进行安全评估

## 工具推荐

### 密钥管理工具
- **HashiCorp Vault**: 开源密钥管理
- **AWS KMS**: 云密钥管理服务
- **Azure Key Vault**: 微软云密钥管理
- **Google Cloud KMS**: 谷歌云密钥管理

### 监控工具
- **Datadog**: 应用性能监控
- **Splunk**: 日志分析和监控
- **Prometheus + Grafana**: 开源监控堆栈

## 联系信息

如有密钥管理相关问题，请联系：
- 安全团队: security@yuanyuzhou.com
- 技术支持: tech@yuanyuzhou.com
- 紧急联系: emergency@yuanyuzhou.com

---

**重要提醒**: 本文档包含安全敏感信息，请妥善保管，不要分享给未授权人员。
