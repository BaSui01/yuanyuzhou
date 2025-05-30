<template>
  <article class="register-container">
    <header class="auth-header">
      <img src="@/assets/img/logo.svg" alt="元宇宙" class="logo" />
      <h1 class="app-name">元宇宙</h1>
    </header>

    <section class="auth-content">
      <h2>创建账户</h2>
      <p class="description">加入我们，开启您的元宇宙之旅</p>

      <form @submit.prevent="handleRegister" class="auth-form" :class="{ 'form-loading': loading }">
        <!-- 用户名输入 -->
        <fieldset class="form-field">
          <label for="username">用户名</label>
          <div class="input-group">
            <i class="pi pi-user" aria-hidden="true"></i>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="请输入用户名 (3-20个字符)"
              required
              autocomplete="username"
              class="form-input"
              :disabled="loading"
              @blur="validateUsername"
            />
          </div>
          <small v-if="errors.username" class="error-message">{{ errors.username }}</small>
        </fieldset>

        <!-- 邮箱输入 -->
        <fieldset class="form-field">
          <label for="email">邮箱地址</label>
          <div class="input-group">
            <i class="pi pi-envelope" aria-hidden="true"></i>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="请输入邮箱地址"
              required
              autocomplete="email"
              class="form-input"
              :disabled="loading"
              @blur="validateEmail"
            />
          </div>
          <small v-if="errors.email" class="error-message">{{ errors.email }}</small>
        </fieldset>

        <!-- 密码输入 -->
        <fieldset class="form-field">
          <label for="password">密码</label>
          <Password
            id="password"
            v-model="password"
            placeholder="请输入密码 (至少6个字符)"
            required
            toggleMask
            :promptLabel="passwordPrompts.prompt"
            :weakLabel="passwordPrompts.weak"
            :mediumLabel="passwordPrompts.medium"
            :strongLabel="passwordPrompts.strong"
            :disabled="loading"
            class="password-field-direct"
            @input="validatePassword"
          />
          <small v-if="errors.password" class="error-message">{{ errors.password }}</small>
        </fieldset>

        <!-- 确认密码输入 -->
        <fieldset class="form-field">
          <label for="confirmPassword">确认密码</label>
          <Password
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="请再次输入密码"
            required
            toggleMask
            :feedback="false"
            :disabled="loading"
            class="password-field-direct"
            @blur="validateConfirmPassword"
          />
          <small v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</small>
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

        <!-- 服务条款 -->
        <fieldset class="form-options">
          <div class="terms">
            <Checkbox
              v-model="agreeTerms"
              :binary="true"
              inputId="agree-terms"
              :disabled="loading"
            />
            <label for="agree-terms">
              我已阅读并同意
              <router-link to="/terms" class="terms-link" target="_blank">服务条款</router-link>
              和
              <router-link to="/privacy" class="terms-link" target="_blank">隐私政策</router-link>
            </label>
          </div>
        </fieldset>
        <small v-if="errors.agreeTerms" class="error-message">{{ errors.agreeTerms }}</small>

        <!-- 注册按钮 -->
        <Button
          type="submit"
          label="创建账户"
          class="submit-btn"
          :loading="loading"
          :disabled="isFormInvalid"
          icon="pi pi-user-plus"
          iconPos="right"
        />
      </form>

      <footer class="auth-footer">
        已有账号? <router-link to="/auth/login">立即登录</router-link>
      </footer>
    </section>
  </article>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
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
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const captcha = ref('')
const agreeTerms = ref(false)
const loading = ref(false)
const captchaUrl = ref('')

const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  captcha: '',
  agreeTerms: ''
})

// 密码强度提示文本
const passwordPrompts = {
  prompt: '请输入密码',
  weak: '密码强度：弱',
  medium: '密码强度：中等',
  strong: '密码强度：强'
}

// 计算属性
const isFormInvalid = computed(() => {
  return !username.value ||
         !email.value ||
         !password.value ||
         !confirmPassword.value ||
         !captcha.value ||
         !agreeTerms.value ||
         Object.values(errors).some(error => error !== '')
})

// 验证函数
const validateUsername = () => {
  errors.username = ''

  if (!username.value) {
    errors.username = '请输入用户名'
  } else if (username.value.length < 3) {
    errors.username = '用户名至少需要3个字符'
  } else if (username.value.length > 20) {
    errors.username = '用户名不能超过20个字符'
  } else if (!/^[a-zA-Z0-9_\u4e00-\u9fa5]+$/.test(username.value)) {
    errors.username = '用户名只能包含字母、数字、下划线和中文'
  }
}

const validateEmail = () => {
  errors.email = ''

  if (!email.value) {
    errors.email = '请输入邮箱地址'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.email = '请输入有效的邮箱地址'
  }
}

const validatePassword = () => {
  errors.password = ''

  if (!password.value) {
    errors.password = '请输入密码'
  } else if (password.value.length < 6) {
    errors.password = '密码至少需要6个字符'
  } else if (password.value.length > 50) {
    errors.password = '密码不能超过50个字符'
  }

  // 如果确认密码已输入，重新验证
  if (confirmPassword.value) {
    validateConfirmPassword()
  }
}

const validateConfirmPassword = () => {
  errors.confirmPassword = ''

  if (!confirmPassword.value) {
    errors.confirmPassword = '请确认密码'
  } else if (password.value !== confirmPassword.value) {
    errors.confirmPassword = '两次输入的密码不一致'
  }
}

const clearErrors = () => {
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })
}

// 刷新验证码
const refreshCaptcha = () => {
  if (loading.value) return

  const timestamp = new Date().getTime()
  captchaUrl.value = `/api/v1/auth/captcha?t=${timestamp}`
  captcha.value = ''
  errors.captcha = ''
}

// 表单验证
const validateForm = () => {
  validateUsername()
  validateEmail()
  validatePassword()
  validateConfirmPassword()

  if (!captcha.value) {
    errors.captcha = '请输入验证码'
  } else {
    errors.captcha = ''
  }

  if (!agreeTerms.value) {
    errors.agreeTerms = '请阅读并同意服务条款和隐私政策'
  } else {
    errors.agreeTerms = ''
  }

  return Object.values(errors).every(error => error === '')
}

// 注册处理
const handleRegister = async () => {
  if (!validateForm() || loading.value) return

  try {
    loading.value = true

    const registerData = {
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
      password_confirmation: confirmPassword.value,
      captcha: captcha.value.trim()
    }

    await authStore.register(registerData)

    toast.add({
      severity: 'success',
      summary: '注册成功',
      detail: '账户创建成功！请查看邮箱激活账号后登录',
      life: 6000
    })

    // 清空表单
    username.value = ''
    email.value = ''
    password.value = ''
    confirmPassword.value = ''
    captcha.value = ''
    agreeTerms.value = false
    clearErrors()

    // 延迟跳转到登录页
    setTimeout(() => {
      router.push('/auth/login')
    }, 2000)

  } catch (error) {
    console.error('注册失败:', error)

    if (error.status === 422 && error.data?.errors) {
      // 处理后端返回的表单验证错误
      const serverErrors = error.data.errors
      Object.keys(serverErrors).forEach(key => {
        if (errors.hasOwnProperty(key)) {
          errors[key] = serverErrors[key][0]
        }
      })
    } else if (error.status === 409) {
      // 用户名或邮箱已存在
      toast.add({
        severity: 'error',
        summary: '注册失败',
        detail: '用户名或邮箱已被使用，请选择其他的',
        life: 5000
      })
    } else {
      toast.add({
        severity: 'error',
        summary: '注册失败',
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

// 注册页面特定样式
.register-container {
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

  .form-options {
    margin-bottom: 0.5rem;

    .terms {
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      line-height: 1.5;

      label {
        margin: 0;
        color: var(--gray-600);
        font-size: 0.875rem;
        cursor: pointer;

        .terms-link {
          color: var(--primary-600);
          text-decoration: none;
          font-weight: 600;

          &:hover {
            color: var(--primary-700);
            text-decoration: underline;
          }
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

  // 响应式调整
  @media (max-width: 640px) {
    .captcha-field .captcha-group {
      .captcha-placeholder {
        width: 100%;
        height: 3rem;
      }
    }

    .form-options {
      .terms {
        align-items: flex-start;
        gap: 0.5rem;

        label {
          font-size: 0.8125rem;
        }
      }
    }
  }
}
</style>
