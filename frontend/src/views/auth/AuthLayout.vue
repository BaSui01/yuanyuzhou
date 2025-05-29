<template>
  <div class="auth-layout">
    <div class="auth-container">
      <div class="auth-logo">
        <img src="@/assets/img/logo.svg" alt="元宇宙" />
      </div>
      <div class="auth-content">
        <router-view />
      </div>
      <div class="auth-footer">
        <p>&copy; {{ currentYear }} 元宇宙社交空间. 保留所有权利.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style lang="scss">
@use '@/assets/styles/view/auth/auth.scss';
</style>
