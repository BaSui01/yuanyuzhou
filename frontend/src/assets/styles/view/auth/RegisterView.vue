<template>
  <div class="register-view">
    <div class="mb-8 text-center">
      <h2 class="text-2xl font-bold text-white">创建账户</h2>
      <p class="text-gray-400 mt-2">加入元宇宙社交空间，开启无限可能</p>
    </div>

    <!-- 注册表单 -->
    <form @submit.prevent="handleRegister" class="space-y-6">
      <!-- 成功提示 -->
      <div v-if="successMessage" class="bg-green-500/20 border border-green-500/30 text-green-400 px-4 py-3 rounded-lg text-sm">
        {{ successMessage }}
      </div>

      <!-- 错误提示 -->
      <div v-if="errorMessage" class="bg-red-500/20 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg text-sm">
        {{ errorMessage }}
      </div>

      <!-- 用户名输入 -->
      <div class="form-group">
        <label for="name" class="block text-sm font-medium text-gray-300 mb-2">用户名</label>
        <span class="p-input-icon-left w-full">
          <i class="pi pi-user"></i>
          <InputText
            id="name"
            v-model="name"
            type="text"
            class="w-full"
            placeholder="输入您的用户名"
            :class="{ 'p-invalid': v$.name.$error }"
            @blur="v$.name.$touch()"
          />
        </span>
        <small v-if="v$.name.$error" class="text-red-400">{{ v$.name.$errors[0].$message }}</small>
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
        <label for="password" class="block text-sm font-medium text-gray-300 mb-2">密码</label>
        <span class="p-input-icon-left w-full">
          <i class="pi pi-lock"></i>
          <Password
            id="password"
            v-model="password"
            toggleMask
            class="w-full"
            inputClass="w-full"
            placeholder="设置您的密码"
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
            placeholder="再次输入密码"
            :class="{ 'p-invalid': v$.passwordConfirmation.$error }"
            @blur="v$.passwordConfirmation.$touch()"
          />
        </span>
        <small v-if="v$.passwordConfirmation.$error" class="text-red-400">{{ v$.passwordConfirmation.$errors[0].$message }}</small>
      </div>

      <!-- 同意条款 -->
      <div class="form-group">
        <div class="flex items-center">
          <Checkbox
            id="agreeTerms"
            v-model="agreeTerms"
            :binary="true"
            :class="{ 'p-invalid': v$.agreeTerms.$error }"
            @blur="v$.agreeTerms.$touch()"
          />
          <label for="agreeTerms" class="ml-2 text-sm text-gray-300">
            我已阅读并同意
            <a href="#" class="text-cyan-400 hover:text-cyan-300">服务条款</a>
            和
            <a href="#" class="text-cyan-400 hover:text-cyan-300">隐私政策</a>
          </label>
        </div>
        <small v-if="v$.agreeTerms.$error" class="text-red-400 block mt-1">{{ v$.agreeTerms.$errors[0].$message }}</small>
      </div>

      <!-- 提交按钮 -->
      <Button
        type="submit"
        label="注册"
        icon="pi pi-user-plus"
        class="w-full"
        :loading="loading"
      />

      <!-- 社交登录 -->
      <div class="social-login">
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-700"></div>
          </div>
          <div class="relative flex justify-center">
            <span class="bg-gray-900 px-4 text-sm text-gray-400">或通过以下方式注册</span>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-3">
          <Button
            icon="pi pi-google"
            class="p-button-outlined p-button-secondary"
            @click="socialRegister('google')"
          />
          <Button
            icon="pi pi-facebook"
            class="p-button-outlined p-button-secondary"
            @click="socialRegister('facebook')"
          />
          <Button
            icon="pi pi-github"
            class="p-button-outlined p-button-secondary"
            @click="socialRegister('github')"
          />
        </div>
      </div>

      <!-- 登录链接 -->
      <div class="text-center mt-6">
        <p class="text-gray-400">
          已有账户?
          <router-link to="/auth/login" class="text-cyan-400 hover:text-cyan-300">
            立即登录
          </router-link>
        </p>
      </div>
    </form>
  </div>
</template>

<script>
import { RegisterModule } from '@/server/view/auth/auth';

export default {
  name: 'RegisterView',
  ...RegisterModule
};
</script>

<style lang="scss" scoped>
@use'../../styles/view/auth/auth.scss';
</style>
