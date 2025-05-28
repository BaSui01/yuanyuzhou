<template>
  <div class="forgot-password-view">
    <div class="mb-8 text-center">
      <h2 class="text-2xl font-bold text-white">找回密码</h2>
      <p class="text-gray-400 mt-2">输入您的邮箱地址，我们将发送重置密码链接</p>
    </div>

    <!-- 状态信息 -->
    <div v-if="successMessage" class="bg-green-500/20 border border-green-500/30 text-green-400 px-4 py-3 rounded-lg text-sm mb-6">
      {{ successMessage }}
    </div>

    <div v-if="errorMessage" class="bg-red-500/20 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg text-sm mb-6">
      {{ errorMessage }}
    </div>

    <!-- 重置密码表单 -->
    <form v-if="!successMessage" @submit.prevent="handleForgotPassword" class="space-y-6">
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

      <!-- 提交按钮 -->
      <Button
        type="submit"
        label="发送重置链接"
        icon="pi pi-envelope"
        class="w-full"
        :loading="loading"
      />

      <!-- 返回登录 -->
      <div class="text-center mt-6">
        <router-link to="/auth/login" class="text-cyan-400 hover:text-cyan-300">
          <i class="pi pi-arrow-left mr-1"></i>
          返回登录
        </router-link>
      </div>
    </form>

    <!-- 成功后显示 -->
    <div v-else class="mt-6">
      <Button
        label="返回登录"
        icon="pi pi-arrow-left"
        class="w-full"
        @click="$router.push('/auth/login')"
      />
    </div>
  </div>
</template>

<script>
import { ForgotPasswordModule } from '@/server/view/auth/auth';

export default {
  name: 'ForgotPasswordView',
  ...ForgotPasswordModule
};
</script>

<style lang="scss" scoped>
@use'../../styles/view/auth/auth.scss';
</style>
