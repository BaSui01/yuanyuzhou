<template>
  <div id="app">
    <Toast position="top-right" />
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  console.log('元宇宙社交平台已启动')
})
</script>

<style lang="scss">
// 导入基础样式文件
@use '@styles/main.scss';

#app {
  min-height: 100vh;
  width: 100%;
}
</style>
