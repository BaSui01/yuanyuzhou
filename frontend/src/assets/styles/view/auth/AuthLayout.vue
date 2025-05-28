<template>
  <div class="auth-layout">
    <div class="auth-container min-h-screen flex flex-col md:flex-row">
      <!-- 左侧信息面板 -->
      <div class="auth-info bg-gradient-to-br from-gray-900 to-gray-800 md:w-1/2 p-8 md:p-12 flex flex-col">
        <div class="mb-8">
          <router-link to="/" class="flex items-center">
            <img src="/logo.svg" alt="Logo" class="h-10 w-10 mr-3" />
            <span class="text-xl font-bold text-white">元宇宙社交空间</span>
          </router-link>
        </div>

        <div class="flex-1 flex flex-col justify-center">
          <h1 class="text-3xl md:text-4xl font-bold text-white mb-6">
            探索无限可能的<br />
            <span class="text-gradient">元宇宙社交空间</span>
          </h1>

          <p class="text-gray-300 mb-8 max-w-md">
            加入我们的元宇宙社交平台，体验沉浸式社交互动、AI智能助手和丰富的虚拟世界。
          </p>

          <div class="features space-y-4">
            <div class="feature flex items-center">
              <div class="feature-icon w-10 h-10 rounded-full bg-cyan-500/20 flex items-center justify-center mr-4">
                <i class="pi pi-comments text-cyan-400"></i>
              </div>
              <div>
                <h3 class="text-white font-medium">AI智能助手</h3>
                <p class="text-gray-400 text-sm">个性化AI伴侣，随时为您提供帮助</p>
              </div>
            </div>

            <div class="feature flex items-center">
              <div class="feature-icon w-10 h-10 rounded-full bg-purple-500/20 flex items-center justify-center mr-4">
                <i class="pi pi-globe text-purple-400"></i>
              </div>
              <div>
                <h3 class="text-white font-medium">沉浸式体验</h3>
                <p class="text-gray-400 text-sm">3D虚拟空间，身临其境的社交互动</p>
              </div>
            </div>

            <div class="feature flex items-center">
              <div class="feature-icon w-10 h-10 rounded-full bg-pink-500/20 flex items-center justify-center mr-4">
                <i class="pi pi-users text-pink-400"></i>
              </div>
              <div>
                <h3 class="text-white font-medium">社交连接</h3>
                <p class="text-gray-400 text-sm">与志同道合的朋友建立联系</p>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-auto pt-8">
          <p class="text-gray-500 text-sm">© 2025 元宇宙社交空间. 保留所有权利.</p>
        </div>
      </div>

      <!-- 右侧表单面板 -->
      <div class="auth-form md:w-1/2 p-8 md:p-12 flex flex-col justify-center items-center">
        <div class="w-full max-w-md">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { AuthLayoutModule } from '@/server/view/auth/auth';

export default {
  name: 'AuthLayout',
  ...AuthLayoutModule
};
</script>

<style lang="scss" scoped>
@use'../../styles/view/auth/auth.scss';
</style>
