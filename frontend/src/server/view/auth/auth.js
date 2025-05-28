import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, sameAs, helpers } from '@vuelidate/validators'

// 登录视图逻辑
export const LoginModule = {
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()

    // 表单数据
    const email = ref('')
    const password = ref('')
    const rememberMe = ref(false)
    const errorMessage = ref('')
    const loading = ref(false)

    // 表单验证规则
    const rules = {
      email: { required, email },
      password: { required, minLength: minLength(6) }
    }

    const v$ = useVuelidate(rules, { email, password })

    // 登录处理
    const handleLogin = async () => {
      // 验证表单
      const isValid = await v$.value.$validate()
      if (!isValid) return

      loading.value = true
      errorMessage.value = ''

      try {
        const result = await authStore.login({
          email: email.value,
          password: password.value,
          remember: rememberMe.value
        })

        if (result.success) {
          // 登录成功，重定向
          const redirectPath = route.query.redirect || '/dashboard'
          router.push(redirectPath)
        } else {
          errorMessage.value = result.message || '登录失败，请检查您的凭据'
        }
      } catch (error) {
        errorMessage.value = '登录过程中发生错误，请稍后重试'
        console.error('登录错误:', error)
      } finally {
        loading.value = false
      }
    }

    // 社交登录
    const socialLogin = async (provider) => {
      try {
        // 获取社交登录URL
        const response = await authStore.getSocialLoginUrl(provider)
        if (response.success && response.data.url) {
          window.location.href = response.data.url
        } else {
          errorMessage.value = '无法启动社交登录'
        }
      } catch (error) {
        errorMessage.value = '社交登录过程中发生错误'
        console.error('社交登录错误:', error)
      }
    }

    return {
      email,
      password,
      rememberMe,
      errorMessage,
      loading,
      v$,
      handleLogin,
      socialLogin
    }
  }
}

// 忘记密码视图逻辑
export const ForgotPasswordModule = {
  setup() {
    const authStore = useAuthStore()

    // 表单数据
    const email = ref('')
    const errorMessage = ref('')
    const successMessage = ref('')
    const loading = ref(false)

    // 自定义验证消息
    const requiredMsg = helpers.withMessage('请输入您的邮箱地址', required)
    const emailMsg = helpers.withMessage('请输入有效的电子邮箱地址', email)

    // 表单验证规则
    const rules = {
      email: { required: requiredMsg, email: emailMsg }
    }

    const v$ = useVuelidate(rules, { email })

    // 忘记密码处理
    const handleForgotPassword = async () => {
      // 验证表单
      const isValid = await v$.value.$validate()
      if (!isValid) return

      loading.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        const result = await authStore.forgotPassword(email.value)

        if (result.success) {
          successMessage.value = '重置密码链接已发送到您的邮箱，请查收'
        } else {
          errorMessage.value = result.message || '发送重置密码链接失败，请重试'
        }
      } catch (error) {
        errorMessage.value = '发送重置密码链接过程中发生错误，请稍后重试'
        console.error('忘记密码错误:', error)
      } finally {
        loading.value = false
      }
    }

    return {
      email,
      errorMessage,
      successMessage,
      loading,
      v$,
      handleForgotPassword
    }
  }
}

// 注册视图逻辑
export const RegisterModule = {
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    // 表单数据
    const name = ref('')
    const email = ref('')
    const password = ref('')
    const passwordConfirmation = ref('')
    const agreeTerms = ref(false)
    const errorMessage = ref('')
    const successMessage = ref('')
    const loading = ref(false)

    // 表单验证规则
    const rules = {
      name: {
        required: helpers.withMessage('请输入用户名', required),
        minLength: helpers.withMessage('用户名至少需要3个字符', minLength(3))
      },
      email: {
        required: helpers.withMessage('请输入邮箱地址', required),
        email: helpers.withMessage('请输入有效的邮箱地址', email)
      },
      password: {
        required: helpers.withMessage('请输入密码', required),
        minLength: helpers.withMessage('密码至少需要8个字符', minLength(8))
      },
      passwordConfirmation: {
        required: helpers.withMessage('请确认密码', required),
        sameAsPassword: helpers.withMessage('两次输入的密码不一致', sameAs(password))
      },
      agreeTerms: {
        sameAs: helpers.withMessage('请同意服务条款和隐私政策', sameAs(true))
      }
    }

    const v$ = useVuelidate(rules, { name, email, password, passwordConfirmation, agreeTerms })

    // 注册处理
    const handleRegister = async () => {
      // 验证表单
      const isValid = await v$.value.$validate()
      if (!isValid) return

      loading.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        const result = await authStore.register({
          name: name.value,
          email: email.value,
          password: password.value,
          password_confirmation: passwordConfirmation.value
        })

        if (result.success) {
          successMessage.value = '注册成功，即将跳转到仪表盘'

          // 3秒后跳转到仪表盘
          setTimeout(() => {
            router.push('/dashboard')
          }, 3000)
        } else {
          errorMessage.value = result.message || '注册失败，请重试'
        }
      } catch (error) {
        errorMessage.value = '注册过程中发生错误，请稍后重试'
        console.error('注册错误:', error)
      } finally {
        loading.value = false
      }
    }

    // 社交注册
    const socialRegister = async (provider) => {
      loading.value = true
      errorMessage.value = ''

      try {
        const result = await authStore.getSocialLoginUrl(provider)

        if (result.success && result.data.url) {
          window.location.href = result.data.url
        } else {
          errorMessage.value = result.message || `通过${provider}注册失败，请重试`
        }
      } catch (error) {
        errorMessage.value = '社交注册过程中发生错误，请稍后重试'
        console.error('社交注册错误:', error)
      } finally {
        loading.value = false
      }
    }

    return {
      name,
      email,
      password,
      passwordConfirmation,
      agreeTerms,
      errorMessage,
      successMessage,
      loading,
      v$,
      handleRegister,
      socialRegister
    }
  }
}

// 重置密码视图逻辑
export const ResetPasswordModule = {
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()

    // 表单数据
    const email = ref('')
    const password = ref('')
    const passwordConfirmation = ref('')
    const token = ref('')
    const errorMessage = ref('')
    const successMessage = ref('')
    const loading = ref(false)

    // 表单验证规则
    const rules = {
      email: { required, email },
      password: { required, minLength: minLength(8) },
      passwordConfirmation: {
        required,
        sameAsPassword: sameAs(password)
      }
    }

    const v$ = useVuelidate(rules, { email, password, passwordConfirmation })

    // 重置密码处理
    const handleResetPassword = async () => {
      // 验证表单
      const isValid = await v$.value.$validate()
      if (!isValid) return

      loading.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        const result = await authStore.resetPassword({
          email: email.value,
          token: token.value,
          password: password.value,
          passwordConfirmation: passwordConfirmation.value
        })

        if (result.success) {
          successMessage.value = '密码重置成功，请使用新密码登录'

          // 3秒后跳转到登录页
          setTimeout(() => {
            router.push('/auth/login')
          }, 3000)
        } else {
          errorMessage.value = result.message || '重置密码失败，请重试'
        }
      } catch (error) {
        errorMessage.value = '重置密码过程中发生错误，请稍后重试'
        console.error('重置密码错误:', error)
      } finally {
        loading.value = false
      }
    }

    // 生命周期钩子
    const onMounted = () => {
      // 从URL获取token和email参数
      const urlToken = route.query.token
      const urlEmail = route.query.email

      if (urlToken) {
        token.value = urlToken
      }

      if (urlEmail) {
        email.value = urlEmail
      }
    }

    onMounted()

    return {
      email,
      password,
      passwordConfirmation,
      token,
      errorMessage,
      successMessage,
      loading,
      v$,
      handleResetPassword
    }
  }
}

// 认证布局逻辑
export const AuthLayoutModule = {
  setup() {
    return {}
  }
}

// 默认导出所有模块
export default {
  LoginModule,
  ForgotPasswordModule,
  RegisterModule,
  ResetPasswordModule,
  AuthLayoutModule
}
