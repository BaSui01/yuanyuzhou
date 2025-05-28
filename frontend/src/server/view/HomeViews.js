import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 响应式数据
const showDemo = ref(false)
const stats = ref({
    users: 12580,
    aiPets: 8964,
    conversations: 156789,
    online: 1247
})

// 计算属性
const isAuthenticated = computed(() => authStore.isAuthenticated)
const userAvatar = computed(() => authStore.userAvatar)

// 方法
const playDemo = () => {
    showDemo.value = true
}

const formatNumber = (num) => {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
    }
    return num.toString()
}

// 页面加载时的动画
onMounted(() => {
    // 可以添加页面加载动画
})
