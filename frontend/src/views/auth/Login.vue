<template>
  <article class="login-container">
    <header class="auth-header">
      <img src="@/assets/img/logo.svg" alt="元宇宙" class="logo" />
      <h1 class="app-name">元宇宙</h1>
    </header>

    <section class="auth-content">
      <h2>欢迎回来</h2>
      <p class="description">登录您的账户，开启元宇宙之旅</p>

      <form @submit.prevent="handleLogin" class="auth-form" :class="{ 'form-loading': loading }">
        <!-- 用户名输入 -->
        <fieldset class="form-field">
          <label for="username">用户名</label>
          <div class="input-group">
            <i class="pi pi-user" aria-hidden="true"></i>
            <input id="username" v-model="username" type="text" placeholder="请输入用户名或邮箱" required autocomplete="username"
              class="form-input" :disabled="loading" />
          </div>
        </fieldset>

        <!-- 密码输入 -->
        <fieldset class="form-field">
          <label for="password">密码</label>
          <Password id="password" v-model="password" placeholder="请输入密码" :feedback="false" toggleMask required
            autocomplete="current-password" :disabled="loading" class="password-field-direct" />
        </fieldset>

        <!-- 验证码输入 -->
        <fieldset class="form-field captcha-field">
          <label for="captcha">验证码</label>
          <div class="captcha-group">
            <div class="input-group captcha-input">
              <i class="pi pi-shield" aria-hidden="true"></i>
              <input id="captcha" v-model="captcha" type="text" placeholder="请输入验证码" required maxlength="6"
                class="form-input" :disabled="loading" />
            </div>
            <img v-if="captchaUrl" :src="captchaUrl" alt="验证码图片，点击刷新" class="captcha-image" @click="refreshCaptcha"
              :style="{ opacity: loading ? 0.6 : 1 }" />
            <div v-else class="captcha-placeholder" @click="refreshCaptcha">
              <i class="pi pi-refresh"></i>
              <span>点击获取验证码</span>
            </div>
          </div>
          <small v-if="captchaError" class="error-message">{{ captchaError }}</small>
        </fieldset>

        <!-- 表单选项 -->
        <fieldset class="form-options">
          <div class="remember-option">
            <Checkbox v-model="rememberMe" :binary="true" inputId="remember-me" :disabled="loading" />
            <label for="remember-me">记住我</label>
          </div>
          <router-link to="/auth/forgot-password" class="forgot-link">
            忘记密码?
          </router-link>
        </fieldset>

        <!-- 登录按钮 -->
        <Button type="submit" label="登录" class="submit-btn" :loading="loading" :disabled="isFormInvalid"
          icon="pi pi-sign-in" iconPos="right" />
      </form>

      <!-- 社交登录 -->
      <section class="social-login">
        <p class="social-title">或使用以下方式登录</p>
        <div class="social-buttons">
          <button type="button" class="social-btn github" @click="handleSocialLogin('github')">
            <i class="pi pi-github"></i>
            GitHub
          </button>
          <button type="button" class="social-btn google" @click="handleSocialLogin('google')">
            <i class="pi pi-google"></i>
            Google
          </button>
        </div>
      </section>

      <footer class="auth-footer">
        还没有账号? <router-link to="/auth/register">立即注册</router-link>
      </footer>
    </section>
  </article>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import Button from 'primevue/button'
import Password from 'primevue/password'
import Checkbox from 'primevue/checkbox'

// 响应式数据
const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const captcha = ref('')
const rememberMe = ref(false)
const loading = ref(false)
const captchaError = ref('')
const captchaUrl = ref('')

// 计算属性
const isFormInvalid = computed(() => {
  return !username.value || !password.value || !captcha.value
})

// 刷新验证码
const refreshCaptcha = () => {
  if (loading.value) return

  const timestamp = new Date().getTime()
  captchaUrl.value = `/api/v1/auth/captcha?t=${timestamp}`
  captcha.value = ''
  captchaError.value = ''
}

// 社交登录处理
const handleSocialLogin = (provider) => {
  if (loading.value) return

  toast.add({
    severity: 'info',
    summary: '功能提示',
    detail: `${provider} 登录功能正在开发中`,
    life: 3000
  })
}

// 登录处理
const handleLogin = async () => {
  if (isFormInvalid.value || loading.value) return

  try {
    loading.value = true
    captchaError.value = ''

    const loginData = {
      username: username.value.trim(),
      password: password.value,
      remember_me: rememberMe.value,
      captcha: captcha.value.trim()
    }

    await authStore.login(loginData)

    toast.add({
      severity: 'success',
      summary: '登录成功',
      detail: '欢迎回来！正在跳转...',
      life: 3000
    })

    // 延迟跳转，让用户看到成功消息
    setTimeout(() => {
      const redirectPath = router.currentRoute.value.query.redirect || '/'
      router.push(redirectPath)
    }, 1000)

  } catch (error) {
    console.error('登录失败:', error)

    // 处理不同类型的错误
    if (error.status === 401) {
      toast.add({
        severity: 'error',
        summary: '登录失败',
        detail: '用户名或密码错误',
        life: 5000
      })
    } else if (error.status === 422) {
      // 验证错误
      const errorData = error.data || {}
      if (errorData.captcha) {
        captchaError.value = errorData.captcha[0] || '验证码错误'
        refreshCaptcha()
      } else {
        toast.add({
          severity: 'error',
          summary: '输入错误',
          detail: '请检查您的输入信息',
          life: 3000
        })
      }
    } else if (error.status === 429) {
      // 频率限制
      refreshCaptcha()
      toast.add({
        severity: 'warn',
        summary: '安全验证',
        detail: '登录尝试次数过多，请重新输入验证码',
        life: 5000
      })
    } else if (error.status === 423) {
      // 账户被锁定
      toast.add({
        severity: 'error',
        summary: '账户锁定',
        detail: '您的账户已被暂时锁定，请稍后再试或联系客服',
        life: 8000
      })
    } else {
      toast.add({
        severity: 'error',
        summary: '登录失败',
        detail: error.message || '服务器错误，请稍后再试',
        life: 5000
      })
    }

    // 刷新验证码
    refreshCaptcha()
  } finally {
    loading.value = false
  }
}

// 组件挂载时的初始化
onMounted(() => {
  // 初始化验证码
  refreshCaptcha()

  // 聚焦到用户名输入框
  setTimeout(() => {
    const usernameInput = document.getElementById('username')
    if (usernameInput) {
      usernameInput.focus()
    }
  }, 100)
})
</script>

<style lang="scss">
@use '@/assets/styles/view/auth/auth.scss';

// 登录页面特定样式
.login-container {

  // 直接使用 Password 组件的样式修复
  .password-field-direct {
    :deep(.p-password) {
      width: 100%;
      position: relative;

      // 添加左侧图标
      &::before {
        content: '\e926'; // pi-lock 图标
        font-family: 'primeicons';
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--gray-400);
        font-size: 1.125rem;
        z-index: 3;
        pointer-events: none;
        transition: color 0.2s ease;
      }

      &:focus-within::before {
        color: var(--primary-500);
      }

      .p-password-input {
        width: 100%;
        padding: 0.875rem 3rem 0.875rem 3rem !important;
        border: 2px solid var(--gray-200) !important;
        border-radius: 0.75rem !important;
        font-size: 1rem !important;
        background: var(--gray-50) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        color: var(--gray-900) !important;

        &::placeholder {
          color: var(--gray-400) !important;
        }

        &:focus {
          border-color: var(--primary-500) !important;
          background: white !important;
          box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1), 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
          outline: none !important;
          color: var(--gray-900) !important;
        }

        &:hover:not(:focus) {
          border-color: var(--gray-300) !important;
          background: white !important;
        }

        &:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
      }

      .p-password-toggle-icon {
        color: var(--gray-400);
        right: 1rem;
        z-index: 2;

        &:hover {
          color: var(--primary-500);
        }
      }
    }
  }

  // 验证码占位符样式
  .captcha-placeholder {
    height: 3.375rem;
    min-width: 120px;
    border: 2px dashed var(--gray-300);
    border-radius: 0.75rem;
    cursor: pointer;
    transition: all 0.2s ease;
    background: var(--gray-50);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.25rem;
    color: var(--gray-500);
    font-size: 0.75rem;
    font-weight: 500;

    &:hover {
      border-color: var(--primary-500);
      background: var(--primary-50);
      color: var(--primary-600);
      transform: scale(1.02);
    }

    &:active {
      transform: scale(0.98);
    }

    i {
      font-size: 1rem;
    }
  }

  // 移动端适配
  @media (max-width: 640px) {
    .captcha-field .captcha-group {
      .captcha-placeholder {
        width: 100%;
        height: 3rem;
      }
    }
  }
}
</style>
