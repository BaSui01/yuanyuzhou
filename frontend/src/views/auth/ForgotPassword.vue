<template>
  <article class="forgot-password-container">
    <header class="auth-header">
      <img src="@/assets/img/logo.svg" alt="元宇宙" class="logo" />
      <h1 class="app-name">元宇宙</h1>
    </header>

    <section class="auth-content">
      <h2>找回密码</h2>
      <p class="description">请输入您的邮箱地址，我们将发送重置密码的链接到您的邮箱</p>

      <!-- 成功提示 -->
      <div v-if="emailSent" class="success-message">
        <i class="pi pi-check-circle"></i>
        <div>
          <strong>邮件已发送</strong>
          <p>请查看您的邮箱 <strong>{{ email }}</strong>，按照邮件中的指引重置密码。如果没有收到邮件，请检查垃圾邮件文件夹。</p>
        </div>
      </div>

      <form v-if="!emailSent" @submit.prevent="handleSubmit" class="auth-form" :class="{ 'form-loading': loading }">
        <!-- 邮箱输入 -->
        <fieldset class="form-field">
          <label for="email">邮箱地址</label>
          <div class="input-group">
            <i class="pi pi-envelope" aria-hidden="true"></i>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="请输入您的邮箱地址"
              required
              autocomplete="email"
              class="form-input"
              :disabled="loading"
              @blur="validateEmail"
            />
          </div>
          <small v-if="errors.email" class="error-message">{{ errors.email }}</small>
        </fieldset>

        <!-- 验证码输入 -->
        <fieldset class="form-field captcha-field">
          <label for="captcha">安全验证</label>
          <div class="captcha-group">
            <div class="input-group captcha-input">
              <i class="pi pi-shield" aria-hidden="true"></i>
              <input
                id="captcha"
                v-model="captcha"
                type="text"
                placeholder="请输入验证码"
                required
                maxlength="6"
                class="form-input"
                :disabled="loading"
              />
            </div>
            <img
              v-if="captchaUrl"
              :src="captchaUrl"
              alt="验证码图片，点击刷新"
              class="captcha-image"
              @click="refreshCaptcha"
              :style="{ opacity: loading ? 0.6 : 1 }"
            />
            <div v-else class="captcha-placeholder" @click="refreshCaptcha">
              <i class="pi pi-refresh"></i>
              <span>点击获取验证码</span>
            </div>
          </div>
          <small v-if="errors.captcha" class="error-message">{{ errors.captcha }}</small>
        </fieldset>

        <!-- 提交按钮 -->
        <Button
          type="submit"
          label="发送重置链接"
          class="submit-btn"
          :loading="loading"
          :disabled="isFormInvalid"
          icon="pi pi-send"
          iconPos="right"
        />
      </form>

      <!-- 重新发送或返回操作 -->
      <div v-if="emailSent" class="resend-actions">
        <Button
          :label="resendCooldown > 0 ? `${resendCooldown}秒后可重发` : '重新发送邮件'"
          severity="secondary"
          text
          @click="resendEmail"
          :loading="resending"
          :disabled="resendCooldown > 0"
          class="resend-button"
        />
      </div>

      <footer class="auth-footer">
        <router-link to="/auth/login" class="back-link">
          <i class="pi pi-arrow-left"></i>
          返回登录
        </router-link>
        <span class="separator">|</span>
        <router-link to="/auth/register" class="register-link">
          还没有账号？注册
        </router-link>
      </footer>
    </section>
  </article>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import Button from 'primevue/button'

// 响应式数据
const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

const email = ref('')
const captcha = ref('')
const loading = ref(false)
const resending = ref(false)
const emailSent = ref(false)
const captchaUrl = ref('')
const resendCooldown = ref(0)

const errors = reactive({
  email: '',
  captcha: ''
})

let cooldownTimer = null

// 计算属性
const isFormInvalid = computed(() => {
  return !email.value || !captcha.value || Object.values(errors).some(error => error !== '')
})

// 验证邮箱
const validateEmail = () => {
  errors.email = ''

  if (!email.value) {
    errors.email = '请输入邮箱地址'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.email = '请输入有效的邮箱地址'
  }
}

// 刷新验证码
const refreshCaptcha = () => {
  if (loading.value || resending.value) return

  const timestamp = new Date().getTime()
  captchaUrl.value = `/api/v1/auth/captcha?t=${timestamp}`
  captcha.value = ''
  errors.captcha = ''
}

// 开始倒计时
const startCooldown = (seconds = 60) => {
  resendCooldown.value = seconds

  cooldownTimer = setInterval(() => {
    resendCooldown.value--

    if (resendCooldown.value <= 0) {
      clearInterval(cooldownTimer)
      cooldownTimer = null
    }
  }, 1000)
}

// 发送重置邮件
const sendResetEmail = async () => {
  validateEmail()

  if (!captcha.value.trim()) {
    errors.captcha = '请输入验证码'
    return false
  } else {
    errors.captcha = ''
  }

  if (Object.values(errors).some(error => error !== '')) {
    return false
  }

  try {
    await authStore.forgotPassword({
      email: email.value.trim(),
      captcha: captcha.value.trim()
    })

    return true
  } catch (error) {
    console.error('发送重置邮件失败:', error)

    if (error.status === 422) {
      const serverErrors = error.data?.errors || {}
      if (serverErrors.email) {
        errors.email = serverErrors.email[0]
      }
      if (serverErrors.captcha) {
        errors.captcha = serverErrors.captcha[0]
      }
    } else if (error.status === 404) {
      errors.email = '该邮箱地址未注册'
    } else if (error.status === 429) {
      toast.add({
        severity: 'warn',
        summary: '请求过于频繁',
        detail: '请稍后再试',
        life: 5000
      })
    } else {
      toast.add({
        severity: 'error',
        summary: '发送失败',
        detail: error.message || '服务器错误，请稍后再试',
        life: 5000
      })
    }

    refreshCaptcha()
    return false
  }
}

// 处理表单提交
const handleSubmit = async () => {
  if (isFormInvalid.value || loading.value) return

  loading.value = true

  try {
    const success = await sendResetEmail()

    if (success) {
      emailSent.value = true
      startCooldown(60)

      toast.add({
        severity: 'success',
        summary: '邮件已发送',
        detail: '请查看您的邮箱，按照邮件中的指引重置密码',
        life: 6000
      })
    }
  } finally {
    loading.value = false
  }
}

// 重新发送邮件
const resendEmail = async () => {
  if (resending.value || resendCooldown.value > 0) return

  resending.value = true

  try {
    const success = await sendResetEmail()

    if (success) {
      startCooldown(60)

      toast.add({
        severity: 'success',
        summary: '邮件已重新发送',
        detail: '请查看您的邮箱',
        life: 4000
      })
    }
  } finally {
    resending.value = false
  }
}

// 组件挂载时的初始化
onMounted(() => {
  refreshCaptcha()

  // 聚焦到邮箱输入框
  setTimeout(() => {
    const emailInput = document.getElementById('email')
    if (emailInput) {
      emailInput.focus()
    }
  }, 100)
})

// 组件卸载时清理定时器
onUnmounted(() => {
  if (cooldownTimer) {
    clearInterval(cooldownTimer)
  }
})
</script>

<style lang="scss">
@use '@/assets/styles/view/auth/auth.scss';

// 忘记密码页面特定样式
.forgot-password-container {
  .resend-actions {
    text-align: center;
    margin: 2rem 0;

    .resend-button {
      :deep(.p-button) {
        color: var(--primary-600);
        font-weight: 600;

        &:hover:not(:disabled) {
          background: var(--primary-50);
          color: var(--primary-700);
        }

        &:disabled {
          opacity: 0.6;
          color: var(--gray-400);
        }
      }
    }
  }

  .auth-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    text-align: center;
    margin-top: 2rem;
    font-size: 0.875rem;
    color: var(--gray-600);
    font-weight: 500;

    .separator {
      color: var(--gray-300);
    }

    .back-link,
    .register-link {
      color: var(--primary-600);
      text-decoration: none;
      font-weight: 600;
      transition: color 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.375rem;

      &:hover {
        color: var(--primary-700);
      }

      i {
        font-size: 0.8125rem;
      }
    }

    .back-link {
      color: var(--gray-500);

      &:hover {
        color: var(--primary-600);
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

  // 响应式调整
  @media (max-width: 640px) {
    .captcha-field .captcha-group {
      .captcha-placeholder {
        width: 100%;
        height: 3rem;
      }
    }

    .auth-footer {
      flex-direction: column;
      gap: 0.75rem;

      .separator {
        display: none;
      }
    }
  }
}
</style>
