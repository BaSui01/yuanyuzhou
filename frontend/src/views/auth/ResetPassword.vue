<template>
  <article class="reset-password-container">
    <header class="auth-header">
      <img src="@/assets/img/logo.svg" alt="元宇宙" class="logo" />
      <h1 class="app-name">元宇宙</h1>
    </header>

    <section class="auth-content">
      <h2>重置密码</h2>
      <p class="description">请为您的账户设置新密码</p>

      <!-- 错误提示 -->
      <div v-if="linkExpired" class="error-message-box">
        <i class="pi pi-exclamation-triangle"></i>
        <div>
          <strong>链接已过期</strong>
          <p>重置密码链接已过期或无效，请重新申请密码重置。</p>
        </div>
      </div>

      <!-- 成功提示 -->
      <div v-if="resetSuccess" class="success-message">
        <i class="pi pi-check-circle"></i>
        <div>
          <strong>密码重置成功</strong>
          <p>您的密码已成功重置，即将跳转到登录页面...</p>
        </div>
      </div>

      <form v-if="!linkExpired && !resetSuccess" @submit.prevent="handleSubmit" class="auth-form"
        :class="{ 'form-loading': loading }">
        <!-- 新密码输入 -->
        <fieldset class="form-field">
          <label for="password">新密码</label>
          <Password id="password" v-model="password" placeholder="请输入新密码 (至少8个字符)" required toggleMask
            :promptLabel="passwordPrompts.prompt" :weakLabel="passwordPrompts.weak"
            :mediumLabel="passwordPrompts.medium" :strongLabel="passwordPrompts.strong" :disabled="loading"
            class="password-field-direct" @input="validatePassword" />
          <small v-if="errors.password" class="error-message">{{ errors.password }}</small>
        </fieldset>

        <!-- 确认新密码输入 -->
        <fieldset class="form-field">
          <label for="confirmPassword">确认新密码</label>
          <Password id="confirmPassword" v-model="confirmPassword" placeholder="请再次输入新密码" required toggleMask
            :feedback="false" :disabled="loading" class="password-field-direct" @blur="validateConfirmPassword" />
          <small v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</small>
        </fieldset>

        <!-- 密码要求提示 -->
        <div class="password-requirements">
          <h4>密码要求：</h4>
          <ul>
            <li :class="{ valid: passwordChecks.length }">
              <i :class="passwordChecks.length ? 'pi pi-check' : 'pi pi-times'"></i>
              至少8个字符
            </li>
            <li :class="{ valid: passwordChecks.uppercase }">
              <i :class="passwordChecks.uppercase ? 'pi pi-check' : 'pi pi-times'"></i>
              包含大写字母
            </li>
            <li :class="{ valid: passwordChecks.lowercase }">
              <i :class="passwordChecks.lowercase ? 'pi pi-check' : 'pi pi-times'"></i>
              包含小写字母
            </li>
            <li :class="{ valid: passwordChecks.number }">
              <i :class="passwordChecks.number ? 'pi pi-check' : 'pi pi-times'"></i>
              包含数字
            </li>
          </ul>
        </div>

        <!-- 重置按钮 -->
        <Button type="submit" label="重置密码" class="submit-btn" :loading="loading" :disabled="isFormInvalid"
          icon="pi pi-refresh" iconPos="right" />
      </form>

      <footer class="auth-footer">
        <router-link to="/auth/login" class="back-link">
          <i class="pi pi-arrow-left"></i>
          返回登录
        </router-link>
        <span v-if="!linkExpired" class="separator">|</span>
        <router-link v-if="linkExpired" to="/auth/forgot-password" class="forgot-link">
          重新申请重置
        </router-link>
      </footer>
    </section>
  </article>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import Button from 'primevue/button'
import Password from 'primevue/password'

// 响应式数据
const route = useRoute()
const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

const token = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const linkExpired = ref(false)
const resetSuccess = ref(false)

const errors = reactive({
  password: '',
  confirmPassword: ''
})

// 密码强度提示文本
const passwordPrompts = {
  prompt: '请输入密码',
  weak: '密码强度：弱',
  medium: '密码强度：中等',
  strong: '密码强度：强'
}

// 密码检查状态
const passwordChecks = reactive({
  length: false,
  uppercase: false,
  lowercase: false,
  number: false
})

// 计算属性
const isFormInvalid = computed(() => {
  return !password.value ||
    !confirmPassword.value ||
    !Object.values(passwordChecks).every(check => check) ||
    Object.values(errors).some(error => error !== '')
})

// 密码验证
const validatePassword = () => {
  errors.password = ''

  // 更新密码检查状态
  passwordChecks.length = password.value.length >= 8
  passwordChecks.uppercase = /[A-Z]/.test(password.value)
  passwordChecks.lowercase = /[a-z]/.test(password.value)
  passwordChecks.number = /\d/.test(password.value)

  if (!password.value) {
    errors.password = '请输入新密码'
  } else if (password.value.length < 8) {
    errors.password = '密码至少需要8个字符'
  } else if (password.value.length > 50) {
    errors.password = '密码不能超过50个字符'
  } else if (!Object.values(passwordChecks).every(check => check)) {
    errors.password = '密码不符合安全要求'
  }

  // 如果确认密码已输入，重新验证
  if (confirmPassword.value) {
    validateConfirmPassword()
  }
}

const validateConfirmPassword = () => {
  errors.confirmPassword = ''

  if (!confirmPassword.value) {
    errors.confirmPassword = '请确认新密码'
  } else if (password.value !== confirmPassword.value) {
    errors.confirmPassword = '两次输入的密码不一致'
  }
}

// 表单验证
const validateForm = () => {
  validatePassword()
  validateConfirmPassword()

  return Object.values(errors).every(error => error === '') &&
    Object.values(passwordChecks).every(check => check)
}

// 处理表单提交
const handleSubmit = async () => {
  if (!validateForm() || loading.value) return

  try {
    loading.value = true

    await authStore.resetPassword({
      email: email.value,
      token: token.value,
      password: password.value,
      password_confirmation: confirmPassword.value
    })

    resetSuccess.value = true

    toast.add({
      severity: 'success',
      summary: '密码重置成功',
      detail: '您的密码已成功重置，请使用新密码登录',
      life: 6000
    })

    // 延迟跳转到登录页面
    setTimeout(() => {
      router.push('/auth/login')
    }, 3000)

  } catch (error) {
    console.error('重置密码失败:', error)

    if (error.status === 422) {
      // 处理表单验证错误
      const serverErrors = error.data?.errors || {}
      Object.keys(serverErrors).forEach(key => {
        if (errors.hasOwnProperty(key)) {
          errors[key] = serverErrors[key][0]
        }
      })
    } else if (error.status === 401 || error.status === 403) {
      linkExpired.value = true
      toast.add({
        severity: 'error',
        summary: '链接已过期',
        detail: '重置密码链接已过期或无效，请重新申请',
        life: 6000
      })
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
        summary: '重置失败',
        detail: error.message || '服务器错误，请稍后再试',
        life: 5000
      })
    }
  } finally {
    loading.value = false
  }
}

// 监听密码变化，实时更新检查状态
watch(password, (newPassword) => {
  if (newPassword) {
    passwordChecks.length = newPassword.length >= 8
    passwordChecks.uppercase = /[A-Z]/.test(newPassword)
    passwordChecks.lowercase = /[a-z]/.test(newPassword)
    passwordChecks.number = /\d/.test(newPassword)
  } else {
    Object.keys(passwordChecks).forEach(key => {
      passwordChecks[key] = false
    })
  }
})

// 组件挂载时的初始化
onMounted(() => {
  // 从URL参数中获取token和email
  token.value = route.query.token || ''
  email.value = route.query.email || ''

  // 验证必要参数
  if (!token.value || !email.value) {
    linkExpired.value = true
    toast.add({
      severity: 'error',
      summary: '无效链接',
      detail: '重置密码链接无效或已过期',
      life: 5000
    })
    return
  }

  // 聚焦到密码输入框
  setTimeout(() => {
    const passwordInput = document.getElementById('password')
    if (passwordInput) {
      passwordInput.focus()
    }
  }, 100)
})
</script>

<style lang="scss">
@use '@/assets/styles/view/auth/auth.scss';

// 重置密码页面特定样式
.reset-password-container {

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

  .error-message-box {
    background: linear-gradient(135deg, #fef2f2, #fee2e2);
    border: 2px solid #fca5a5;
    color: var(--red-700);
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    animation: slideInUp 0.4s ease;

    .pi {
      font-size: 1.5rem;
      margin-top: 0.125rem;
      color: var(--red-600);
    }

    div {
      flex: 1;

      strong {
        display: block;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        color: var(--red-700);
      }

      p {
        margin: 0;
        font-size: 0.875rem;
        line-height: 1.5;
        color: #991b1b;
      }
    }
  }

  .password-requirements {
    background: var(--gray-50);
    border: 2px solid var(--gray-200);
    border-radius: 0.75rem;
    padding: 1.25rem;
    margin: 1rem 0;

    h4 {
      margin: 0 0 0.75rem 0;
      font-size: 0.875rem;
      font-weight: 600;
      color: var(--gray-700);
    }

    ul {
      margin: 0;
      padding: 0;
      list-style: none;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 0.5rem;
    }

    li {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.875rem;
      color: var(--gray-600);
      transition: color 0.2s ease;

      i {
        font-size: 0.75rem;
        width: 1rem;
        text-align: center;
        color: var(--gray-400);
        transition: color 0.2s ease;
      }

      &.valid {
        color: var(--green-700);

        i {
          color: var(--green-600);
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
    .forgot-link {
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

  // 响应式调整
  @media (max-width: 640px) {
    .password-requirements {
      ul {
        grid-template-columns: 1fr;
        gap: 0.75rem;
      }

      li {
        font-size: 0.8125rem;
      }
    }

    .auth-footer {
      flex-direction: column;
      gap: 0.75rem;

      .separator {
        display: none;
      }
    }

    .error-message-box {
      padding: 1.25rem;

      .pi {
        font-size: 1.25rem;
      }

      div {
        strong {
          font-size: 0.9375rem;
        }

        p {
          font-size: 0.8125rem;
        }
      }
    }
  }
}
</style>
