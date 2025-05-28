<template>
  <div class="forgot-password-container">
    <h2>找回密码</h2>
    <p class="description">请输入您的邮箱地址，我们将发送重置密码链接给您。</p>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="email">邮箱</label>
        <InputText
          id="email"
          v-model="email"
          type="email"
          class="w-full"
          placeholder="请输入邮箱"
          :class="{ 'p-invalid': submitted && !email }"
        />
        <small v-if="submitted && !email" class="p-error">邮箱不能为空</small>
      </div>

      <Button
        type="submit"
        label="发送重置链接"
        class="w-full"
        :loading="loading"
      />

      <div class="form-footer">
        <p>记起密码了? <router-link to="/auth/login">返回登录</router-link></p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const email = ref('');
const loading = ref(false);
const submitted = ref(false);
const resetSent = ref(false);

const handleSubmit = async () => {
  submitted.value = true;

  if (!email.value) {
    return;
  }

  loading.value = true;

  try {
    await authStore.forgotPassword(email.value);
    resetSent.value = true;
  } catch (error) {
    console.error('发送重置密码邮件失败:', error);
  } finally {
    loading.value = false;
  }
};
</script>
