<template>
  <div class="forgot-password-container">
    <div class="forgot-password-card">
      <div class="logo-container">
        <img src="@/assets/img/logo.svg" alt="元宇宙" class="logo" />
        <h1 class="app-name">元宇宙</h1>
      </div>

      <h2 class="forgot-password-title">找回密码</h2>
      <p class="description">请输入您的邮箱，我们将发送重置密码链接</p>

      <form @submit.prevent="handleSubmit" class="forgot-password-form">
        <div class="form-group">
          <label for="email">邮箱</label>
          <div class="input-wrapper">
            <i class="pi pi-envelope"></i>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="请输入邮箱"
              required
              class="form-input"
            />
          </div>
          <small v-if="error" class="error-text">{{ error }}</small>
        </div>

        <div class="form-group captcha-group">
          <label for="captcha">验证码</label>
          <div class="captcha-wrapper">
            <div class="input-wrapper captcha-input-wrapper">
              <i class="pi pi-shield"></i>
              <input
                id="captcha"
                v-model="captcha"
                type="text"
                placeholder="请输入验证码"
                required
                class="form-input"
              />
            </div>
            <img :src="captchaUrl" alt="验证码" class="captcha-image" @click="refreshCaptcha" />
          </div>
        </div>

        <Button
          type="submit"
          label="发送重置链接"
          class="submit-button"
          :loading="loading"
        />
      </form>

      <div class="form-footer">
        <router-link to="/auth/login" class="back-link">
          <i class="pi pi-arrow-left"></i> 返回登录
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ForgotPasswordView',

  setup() {
    const router = useRouter()
    const toast = useToast()
    const authStore = useAuthStore()

    const email = ref('')
    const captcha = ref('')
    const loading = ref(false)
    const error = ref('')
    const captchaUrl = ref('/api/v1/auth/captcha')

    const refreshCaptcha = () => {
      captchaUrl.value = `/api/v1/auth/captcha?t=${new Date().getTime()}`
    }

    const handleSubmit = async () => {
      if (!email.value) {
        error.value = '请输入邮箱地址'
        return
      }

      if (!captcha.value) {
        error.value = '请输入验证码'
        return
      }

      try {
        loading.value = true
        error.value = ''

        await authStore.forgotPassword({
          email: email.value,
          captcha: captcha.value
        })

        toast.add({
          severity: 'success',
          summary: '邮件已发送',
          detail: '请查看您的邮箱，按照邮件中的指引重置密码',
          life: 5000
        })

        // 重置表单
        email.value = ''
        captcha.value = ''
        refreshCaptcha()

      } catch (err) {
        console.error('找回密码失败:', err)

        if (err.status === 422) {
          error.value = '邮箱格式不正确'
        } else if (err.status === 404) {
          error.value = '该邮箱未注册'
        } else if (err.status === 429) {
          error.value = '请求过于频繁，请稍后再试'
        } else {
          error.value = err.message || '服务器错误，请稍后再试'
        }

        refreshCaptcha()
      } finally {
        loading.value = false
      }
    }

    // 初始化验证码
    refreshCaptcha()

    return {
      email,
      captcha,
      loading,
      error,
      captchaUrl,
      refreshCaptcha,
      handleSubmit
    }
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/view/auth/auth.scss';
</style>
