<template>
  <div class="register-container">
    <h2>注册账号</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">用户名</label>
        <InputText
          id="username"
          v-model="username"
          class="w-full"
          placeholder="请输入用户名"
          :class="{ 'p-invalid': submitted && !username }"
        />
        <small v-if="submitted && !username" class="p-error">用户名不能为空</small>
      </div>

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
          placeholder="请再次输入密码"
          :class="{ 'p-invalid': submitted && !confirmPassword || (submitted && password !== confirmPassword) }"
          :feedback="false"
        />
        <small v-if="submitted && !confirmPassword" class="p-error">请确认密码</small>
        <small v-else-if="submitted && password !== confirmPassword" class="p-error">两次密码不一致</small>
      </div>

      <div class="form-options">
        <div class="terms">
          <Checkbox v-model="agreeTerms" :binary="true" id="agreeTerms" />
          <label for="agreeTerms" class="ml-2">我同意 <a href="#" @click.prevent="showTerms">服务条款</a> 和 <a href="#" @click.prevent="showPrivacy">隐私政策</a></label>
        </div>
      </div>

      <Button
        type="submit"
        label="注册"
        class="w-full"
        :loading="loading"
        :disabled="!agreeTerms"
      />

      <div class="form-footer">
        <p>已有账号? <router-link to="/auth/login">立即登录</router-link></p>
      </div>
    </form>

    <Dialog v-model:visible="termsVisible" header="服务条款" modal style="width: 50vw">
      <p>这里是服务条款内容...</p>
    </Dialog>

    <Dialog v-model:visible="privacyVisible" header="隐私政策" modal style="width: 50vw">
      <p>这里是隐私政策内容...</p>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const agreeTerms = ref(false);
const loading = ref(false);
const submitted = ref(false);
const termsVisible = ref(false);
const privacyVisible = ref(false);

const showTerms = () => {
  termsVisible.value = true;
};

const showPrivacy = () => {
  privacyVisible.value = true;
};

const handleRegister = async () => {
  submitted.value = true;

  if (!username.value || !email.value || !password.value || !confirmPassword.value) {
    return;
  }

  if (password.value !== confirmPassword.value) {
    return;
  }

  if (!agreeTerms.value) {
    return;
  }

  loading.value = true;

  try {
    await authStore.register({
      username: username.value,
      email: email.value,
      password: password.value
    });

    router.push('/auth/login');
  } catch (error) {
    console.error('注册失败:', error);
  } finally {
    loading.value = false;
  }
};
</script>
