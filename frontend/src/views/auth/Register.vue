<template>
  <div class="register-container">
    <div class="register-card">
      <div class="logo-container">
        <img src="@/assets/img/logo.svg" alt="元宇宙" class="logo" />
        <h1 class="app-name">元宇宙</h1>
      </div>

      <h2 class="register-title">注册账号</h2>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <div class="input-wrapper">
            <i class="pi pi-user"></i>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="请输入用户名"
              required
              class="form-input"
            />
          </div>
          <small v-if="errors.username" class="error-text">{{ errors.username }}</small>
        </div>

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
          <small v-if="errors.email" class="error-text">{{ errors.email }}</small>
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <div class="input-wrapper">
            <i class="pi pi-lock"></i>
            <Password
              id="password"
              v-model="password"
              placeholder="请输入密码"
              required
              toggleMask
              class="form-input password-input"
            />
          </div>
          <small v-if="errors.password" class="error-text">{{ errors.password }}</small>
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <div class="input-wrapper">
            <i class="pi pi-lock"></i>
            <Password
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="请再次输入密码"
              required
              toggleMask
              :feedback="false"
              class="form-input password-input"
            />
          </div>
          <small v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</small>
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
          <small v-if="errors.captcha" class="error-text">{{ errors.captcha }}</small>
        </div>

        <div class="form-options">
          <div class="terms">
            <Checkbox v-model="agreeTerms" :binary="true" id="agree-terms" />
            <label for="agree-terms">
              我已阅读并同意 <router-link to="/terms" class="terms-link">服务条款</router-link> 和
              <router-link to="/privacy" class="terms-link">隐私政策</router-link>
            </label>
          </div>
        </div>
        <small v-if="errors.agreeTerms" class="error-text">{{ errors.agreeTerms }}</small>

        <Button
          type="submit"
          label="注册"
          class="submit-button"
          :loading="loading"
          :disabled="!agreeTerms"
        />
      </form>

      <div class="form-footer">
        已有账号? <router-link to="/auth/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'RegisterView',

  setup() {
    const router = useRouter()
    const toast = useToast()
    const authStore = useAuthStore()

    const username = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const captcha = ref('')
    const agreeTerms = ref(false)
    const loading = ref(false)
    const captchaUrl = ref('/api/v1/auth/captcha')
    const errors = reactive({})

    const refreshCaptcha = () => {
      captchaUrl.value = `/api/v1/auth/captcha?t=${new Date().getTime()}`
    }

    const validateForm = () => {
      errors.username = ''
      errors.email = ''
      errors.password = ''
      errors.confirmPassword = ''
      errors.captcha = ''
      errors.agreeTerms = ''

      let isValid = true

      if (!username.value || username.value.length < 3) {
        errors.username = '用户名至少需要3个字符'
        isValid = false
      }

      if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        errors.email = '请输入有效的邮箱地址'
        isValid = false
      }

      if (!password.value || password.value.length < 6) {
        errors.password = '密码至少需要6个字符'
        isValid = false
      }

      if (password.value !== confirmPassword.value) {
        errors.confirmPassword = '两次输入的密码不一致'
        isValid = false
      }

      if (!captcha.value) {
        errors.captcha = '请输入验证码'
        isValid = false
      }

      if (!agreeTerms.value) {
        errors.agreeTerms = '请阅读并同意服务条款和隐私政策'
        isValid = false
      }

      return isValid
    }

    const handleRegister = async () => {
      if (!validateForm()) {
        return
      }

      try {
        loading.value = true

        await authStore.register({
          username: username.value,
          email: email.value,
          password: password.value,
          password_confirmation: confirmPassword.value,
          captcha: captcha.value
        })

        toast.add({
          severity: 'success',
          summary: '注册成功',
          detail: '请登录您的邮箱激活账号',
          life: 5000
        })

        router.push('/auth/login')
      } catch (error) {
        console.error('注册失败:', error)

        if (error.errors) {
          // 处理后端返回的表单错误
          Object.keys(error.errors).forEach(key => {
            errors[key] = error.errors[key][0]
          })
        } else {
          toast.add({
            severity: 'error',
            summary: '注册失败',
            detail: error.message || '服务器错误，请稍后再试',
            life: 3000
          })
        }

        refreshCaptcha()
      } finally {
        loading.value = false
      }
    }

    // 初始化验证码
    refreshCaptcha()

    return {
      username,
      email,
      password,
      confirmPassword,
      captcha,
      agreeTerms,
      loading,
      captchaUrl,
      errors,
      refreshCaptcha,
      handleRegister
    }
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/view/auth/auth.scss';
</style>
