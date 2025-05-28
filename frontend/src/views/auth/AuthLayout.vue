<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-logo">
        <img src="@/assets/logo.png" alt="Logo" />
        <h1>元宇宙社交空间</h1>
      </div>
      <div class="auth-content">
        <router-view />
      </div>
      <div class="auth-footer">
        <p>© 2023 元宇宙社交空间 - Web版桌宠AI助手</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// 使用外部JS文件，不内嵌JS
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(() => {
  // 可以在这里添加认证布局加载后的逻辑
  console.log('Auth layout mounted');
});
</script>

<style lang="scss">
// 引入外部SCSS文件
@import '@/assets/styles/view/auth/auth.scss';
</style>
