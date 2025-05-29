<template>
  <div class="reset-password-container">
    <div class="reset-password-card">
      <div class="logo-container">
        <img src="@/assets/img/logo.svg" alt="元宇宙" class="logo" />
        <h1 class="app-name">元宇宙</h1>
      </div>

      <h2 class="reset-password-title">重置密码</h2>
      <p class="description">请设置您的新密码</p>

      <form @submit.prevent="handleSubmit" class="reset-password-form">
        <div class="form-group">
          <label for="password">新密码</label>
          <div class="input-wrapper">
            <i class="pi pi-lock"></i>
            <Password
              id="password"
              v-model="password"
              placeholder="请输入新密码"
              required
              toggleMask
              class="form-input password-input"
            />
          </div>
          <small v-if="errors.password" class="error-text">{{ errors.password }}</small>
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认新密码</label>
          <div class="input-wrapper">
            <i class="pi pi-lock"></i>
            <Password
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="请再次输入新密码"
              required
              toggleMask
              :feedback="false"
              class="form-input password-input"
            />
          </div>
          <small v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</small>
        </div>

        <Button
          type="submit"
          label="重置密码"
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
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ResetPasswordView',

  setup() {
    const route = useRoute()
    const router = useRouter()
    const toast = useToast()
    const authStore = useAuthStore()

    const token = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const loading = ref(false)
    const errors = reactive({})

    onMounted(() => {
      // 从URL中获取token和email
      token.value = route.query.token || ''
      email.value = route.query.email || ''

      if (!token.value || !email.value) {
        toast.add({
          severity: 'error',
          summary: '无效链接',
          detail: '重置密码链接无效或已过期',
          life: 5000
        })

        // 重定向到忘记密码页面
        router.push('/auth/forgot-password')
      }
    })

    const validateForm = () => {
      errors.password = ''
      errors.confirmPassword = ''

      let isValid = true

      if (!password.value || password.value.length < 6) {
        errors.password = '密码至少需要6个字符'
        isValid = false
      }

      if (password.value !== confirmPassword.value) {
        errors.confirmPassword = '两次输入的密码不一致'
        isValid = false
      }

      return isValid
    }

    const handleSubmit = async () => {
      if (!validateForm()) {
        return
      }

      try {
        loading.value = true

        await authStore.resetPassword({
          email: email.value,
          token: token.value,
          password: password.value,
          password_confirmation: confirmPassword.value
        })

        toast.add({
          severity: 'success',
          summary: '密码已重置',
          detail: '您的密码已成功重置，请使用新密码登录',
          life: 5000
        })

        // 重定向到登录页面
        router.push('/auth/login')
      } catch (error) {
        console.error('重置密码失败:', error)

        if (error.status === 422) {
          // 处理表单验证错误
          if (error.errors) {
            Object.keys(error.errors).forEach(key => {
              errors[key] = error.errors[key][0]
            })
          }
        } else if (error.status === 401) {
          toast.add({
            severity: 'error',
            summary: '链接已过期',
            detail: '重置密码链接已过期，请重新申请',
            life: 5000
          })
          router.push('/auth/forgot-password')
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

    return {
      password,
      confirmPassword,
      loading,
      errors,
      handleSubmit
    }
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/view/auth/auth.scss';
</style>
