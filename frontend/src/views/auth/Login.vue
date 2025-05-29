<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-container">
        <img src="@/assets/img/logo.svg" alt="元宇宙" class="logo" />
        <h1 class="app-name">元宇宙</h1>
      </div>

      <h2 class="login-title">登录</h2>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">账号</label>
          <div class="input-wrapper">
            <i class="pi pi-user"></i>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="请输入账号"
              required
              class="form-input"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <div class="input-wrapper">
            <i class="pi pi-lock"></i>
            <Password
              id="password"
              v-model="password"
              placeholder="请输入密码"
              :feedback="false"
              toggleMask
              required
              class="form-input password-input"
            />
          </div>
        </div>

        <div class="form-group captcha-group" v-if="showCaptcha">
          <label for="captcha">验证码</label>
          <div class="captcha-wrapper">
            <div class="input-wrapper captcha-input-wrapper">
              <i class="pi pi-shield"></i>
              <input
                id="captcha"
                v-model="captcha"
                type="text"
                placeholder="请输入验证码"
                class="form-input"
              />
            </div>
            <img :src="captchaUrl" alt="验证码" class="captcha-image" @click="refreshCaptcha" />
          </div>
        </div>

        <div class="form-options">
          <div class="remember-me">
            <Checkbox v-model="rememberMe" :binary="true" id="remember-me" />
            <label for="remember-me">记住我</label>
          </div>
          <router-link to="/auth/forgot-password" class="forgot-link">忘记密码?</router-link>
        </div>

        <Button
          type="submit"
          label="登录"
          class="submit-button"
          :loading="loading"
        />
      </form>

      <div class="form-footer">
        还没有账号? <router-link to="/auth/register">立即注册</router-link>
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
  name: 'LoginView',

  setup() {
    const router = useRouter()
    const toast = useToast()
    const authStore = useAuthStore()

    const username = ref('')
    const password = ref('')
    const captcha = ref('')
    const rememberMe = ref(false)
    const loading = ref(false)
    const showCaptcha = ref(false)
    const captchaUrl = ref('/api/v1/auth/captcha')

    const refreshCaptcha = () => {
      captchaUrl.value = `/api/v1/auth/captcha?t=${new Date().getTime()}`
    }

    const handleLogin = async () => {
      if (!username.value || !password.value) {
        toast.add({ severity: 'error', summary: '错误', detail: '请输入账号和密码', life: 3000 })
        return
      }

      if (showCaptcha.value && !captcha.value) {
        toast.add({ severity: 'error', summary: '错误', detail: '请输入验证码', life: 3000 })
        return
      }

      try {
        loading.value = true

        const loginData = {
          username: username.value,
          password: password.value,
          remember_me: rememberMe.value
        }

        if (showCaptcha.value) {
          loginData.captcha = captcha.value
        }

        await authStore.login(loginData)

        toast.add({
          severity: 'success',
          summary: '登录成功',
          detail: '欢迎回来!',
          life: 3000
        })

        // 跳转到首页或之前尝试访问的页面
        const redirectPath = router.currentRoute.value.query.redirect || '/'
        router.push(redirectPath)
      } catch (error) {
        console.error('登录失败:', error)

        // 处理特定错误
        if (error.status === 401) {
          toast.add({
            severity: 'error',
            summary: '登录失败',
            detail: '账号或密码错误',
            life: 3000
          })
        } else if (error.status === 429) {
          // 频率限制，显示验证码
          showCaptcha.value = true
          refreshCaptcha()
          toast.add({
            severity: 'warn',
            summary: '请输入验证码',
            detail: '登录尝试次数过多，请输入验证码',
            life: 3000
          })
        } else {
          toast.add({
            severity: 'error',
            summary: '登录失败',
            detail: error.message || '服务器错误，请稍后再试',
            life: 3000
          })
        }
      } finally {
        loading.value = false
      }
    }

    return {
      username,
      password,
      captcha,
      rememberMe,
      loading,
      showCaptcha,
      captchaUrl,
      refreshCaptcha,
      handleLogin
    }
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/view/auth/auth.scss';
</style>
