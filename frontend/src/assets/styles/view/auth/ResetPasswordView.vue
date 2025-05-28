<template>
  <div class="reset-password-view">
    <div class="mb-8 text-center">
      <h2 class="text-2xl font-bold text-white">重置密码</h2>
      <p class="text-gray-400 mt-2">请设置您的新密码</p>
    </div>

    <!-- 重置密码表单 -->
    <form @submit.prevent="handleResetPassword" class="space-y-6">
      <!-- 成功提示 -->
      <div v-if="successMessage" class="bg-green-500/20 border border-green-500/30 text-green-400 px-4 py-3 rounded-lg text-sm">
        {{ successMessage }}
      </div>

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
            :disabled="!!token"
          />
        </span>
        <small v-if="v$.email.$error" class="text-red-400">{{ v$.email.$errors[0].$message }}</small>
      </div>

      <!-- 密码输入 -->
      <div class="form-group">
        <label for="password" class="block text-sm font-medium text-gray-300 mb-2">新密码</label>
        <span class="p-input-icon-left w-full">
          <i class="pi pi-lock"></i>
          <Password
            id="password"
            v-model="password"
            toggleMask
            class="w-full"
            inputClass="w-full"
            placeholder="输入新密码"
            :class="{ 'p-invalid': v$.password.$error }"
            @blur="v$.password.$touch()"
          />
        </span>
        <small v-if="v$.password.$error" class="text-red-400">{{ v$.password.$errors[0].$message }}</small>
      </div>

      <!-- 确认密码输入 -->
      <div class="form-group">
        <label for="passwordConfirmation" class="block text-sm font-medium text-gray-300 mb-2">确认密码</label>
        <span class="p-input-icon-left w-full">
          <i class="pi pi-lock"></i>
          <Password
            id="passwordConfirmation"
            v-model="passwordConfirmation"
            toggleMask
            :feedback="false"
            class="w-full"
            inputClass="w-full"
            placeholder="再次输入新密码"
            :class="{ 'p-invalid': v$.passwordConfirmation.$error }"
            @blur="v$.passwordConfirmation.$touch()"
          />
        </span>
        <small v-if="v$.passwordConfirmation.$error" class="text-red-400">{{ v$.passwordConfirmation.$errors[0].$message }}</small>
      </div>

      <!-- 提交按钮 -->
      <Button
        type="submit"
        label="重置密码"
        icon="pi pi-check"
        class="w-full"
        :loading="loading"
      />

      <!-- 返回登录 -->
      <div class="text-center mt-6">
        <router-link to="/auth/login" class="text-cyan-400 hover:text-cyan-300">
          返回登录
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { ResetPasswordModule } from '@/server/view/auth/auth';

export default {
  name: 'ResetPasswordView',
  ...ResetPasswordModule
};
</script>

<style lang="scss" scoped>
@use'../../styles/view/auth/auth.scss';
</style>
