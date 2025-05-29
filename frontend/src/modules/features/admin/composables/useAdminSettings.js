/**
 * 管理后台设置 composable
 */
import { ref, reactive } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { settings } from '../api/settings'

export function useAdminSettings() {
  const toast = useToast()
  const confirm = useConfirm()

  // 状态
  const systemSettings = ref(null)
  const securitySettings = ref(null)
  const emailSettings = ref(null)
  const storageSettings = ref(null)
  const aiSettings = ref(null)
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref(null)

  /**
   * 获取系统设置
   * @returns {Promise<Object>} - 返回系统设置
   */
  const getSystemSettings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await settings.getSystemSettings()
      systemSettings.value = response
      return systemSettings.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取系统设置失败'

      toast.add({
        severity: 'error',
        summary: '获取设置失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新系统设置
   * @param {Object} data - 系统设置数据
   * @returns {Promise<Object>} - 返回更新结果
   */
  const updateSystemSettings = async (data) => {
    submitting.value = true
    error.value = null

    try {
      const response = await settings.updateSystemSettings(data)
      systemSettings.value = response

      toast.add({
        severity: 'success',
        summary: '更新成功',
        detail: '系统设置已更新',
        life: 3000
      })

      return { success: true, settings: response }
    } catch (err) {
      error.value = err.response?.data?.message || '更新系统设置失败'

      toast.add({
        severity: 'error',
        summary: '更新失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 获取安全设置
   * @returns {Promise<Object>} - 返回安全设置
   */
  const getSecuritySettings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await settings.getSecuritySettings()
      securitySettings.value = response
      return securitySettings.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取安全设置失败'

      toast.add({
        severity: 'error',
        summary: '获取设置失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新安全设置
   * @param {Object} data - 安全设置数据
   * @returns {Promise<Object>} - 返回更新结果
   */
  const updateSecuritySettings = async (data) => {
    submitting.value = true
    error.value = null

    try {
      const response = await settings.updateSecuritySettings(data)
      securitySettings.value = response

      toast.add({
        severity: 'success',
        summary: '更新成功',
        detail: '安全设置已更新',
        life: 3000
      })

      return { success: true, settings: response }
    } catch (err) {
      error.value = err.response?.data?.message || '更新安全设置失败'

      toast.add({
        severity: 'error',
        summary: '更新失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 获取邮件设置
   * @returns {Promise<Object>} - 返回邮件设置
   */
  const getEmailSettings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await settings.getEmailSettings()
      emailSettings.value = response
      return emailSettings.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取邮件设置失败'

      toast.add({
        severity: 'error',
        summary: '获取设置失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新邮件设置
   * @param {Object} data - 邮件设置数据
   * @returns {Promise<Object>} - 返回更新结果
   */
  const updateEmailSettings = async (data) => {
    submitting.value = true
    error.value = null

    try {
      const response = await settings.updateEmailSettings(data)
      emailSettings.value = response

      toast.add({
        severity: 'success',
        summary: '更新成功',
        detail: '邮件设置已更新',
        life: 3000
      })

      return { success: true, settings: response }
    } catch (err) {
      error.value = err.response?.data?.message || '更新邮件设置失败'

      toast.add({
        severity: 'error',
        summary: '更新失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 发送测试邮件
   * @param {Object} data - 测试邮件数据
   * @returns {Promise<Object>} - 返回发送结果
   */
  const sendTestEmail = async (data) => {
    submitting.value = true
    error.value = null

    try {
      await settings.sendTestEmail(data)

      toast.add({
        severity: 'success',
        summary: '发送成功',
        detail: '测试邮件已发送',
        life: 3000
      })

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || '发送测试邮件失败'

      toast.add({
        severity: 'error',
        summary: '发送失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 获取存储设置
   * @returns {Promise<Object>} - 返回存储设置
   */
  const getStorageSettings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await settings.getStorageSettings()
      storageSettings.value = response
      return storageSettings.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取存储设置失败'

      toast.add({
        severity: 'error',
        summary: '获取设置失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新存储设置
   * @param {Object} data - 存储设置数据
   * @returns {Promise<Object>} - 返回更新结果
   */
  const updateStorageSettings = async (data) => {
    submitting.value = true
    error.value = null

    try {
      const response = await settings.updateStorageSettings(data)
      storageSettings.value = response

      toast.add({
        severity: 'success',
        summary: '更新成功',
        detail: '存储设置已更新',
        life: 3000
      })

      return { success: true, settings: response }
    } catch (err) {
      error.value = err.response?.data?.message || '更新存储设置失败'

      toast.add({
        severity: 'error',
        summary: '更新失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 获取AI设置
   * @returns {Promise<Object>} - 返回AI设置
   */
  const getAISettings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await settings.getAISettings()
      aiSettings.value = response
      return aiSettings.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取AI设置失败'

      toast.add({
        severity: 'error',
        summary: '获取设置失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新AI设置
   * @param {Object} data - AI设置数据
   * @returns {Promise<Object>} - 返回更新结果
   */
  const updateAISettings = async (data) => {
    submitting.value = true
    error.value = null

    try {
      const response = await settings.updateAISettings(data)
      aiSettings.value = response

      toast.add({
        severity: 'success',
        summary: '更新成功',
        detail: 'AI设置已更新',
        life: 3000
      })

      return { success: true, settings: response }
    } catch (err) {
      error.value = err.response?.data?.message || '更新AI设置失败'

      toast.add({
        severity: 'error',
        summary: '更新失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 获取所有设置
   * @returns {Promise<Object>} - 返回所有设置
   */
  const getAllSettings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await settings.getAllSettings()

      systemSettings.value = response.system
      securitySettings.value = response.security
      emailSettings.value = response.email
      storageSettings.value = response.storage
      aiSettings.value = response.ai

      return response
    } catch (err) {
      error.value = err.response?.data?.message || '获取所有设置失败'

      toast.add({
        severity: 'error',
        summary: '获取设置失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 备份系统设置
   * @returns {Promise<Blob>} - 返回备份文件
   */
  const backupSettings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await settings.backupSettings()

      // 创建下载链接
      const url = window.URL.createObjectURL(response)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `settings-backup-${new Date().toISOString().split('T')[0]}.json`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      toast.add({
        severity: 'success',
        summary: '备份成功',
        detail: '系统设置已备份',
        life: 3000
      })

      return response
    } catch (err) {
      error.value = err.response?.data?.message || '备份系统设置失败'

      toast.add({
        severity: 'error',
        summary: '备份失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 恢复系统设置
   * @param {File} file - 备份文件
   * @returns {Promise<Object>} - 返回恢复结果
   */
  const restoreSettings = async (file) => {
    submitting.value = true
    error.value = null

    try {
      // 确认恢复操作
      return new Promise((resolve) => {
        confirm.require({
          message: '确定要恢复系统设置吗？当前设置将被覆盖。',
          header: '确认恢复',
          icon: 'pi pi-exclamation-triangle',
          acceptClass: 'p-button-warning',
          accept: async () => {
            try {
              const formData = new FormData()
              formData.append('file', file)

              const response = await settings.restoreSettings(formData)

              toast.add({
                severity: 'success',
                summary: '恢复成功',
                detail: '系统设置已恢复',
                life: 3000
              })

              // 重新加载所有设置
              await getAllSettings()

              resolve({ success: true })
            } catch (err) {
              error.value = err.response?.data?.message || '恢复系统设置失败'

              toast.add({
                severity: 'error',
                summary: '恢复失败',
                detail: error.value,
                life: 5000
              })

              resolve({ success: false, error: error.value })
            } finally {
              submitting.value = false
            }
          },
          reject: () => {
            submitting.value = false
            resolve({ success: false, cancelled: true })
          }
        })
      })
    } catch (err) {
      submitting.value = false
      error.value = err.message || '恢复系统设置失败'

      toast.add({
        severity: 'error',
        summary: '恢复失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    }
  }

  return {
    systemSettings,
    securitySettings,
    emailSettings,
    storageSettings,
    aiSettings,
    loading,
    submitting,
    error,
    getSystemSettings,
    updateSystemSettings,
    getSecuritySettings,
    updateSecuritySettings,
    getEmailSettings,
    updateEmailSettings,
    sendTestEmail,
    getStorageSettings,
    updateStorageSettings,
    getAISettings,
    updateAISettings,
    getAllSettings,
    backupSettings,
    restoreSettings
  }
}
