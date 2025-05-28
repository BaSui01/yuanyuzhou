<template>
  <div class="login-view">
    <div class="mb-8 text-center">
      <h2 class="text-2xl font-bold text-white">欢迎回来</h2>
      <p class="text-gray-400 mt-2">登录您的账号以继续访问</p>
    </div>

    <!-- 登录表单 -->
    <form @submit.prevent="handleLogin" class="space-y-6">
      <!-- 错误提示 -->
      <div v-if="errorMessage" class="bg-red-500/20 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg text-sm">
        {{ errorMessage }}
      </div>

      <!-- 邮箱输入 -->
      <div class="form-group">
        <label for="email" class="block text-sm font-medium text-gray-300 mb-2">邮箱地址</label>
        <span class="p-input-icon-left w-full">
          <i class="pi pi-envelope"></i>
          <InputText
            id="email"
            v-model="email"
            type="email"
            class="w-full"
            placeholder="输入您的邮箱"
            :class="{ 'p-invalid': v$.email.$error }"
            @blur="v$.email.$touch()"
          />
        </span>
        <small v-if="v$.email.$error" class="text-red-400">{{ v$.email.$errors[0].$message }}</small>
      </div>

      <!-- 密码输入 -->
      <div class="form-group">
        <div class="flex justify-between items-center mb-2">
          <label for="password" class="block text-sm font-medium text-gray-300">密码</label>
          <router-link to="/auth/forgot-password" class="text-xs text-cyan-400 hover:text-cyan-300">
            忘记密码?
          </router-link>
        </div>
        <span class="p-input-icon-left w-full">
          <i class="pi pi-lock"></i>
          <Password
            id="password"
            v-model="password"
            :feedback="false"
            toggleMask
            class="w-full"
            inputClass="w-full"
            placeholder="输入您的密码"
            :class="{ 'p-invalid': v$.password.$error }"
            @blur="v$.password.$touch()"
          />
        </span>
        <small v-if="v$.password.$error" class="text-red-400">{{ v$.password.$errors[0].$message }}</small>
      </div>

      <!-- 记住我 -->
      <div class="flex items-center">
        <Checkbox v-model="rememberMe" :binary="true" inputId="rememberMe" />
        <label for="rememberMe" class="ml-2 text-sm text-gray-300">记住我</label>
      </div>

      <!-- 提交按钮 -->
      <Button
        type="submit"
        label="登录"
        icon="pi pi-sign-in"
        class="w-full"
        :loading="loading"
      />

      <!-- 社交登录 -->
      <div class="relative my-6">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-700"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-gray-900 text-gray-400">或使用</span>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <Button
          type="button"
          class="p-button-outlined p-button-secondary"
          @click="socialLogin('google')"
        >
          <i class="pi pi-google mr-2"></i>
          Google
        </Button>
        <Button
          type="button"
          class="p-button-outlined p-button-secondary"
          @click="socialLogin('github')"
        >
          <i class="pi pi-github mr-2"></i>
          GitHub
        </Button>
      </div>

      <!-- 注册链接 -->
      <div class="text-center mt-6">
        <span class="text-gray-400">还没有账号?</span>
        <router-link to="/auth/register" class="text-cyan-400 hover:text-cyan-300 ml-1">
          立即注册
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { LoginModule } from '@/server/view/auth/auth';

export default {
  name: 'LoginView',
  ...LoginModule
};
</script>

<style lang="scss" scoped>
@use'../../styles/view/auth/auth.scss';

.login-view {
  :deep(.p-password-input) {
    width: 100%;
  }

  :deep(.p-password-panel) {
    background-color: #1e1e2d;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
  }
}
</style>
