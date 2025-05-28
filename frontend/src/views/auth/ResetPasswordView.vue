<template>
  <div class="reset-password-container">
    <h2>重置密码</h2>
    <p class="description">请设置您的新密码。</p>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="password">新密码</label>
        <Password
          id="password"
          v-model="password"
          toggleMask
          class="w-full"
          placeholder="请输入新密码"
          :class="{ 'p-invalid': submitted && !password }"
        />
        <small v-if="submitted && !password" class="p-error">密码不能为空</small>
      </div>

      <div class="form-group">
        <label for="confirmPassword">确认密码</label>
        <Password
          id="confirmPassword"
          v-model="confirmPassword"
          toggleMask
          class="w-full"
          placeholder="请再次输入新密码"
          :class="{ 'p-invalid': submitted && !confirmPassword || (submitted && password !== confirmPassword) }"
          :feedback="false"
        />
        <small v-if="submitted && !confirmPassword" class="p-error">请确认密码</small>
        <small v-else-if="submitted && password !== confirmPassword" class="p-error">两次密码不一致</small>
      </div>

      <Button
        type="submit"
        label="重置密码"
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
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const token = ref('');
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const submitted = ref(false);

onMounted(() => {
  token.value = route.query.token;

  if (!token.value) {
    router.push('/auth/login');
  }
});

const handleSubmit = async () => {
  submitted.value = true;

  if (!password.value || !confirmPassword.value) {
    return;
  }

  if (password.value !== confirmPassword.value) {
    return;
  }

  loading.value = true;

  try {
    await authStore.resetPassword({
      token: token.value,
      password: password.value
    });

    router.push('/auth/login');
  } catch (error) {
    console.error('重置密码失败:', error);
  } finally {
    loading.value = false;
  }
};
</script>
