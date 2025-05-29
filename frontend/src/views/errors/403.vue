<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8 text-center">
            <div>
                <h1 class="text-9xl font-extrabold text-red-600">403</h1>
                <h2 class="mt-6 text-3xl font-bold text-gray-900">访问被拒绝</h2>
                <p class="mt-2 text-sm text-gray-600">
                    抱歉，您没有权限访问此页面。
                </p>
            </div>

            <div class="mt-8 space-y-4">
                <button @click="goBack"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors">
                    返回上一页
                </button>

                <router-link to="/"
                    class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors">
                    返回首页
                </router-link>
            </div>

            <div class="mt-8">
                <p class="text-sm text-gray-500">
                    如果您认为这是一个错误，请联系管理员。
                </p>

                <div class="flex justify-center space-x-6 mt-4">
                    <router-link to="/dashboard" class="text-red-600 hover:text-red-800 text-sm font-medium">
                        仪表板
                    </router-link>
                    <router-link to="/user/profile" class="text-red-600 hover:text-red-800 text-sm font-medium">
                        个人资料
                    </router-link>
                    <router-link to="/contact" class="text-red-600 hover:text-red-800 text-sm font-medium">
                        联系我们
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
