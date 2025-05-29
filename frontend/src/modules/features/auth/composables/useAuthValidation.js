import { ref, computed } from 'vue'

/**
 * 认证表单验证 Composable
 * 提供登录、注册、密码重置等表单验证功能
 */
export function useAuthValidation() {
  // 邮箱验证正则
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  // 密码强度验证正则（至少8位，包含字母和数字）
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$/

  // 用户名验证正则（3-20位，字母数字下划线）
  const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/

  /**
   * 验证邮箱
   * @param {string} email - 邮箱地址
   * @returns {Object} 验证结果
   */
  const validateEmail = (email) => {
    if (!email) {
      return { valid: false, message: '邮箱不能为空' }
    }

    if (!emailRegex.test(email)) {
      return { valid: false, message: '请输入有效的邮箱地址' }
    }

    return { valid: true, message: '' }
  }

  /**
   * 验证密码
   * @param {string} password - 密码
   * @returns {Object} 验证结果
   */
  const validatePassword = (password) => {
    if (!password) {
      return { valid: false, message: '密码不能为空' }
    }

    if (password.length < 8) {
      return { valid: false, message: '密码至少需要8位字符' }
    }

    if (!passwordRegex.test(password)) {
      return { valid: false, message: '密码必须包含字母和数字' }
    }

    return { valid: true, message: '' }
  }

  /**
   * 验证密码确认
   * @param {string} password - 原密码
   * @param {string} confirmPassword - 确认密码
   * @returns {Object} 验证结果
   */
  const validatePasswordConfirm = (password, confirmPassword) => {
    if (!confirmPassword) {
      return { valid: false, message: '请确认密码' }
    }

    if (password !== confirmPassword) {
      return { valid: false, message: '两次密码输入不一致' }
    }

    return { valid: true, message: '' }
  }

  /**
   * 验证用户名
   * @param {string} username - 用户名
   * @returns {Object} 验证结果
   */
  const validateUsername = (username) => {
    if (!username) {
      return { valid: false, message: '用户名不能为空' }
    }

    if (username.length < 3) {
      return { valid: false, message: '用户名至少需要3位字符' }
    }

    if (username.length > 20) {
      return { valid: false, message: '用户名不能超过20位字符' }
    }

    if (!usernameRegex.test(username)) {
      return { valid: false, message: '用户名只能包含字母、数字和下划线' }
    }

    return { valid: true, message: '' }
  }

  /**
   * 验证验证码
   * @param {string} captcha - 验证码
   * @returns {Object} 验证结果
   */
  const validateCaptcha = (captcha) => {
    if (!captcha) {
      return { valid: false, message: '验证码不能为空' }
    }

    if (captcha.length < 4) {
      return { valid: false, message: '请输入完整的验证码' }
    }

    return { valid: true, message: '' }
  }

  /**
   * 验证登录表单
   * @param {Object} formData - 表单数据
   * @returns {Object} 验证结果
   */
  const validateLoginForm = (formData) => {
    const errors = {}

    const emailValidation = validateEmail(formData.email)
    if (!emailValidation.valid) {
      errors.email = emailValidation.message
    }

    const passwordValidation = validatePassword(formData.password)
    if (!passwordValidation.valid) {
      errors.password = passwordValidation.message
    }

    const captchaValidation = validateCaptcha(formData.captcha)
    if (!captchaValidation.valid) {
      errors.captcha = captchaValidation.message
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors
    }
  }

  /**
   * 验证注册表单
   * @param {Object} formData - 表单数据
   * @returns {Object} 验证结果
   */
  const validateRegisterForm = (formData) => {
    const errors = {}

    const usernameValidation = validateUsername(formData.username)
    if (!usernameValidation.valid) {
      errors.username = usernameValidation.message
    }

    const emailValidation = validateEmail(formData.email)
    if (!emailValidation.valid) {
      errors.email = emailValidation.message
    }

    const passwordValidation = validatePassword(formData.password)
    if (!passwordValidation.valid) {
      errors.password = passwordValidation.message
    }

    const confirmPasswordValidation = validatePasswordConfirm(formData.password, formData.confirmPassword)
    if (!confirmPasswordValidation.valid) {
      errors.confirmPassword = confirmPasswordValidation.message
    }

    const captchaValidation = validateCaptcha(formData.captcha)
    if (!captchaValidation.valid) {
      errors.captcha = captchaValidation.message
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors
    }
  }

  /**
   * 验证忘记密码表单
   * @param {Object} formData - 表单数据
   * @returns {Object} 验证结果
   */
  const validateForgotPasswordForm = (formData) => {
    const errors = {}

    const emailValidation = validateEmail(formData.email)
    if (!emailValidation.valid) {
      errors.email = emailValidation.message
    }

    const captchaValidation = validateCaptcha(formData.captcha)
    if (!captchaValidation.valid) {
      errors.captcha = captchaValidation.message
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors
    }
  }

  /**
   * 验证重置密码表单
   * @param {Object} formData - 表单数据
   * @returns {Object} 验证结果
   */
  const validateResetPasswordForm = (formData) => {
    const errors = {}

    const passwordValidation = validatePassword(formData.password)
    if (!passwordValidation.valid) {
      errors.password = passwordValidation.message
    }

    const confirmPasswordValidation = validatePasswordConfirm(formData.password, formData.confirmPassword)
    if (!confirmPasswordValidation.valid) {
      errors.confirmPassword = confirmPasswordValidation.message
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors
    }
  }

  /**
   * 获取密码强度
   * @param {string} password - 密码
   * @returns {Object} 密码强度信息
   */
  const getPasswordStrength = (password) => {
    if (!password) {
      return { level: 0, text: '请输入密码', color: 'gray' }
    }

    let score = 0
    const checks = {
      length: password.length >= 8,
      lowercase: /[a-z]/.test(password),
      uppercase: /[A-Z]/.test(password),
      numbers: /\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    }

    // 计算得分
    if (checks.length) score++
    if (checks.lowercase) score++
    if (checks.uppercase) score++
    if (checks.numbers) score++
    if (checks.special) score++

    // 额外长度奖励
    if (password.length >= 12) score++

    if (score <= 2) {
      return { level: 1, text: '弱', color: 'red' }
    } else if (score <= 4) {
      return { level: 2, text: '中', color: 'orange' }
    } else {
      return { level: 3, text: '强', color: 'green' }
    }
  }

  return {
    validateEmail,
    validatePassword,
    validatePasswordConfirm,
    validateUsername,
    validateCaptcha,
    validateLoginForm,
    validateRegisterForm,
    validateForgotPasswordForm,
    validateResetPasswordForm,
    getPasswordStrength
  }
}
