<template>
  <div class="settings-view">
    <div class="settings-header">
      <div class="header-left">
        <h2>系统设置</h2>
        <p>配置和管理系统设置</p>
      </div>
      <div class="header-right">
        <Button label="备份设置" icon="pi pi-download" class="p-button-outlined mr-2" @click="backupSettings" />
        <Button label="恢复设置" icon="pi pi-upload" class="p-button-outlined" @click="openRestoreDialog" />
      </div>
    </div>

    <div class="settings-content">
      <TabView>
        <TabPanel header="系统设置">
          <div class="settings-form" v-if="systemSettings">
            <div class="form-group">
              <label for="siteName">网站名称</label>
              <InputText id="siteName" v-model="systemSettings.siteName" class="w-full" />
            </div>

            <div class="form-group">
              <label for="siteDescription">网站描述</label>
              <Textarea id="siteDescription" v-model="systemSettings.siteDescription" rows="3" class="w-full" />
            </div>

            <div class="form-group">
              <label for="contactEmail">联系邮箱</label>
              <InputText id="contactEmail" v-model="systemSettings.contactEmail" type="email" class="w-full" />
            </div>

            <div class="form-group">
              <label for="timezone">时区</label>
              <Dropdown id="timezone" v-model="systemSettings.timezone" :options="timezoneOptions" optionLabel="name" class="w-full" />
            </div>

            <div class="form-group">
              <label for="dateFormat">日期格式</label>
              <Dropdown id="dateFormat" v-model="systemSettings.dateFormat" :options="dateFormatOptions" optionLabel="name" class="w-full" />
            </div>

            <div class="form-group">
              <label for="maintenanceMode">维护模式</label>
              <div class="switch-container">
                <InputSwitch id="maintenanceMode" v-model="systemSettings.maintenanceMode" />
                <span>{{ systemSettings.maintenanceMode ? '已启用' : '已禁用' }}</span>
              </div>
            </div>

            <div class="form-group" v-if="systemSettings.maintenanceMode">
              <label for="maintenanceMessage">维护信息</label>
              <Textarea id="maintenanceMessage" v-model="systemSettings.maintenanceMessage" rows="3" class="w-full" />
            </div>

            <div class="form-actions">
              <Button label="保存系统设置" icon="pi pi-save" @click="saveSystemSettings" :loading="submitting" />
            </div>
          </div>
        </TabPanel>

        <TabPanel header="安全设置">
          <div class="settings-form" v-if="securitySettings">
            <div class="form-group">
              <label for="passwordPolicy">密码策略</label>
              <Dropdown id="passwordPolicy" v-model="securitySettings.passwordPolicy" :options="passwordPolicyOptions" optionLabel="name" class="w-full" />
            </div>

            <div class="form-group">
              <label for="sessionTimeout">会话超时（分钟）</label>
              <InputNumber id="sessionTimeout" v-model="securitySettings.sessionTimeout" class="w-full" />
            </div>

            <div class="form-group">
              <label for="maxLoginAttempts">最大登录尝试次数</label>
              <InputNumber id="maxLoginAttempts" v-model="securitySettings.maxLoginAttempts" class="w-full" />
            </div>

            <div class="form-group">
              <label for="lockoutDuration">账户锁定时间（分钟）</label>
              <InputNumber id="lockoutDuration" v-model="securitySettings.lockoutDuration" class="w-full" />
            </div>

            <div class="form-group">
              <label for="twoFactorAuth">两步验证</label>
              <div class="switch-container">
                <InputSwitch id="twoFactorAuth" v-model="securitySettings.twoFactorAuth" />
                <span>{{ securitySettings.twoFactorAuth ? '已启用' : '已禁用' }}</span>
              </div>
            </div>

            <div class="form-group">
              <label for="forceHttps">强制HTTPS</label>
              <div class="switch-container">
                <InputSwitch id="forceHttps" v-model="securitySettings.forceHttps" />
                <span>{{ securitySettings.forceHttps ? '已启用' : '已禁用' }}</span>
              </div>
            </div>

            <div class="form-actions">
              <Button label="保存安全设置" icon="pi pi-save" @click="saveSecuritySettings" :loading="submitting" />
            </div>
          </div>
        </TabPanel>

        <TabPanel header="邮件设置">
          <div class="settings-form" v-if="emailSettings">
            <div class="form-group">
              <label for="smtpHost">SMTP服务器</label>
              <InputText id="smtpHost" v-model="emailSettings.smtpHost" class="w-full" />
            </div>

            <div class="form-group">
              <label for="smtpPort">SMTP端口</label>
              <InputNumber id="smtpPort" v-model="emailSettings.smtpPort" class="w-full" />
            </div>

            <div class="form-group">
              <label for="smtpUsername">SMTP用户名</label>
              <InputText id="smtpUsername" v-model="emailSettings.smtpUsername" class="w-full" />
            </div>

            <div class="form-group">
              <label for="smtpPassword">SMTP密码</label>
              <Password id="smtpPassword" v-model="emailSettings.smtpPassword" toggleMask class="w-full" />
            </div>

            <div class="form-group">
              <label for="smtpEncryption">加密方式</label>
              <Dropdown id="smtpEncryption" v-model="emailSettings.smtpEncryption" :options="encryptionOptions" optionLabel="name" class="w-full" />
            </div>

            <div class="form-group">
              <label for="fromEmail">发件人邮箱</label>
              <InputText id="fromEmail" v-model="emailSettings.fromEmail" type="email" class="w-full" />
            </div>

            <div class="form-group">
              <label for="fromName">发件人名称</label>
              <InputText id="fromName" v-model="emailSettings.fromName" class="w-full" />
            </div>

            <div class="form-actions">
              <Button label="发送测试邮件" icon="pi pi-envelope" class="p-button-outlined mr-2" @click="openTestEmailDialog" />
              <Button label="保存邮件设置" icon="pi pi-save" @click="saveEmailSettings" :loading="submitting" />
            </div>
          </div>
        </TabPanel>

        <TabPanel header="存储设置">
          <div class="settings-form" v-if="storageSettings">
            <div class="form-group">
              <label for="storageType">存储类型</label>
              <Dropdown id="storageType" v-model="storageSettings.storageType" :options="storageTypeOptions" optionLabel="name" class="w-full" />
            </div>

            <div v-if="storageSettings.storageType.value === 's3'">
              <div class="form-group">
                <label for="s3AccessKey">访问密钥</label>
                <InputText id="s3AccessKey" v-model="storageSettings.s3.accessKey" class="w-full" />
              </div>

              <div class="form-group">
                <label for="s3SecretKey">密钥</label>
                <Password id="s3SecretKey" v-model="storageSettings.s3.secretKey" toggleMask class="w-full" />
              </div>

              <div class="form-group">
                <label for="s3Bucket">存储桶</label>
                <InputText id="s3Bucket" v-model="storageSettings.s3.bucket" class="w-full" />
              </div>

              <div class="form-group">
                <label for="s3Region">区域</label>
                <InputText id="s3Region" v-model="storageSettings.s3.region" class="w-full" />
              </div>

              <div class="form-group">
                <label for="s3Endpoint">终端节点</label>
                <InputText id="s3Endpoint" v-model="storageSettings.s3.endpoint" class="w-full" />
              </div>
            </div>

            <div v-if="storageSettings.storageType.value === 'local'">
              <div class="form-group">
                <label for="localPath">本地存储路径</label>
                <InputText id="localPath" v-model="storageSettings.local.path" class="w-full" />
              </div>
            </div>

            <div class="form-group">
              <label for="maxUploadSize">最大上传大小（MB）</label>
              <InputNumber id="maxUploadSize" v-model="storageSettings.maxUploadSize" class="w-full" />
            </div>

            <div class="form-group">
              <label for="allowedFileTypes">允许的文件类型</label>
              <Chips id="allowedFileTypes" v-model="storageSettings.allowedFileTypes" class="w-full" />
              <small>输入文件扩展名后按回车添加（如：jpg, png, pdf）</small>
            </div>

            <div class="form-actions">
              <Button label="保存存储设置" icon="pi pi-save" @click="saveStorageSettings" :loading="submitting" />
            </div>
          </div>
        </TabPanel>

        <TabPanel header="AI设置">
          <div class="settings-form" v-if="aiSettings">
            <div class="form-group">
              <label for="aiProvider">AI提供商</label>
              <Dropdown id="aiProvider" v-model="aiSettings.provider" :options="aiProviderOptions" optionLabel="name" class="w-full" />
            </div>

            <div class="form-group">
              <label for="apiKey">API密钥</label>
              <Password id="apiKey" v-model="aiSettings.apiKey" toggleMask class="w-full" />
            </div>

            <div class="form-group">
              <label for="apiEndpoint">API终端节点</label>
              <InputText id="apiEndpoint" v-model="aiSettings.apiEndpoint" class="w-full" />
            </div>

            <div class="form-group">
              <label for="defaultModel">默认模型</label>
              <Dropdown id="defaultModel" v-model="aiSettings.defaultModel" :options="aiModelOptions" optionLabel="name" class="w-full" />
            </div>

            <div class="form-group">
              <label for="maxTokens">最大令牌数</label>
              <InputNumber id="maxTokens" v-model="aiSettings.maxTokens" class="w-full" />
            </div>

            <div class="form-group">
              <label for="temperature">温度</label>
              <Slider id="temperature" v-model="aiSettings.temperature" :min="0" :max="2" :step="0.1" class="w-full" />
              <div class="slider-value">{{ aiSettings.temperature }}</div>
            </div>

            <div class="form-group">
              <label for="aiRateLimit">速率限制（每分钟请求数）</label>
              <InputNumber id="aiRateLimit" v-model="aiSettings.rateLimit" class="w-full" />
            </div>

            <div class="form-actions">
              <Button label="保存AI设置" icon="pi pi-save" @click="saveAISettings" :loading="submitting" />
            </div>
          </div>
        </TabPanel>
      </TabView>
    </div>

    <Dialog v-model:visible="testEmailDialog" header="发送测试邮件" :style="{ width: '450px' }" :modal="true">
      <div class="p-fluid">
        <div class="p-field mb-3">
          <label for="testEmail">收件人邮箱</label>
          <InputText id="testEmail" v-model="testEmail" type="email" required />
        </div>
        <div class="p-field mb-3">
          <label for="testSubject">主题</label>
          <InputText id="testSubject" v-model="testEmailSubject" required />
        </div>
        <div class="p-field mb-3">
          <label for="testMessage">内容</label>
          <Textarea id="testMessage" v-model="testEmailMessage" rows="5" required />
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="testEmailDialog = false" />
        <Button label="发送" icon="pi pi-send" @click="sendTestEmail" :loading="submitting" />
      </template>
    </Dialog>

    <Dialog v-model:visible="restoreDialog" header="恢复设置" :style="{ width: '450px' }" :modal="true">
      <div class="p-fluid">
        <div class="p-field mb-3">
          <label for="restoreFile">备份文件</label>
          <div class="file-upload">
            <input type="file" ref="fileInput" @change="handleFileUpload" accept=".json" />
            <Button label="选择文件" icon="pi pi-upload" class="p-button-outlined" @click="triggerFileInput" />
            <span v-if="selectedFile">{{ selectedFile.name }}</span>
          </div>
        </div>
        <div class="warning-message">
          <i class="pi pi-exclamation-triangle"></i>
          <span>警告：恢复设置将覆盖当前所有系统设置，请确保备份文件正确。</span>
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="restoreDialog = false" />
        <Button label="恢复" icon="pi pi-refresh" @click="restoreSettings" :loading="submitting" :disabled="!selectedFile" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAdminSettings } from './composables/useAdminSettings'

export default {
  name: 'SettingsView',
  setup() {
    const {
      systemSettings,
      securitySettings,
      emailSettings,
      storageSettings,
      aiSettings,
      loading,
      submitting,
      getSystemSettings,
      updateSystemSettings,
      getSecuritySettings,
      updateSecuritySettings,
      getEmailSettings,
      updateEmailSettings,
      sendTestEmail: apiSendTestEmail,
      getStorageSettings,
      updateStorageSettings,
      getAISettings,
      updateAISettings,
      getAllSettings,
      backupSettings: apiBackupSettings,
      restoreSettings: apiRestoreSettings
    } = useAdminSettings()

    // 对话框
    const testEmailDialog = ref(false)
    const restoreDialog = ref(false)

    // 测试邮件表单
    const testEmail = ref('')
    const testEmailSubject = ref('测试邮件')
    const testEmailMessage = ref('这是一封测试邮件，用于验证邮件设置是否正确。')

    // 文件上传
    const fileInput = ref(null)
    const selectedFile = ref(null)

    // 选项
    const timezoneOptions = [
      { name: '(GMT+08:00) 北京', value: 'Asia/Shanghai' },
      { name: '(GMT+08:00) 香港', value: 'Asia/Hong_Kong' },
      { name: '(GMT+08:00) 台北', value: 'Asia/Taipei' },
      { name: '(GMT+09:00) 东京', value: 'Asia/Tokyo' },
      { name: '(GMT+00:00) 伦敦', value: 'Europe/London' },
      { name: '(GMT-05:00) 纽约', value: 'America/New_York' }
    ]

    const dateFormatOptions = [
      { name: 'YYYY-MM-DD', value: 'YYYY-MM-DD' },
      { name: 'DD/MM/YYYY', value: 'DD/MM/YYYY' },
      { name: 'MM/DD/YYYY', value: 'MM/DD/YYYY' },
      { name: 'YYYY年MM月DD日', value: 'YYYY年MM月DD日' }
    ]

    const passwordPolicyOptions = [
      { name: '低（至少6个字符）', value: 'low' },
      { name: '中（至少8个字符，包含数字）', value: 'medium' },
      { name: '高（至少10个字符，包含数字、大小写字母和特殊字符）', value: 'high' }
    ]

    const encryptionOptions = [
      { name: 'None', value: 'none' },
      { name: 'SSL', value: 'ssl' },
      { name: 'TLS', value: 'tls' }
    ]

    const storageTypeOptions = [
      { name: '本地存储', value: 'local' },
      { name: 'Amazon S3', value: 's3' },
      { name: '阿里云OSS', value: 'aliyun' }
    ]

    const aiProviderOptions = [
      { name: 'OpenAI', value: 'openai' },
      { name: '百度文心', value: 'baidu' },
      { name: '讯飞星火', value: 'xfyun' }
    ]

    const aiModelOptions = [
      { name: 'GPT-3.5', value: 'gpt-3.5-turbo' },
      { name: 'GPT-4', value: 'gpt-4' },
      { name: 'Claude', value: 'claude' },
      { name: '文心一言', value: 'ernie-bot' }
    ]

    // 保存系统设置
    const saveSystemSettings = async () => {
      await updateSystemSettings(systemSettings.value)
    }

    // 保存安全设置
    const saveSecuritySettings = async () => {
      await updateSecuritySettings(securitySettings.value)
    }

    // 保存邮件设置
    const saveEmailSettings = async () => {
      await updateEmailSettings(emailSettings.value)
    }

    // 保存存储设置
    const saveStorageSettings = async () => {
      await updateStorageSettings(storageSettings.value)
    }

    // 保存AI设置
    const saveAISettings = async () => {
      await updateAISettings(aiSettings.value)
    }

    // 打开测试邮件对话框
    const openTestEmailDialog = () => {
      testEmail.value = emailSettings.value.fromEmail
      testEmailDialog.value = true
    }

    // 发送测试邮件
    const sendTestEmail = async () => {
      await apiSendTestEmail({
        to: testEmail.value,
        subject: testEmailSubject.value,
        message: testEmailMessage.value
      })
      testEmailDialog.value = false
    }

    // 备份设置
    const backupSettings = async () => {
      await apiBackupSettings()
    }

    // 打开恢复对话框
    const openRestoreDialog = () => {
      selectedFile.value = null
      restoreDialog.value = true
    }

    // 触发文件选择
    const triggerFileInput = () => {
      fileInput.value.click()
    }

    // 处理文件上传
    const handleFileUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedFile.value = file
      }
    }

    // 恢复设置
    const restoreSettings = async () => {
      if (selectedFile.value) {
        await apiRestoreSettings(selectedFile.value)
        restoreDialog.value = false
      }
    }

    // 初始化
    onMounted(async () => {
      await getAllSettings()
    })

    return {
      systemSettings,
      securitySettings,
      emailSettings,
      storageSettings,
      aiSettings,
      loading,
      submitting,
      testEmailDialog,
      restoreDialog,
      testEmail,
      testEmailSubject,
      testEmailMessage,
      fileInput,
      selectedFile,
      timezoneOptions,
      dateFormatOptions,
      passwordPolicyOptions,
      encryptionOptions,
      storageTypeOptions,
      aiProviderOptions,
      aiModelOptions,
      saveSystemSettings,
      saveSecuritySettings,
      saveEmailSettings,
      saveStorageSettings,
      saveAISettings,
      openTestEmailDialog,
      sendTestEmail,
      backupSettings,
      openRestoreDialog,
      triggerFileInput,
      handleFileUpload,
      restoreSettings
    }
  }
}
</script>

<style lang="scss" scoped>
.settings-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-left {
    h2 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 600;
    }

    p {
      margin: 4px 0 0;
      color: #666;
    }
  }
}

.settings-content {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.settings-form {
  padding: 16px 0;

  .form-group {
    margin-bottom: 24px;

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
    }

    small {
      display: block;
      margin-top: 4px;
      color: #666;
    }

    .switch-container {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .slider-value {
      margin-top: 8px;
      text-align: right;
    }
  }

  .form-actions {
    margin-top: 32px;
    display: flex;
    justify-content: flex-end;
  }
}

.file-upload {
  display: flex;
  align-items: center;
  gap: 12px;

  input[type="file"] {
    display: none;
  }
}

.warning-message {
  margin-top: 16px;
  padding: 12px;
  background-color: #fff3cd;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;

  i {
    color: #856404;
  }

  span {
    color: #856404;
    font-size: 0.9rem;
  }
}
</style>
