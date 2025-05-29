import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default function useAppNavbar() {
    const route = useRoute()
    const authStore = useAuthStore()

    // 响应式数据
    const isScrolled = ref(false)
    const isMobileMenuOpen = ref(false)

    // 计算属性
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const userAvatar = computed(() => authStore.user?.avatar || '/default-avatar.png')

    // 导航菜单项
    const navItems = [
        { path: '/', label: '首页', icon: 'pi-home' },
        { path: '/metaverse', label: '元宇宙', icon: 'pi-globe' },
        { path: '/ai/chat', label: 'AI助手', icon: 'pi-android' },
        { path: '/user/friends', label: '社交空间', icon: 'pi-users' },
        { path: '/about', label: '关于我们', icon: 'pi-info-circle' }
    ]

    // 滚动监听
    const handleScroll = () => {
        isScrolled.value = window.scrollY > 50
    }

    // 切换移动端菜单
    const toggleMobileMenu = () => {
        isMobileMenuOpen.value = !isMobileMenuOpen.value
    }

    // 关闭移动端菜单
    const closeMobileMenu = () => {
        isMobileMenuOpen.value = false
    }

    // 检查路由是否活跃
    const isRouteActive = (path) => {
        if (path === '/') {
            return route.path === '/'
        }
        return route.path.startsWith(path)
    }

    // 处理导航点击
    const handleNavClick = (path) => {
        closeMobileMenu()
        // 路由跳转会在模板中处理
    }

    // 处理外部链接点击
    const handleExternalClick = (url) => {
        window.open(url, '_blank')
    }

    // 处理键盘事件
    const handleKeydown = (event) => {
        if (event.key === 'Escape') {
            closeMobileMenu()
        }
    }

    // 生命周期钩子
    onMounted(() => {
        window.addEventListener('scroll', handleScroll)
        document.addEventListener('keydown', handleKeydown)

        // 点击外部关闭移动菜单
        document.addEventListener('click', (event) => {
            const navbar = document.querySelector('.app-navbar')
            if (navbar && !navbar.contains(event.target)) {
                closeMobileMenu()
            }
        })
    })

    onUnmounted(() => {
        window.removeEventListener('scroll', handleScroll)
        document.removeEventListener('keydown', handleKeydown)
    })

    return {
        // 响应式数据
        isScrolled,
        isMobileMenuOpen,

        // 计算属性
        isAuthenticated,
        userAvatar,
        navItems,

        // 方法
        toggleMobileMenu,
        closeMobileMenu,
        isRouteActive,
        handleNavClick,
        handleExternalClick
    }
}
