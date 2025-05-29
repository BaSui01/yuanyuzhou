<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8 text-center">
            <div>
                <h1 class="text-9xl font-extrabold text-yellow-600">500</h1>
                <h2 class="mt-6 text-3xl font-bold text-gray-900">服务器错误</h2>
                <p class="mt-2 text-sm text-gray-600">
                    抱歉，服务器遇到了一个内部错误，无法完成您的请求。
                </p>
            </div>

            <div class="mt-8 space-y-4">
                <button @click="refresh"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-yellow-600 hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-colors">
                    刷新页面
                </button>

                <button @click="goBack"
                    class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-colors">
                    返回上一页
                </button>

                <router-link to="/"
                    class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-colors">
                    返回首页
                </router-link>
            </div>

            <div class="mt-8">
                <p class="text-sm text-gray-500">
                    错误代码：{{ errorCode }}
                </p>
                <p class="text-xs text-gray-400 mt-2">
                    如果问题持续存在，请联系技术支持。
                </p>

                <div class="flex justify-center space-x-6 mt-4">
                    <router-link to="/contact" class="text-yellow-600 hover:text-yellow-800 text-sm font-medium">
                        技术支持
                    </router-link>
                    <a href="mailto:support@example.com"
                        class="text-yellow-600 hover:text-yellow-800 text-sm font-medium">
                        发送邮件
                    </a>
                    <router-link to="/dashboard" class="text-yellow-600 hover:text-yellow-800 text-sm font-medium">
                        仪表板
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const errorCode = ref(generateErrorCode())

function generateErrorCode() {
    return `ERR-${Date.now().toString(36).toUpperCase()}-${Math.random().toString(36).substr(2, 5).toUpperCase()}`
}

const refresh = () => {
    window.location.reload()
}

const goBack = () => {
    if (window.history.length > 1) {
        router.go(-1)
    } else {
        router.push('/')
    }
}
</script>
