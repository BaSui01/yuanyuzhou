<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8 text-center">
            <div>
                <h1 class="text-9xl font-extrabold text-blue-600">404</h1>
                <h2 class="mt-6 text-3xl font-bold text-gray-900">页面未找到</h2>
                <p class="mt-2 text-sm text-gray-600">
                    抱歉，您访问的页面不存在或已被移除。
                </p>
            </div>

            <div class="mt-8 space-y-4">
                <button @click="goBack"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                    返回上一页
                </button>

                <router-link to="/"
                    class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                    返回首页
                </router-link>
            </div>

            <div class="mt-8">
                <div class="flex justify-center space-x-6">
                    <router-link to="/dashboard" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                        仪表板
                    </router-link>
                    <router-link to="/ai/chat" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                        AI对话
                    </router-link>
                    <router-link to="/user/profile" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                        个人资料
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
    if (window.history.length > 1) {
        router.go(-1)
    } else {
        router.push('/')
    }
}
</script>
