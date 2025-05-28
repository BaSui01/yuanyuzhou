<template>
  <div class="login-container">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
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

      <div class="form-group">
        <label for="password">密码</label>
        <Password
          id="password"
          v-model="password"
          toggleMask
          class="w-full"
          placeholder="请输入密码"
          :class="{ 'p-invalid': submitted && !password }"
          :feedback="false"
        />
        <small v-if="submitted && !password" class="p-error">密码不能为空</small>
      </div>

      <div class="form-options">
        <div class="remember-me">
          <Checkbox v-model="rememberMe" :binary="true" id="rememberMe" />
          <label for="rememberMe" class="ml-2">记住我</label>
        </div>
        <router-link to="/auth/forgot-password" class="forgot-link">忘记密码?</router-link>
      </div>

      <Button
        type="submit"
        label="登录"
        class="w-full"
        :loading="loading"
      />

      <div class="form-footer">
        <p>还没有账号? <router-link to="/auth/register">立即注册</router-link></p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const rememberMe = ref(false);
const loading = ref(false);
const submitted = ref(false);

const handleLogin = async () => {
  submitted.value = true;

  if (!email.value || !password.value) {
    return;
  }

  loading.value = true;

  try {
    await authStore.login({
      email: email.value,
      password: password.value,
      rememberMe: rememberMe.value
    });

    router.push('/dashboard');
  } catch (error) {
    console.error('登录失败:', error);
  } finally {
    loading.value = false;
  }
};
</script>
