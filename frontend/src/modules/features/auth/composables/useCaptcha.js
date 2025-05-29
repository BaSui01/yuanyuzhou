import { ref, onMounted } from 'vue'
import { authAPI } from '../api/authService.js'

/**
 * 验证码处理 Composable
 * 提供验证码获取、刷新等功能
 */
export function useCaptcha() {
  // 状态
  const captchaUrl = ref('')
  const loading = ref(false)

  /**
   * 获取验证码
   */
  const getCaptcha = () => {
    loading.value = true
    try {
      captchaUrl.value = authAPI.getCaptcha()
    } finally {
      loading.value = false
    }
  }

  /**
   * 刷新验证码
   */
  const refreshCaptcha = () => {
    getCaptcha()
  }

  /**
   * 预加载验证码
   */
  const preloadCaptcha = () => {
    getCaptcha()
  }

  // 组件挂载时自动获取验证码
  onMounted(() => {
    preloadCaptcha()
  })

  return {
    captchaUrl,
    loading,
    getCaptcha,
    refreshCaptcha,
    preloadCaptcha
  }
}
