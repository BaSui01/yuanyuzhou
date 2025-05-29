<template>
    <nav class="app-navbar" :class="{ scrolled: isScrolled }">
        <div class="navbar-container">
            <div class="navbar-content">
                <!-- Logo -->
                <router-link to="/" class="navbar-logo" @click="closeMobileMenu">
                    <div class="logo-icon">
                        <i class="pi pi-sparkles"></i>
                    </div>
                    <h1 class="logo-text">元宇宙社交空间</h1>
                </router-link>

                <!-- 桌面端导航菜单 -->
                <div class="navbar-menu">
                    <router-link v-for="item in navItems" :key="item.path" :to="item.path" class="nav-link"
                        :class="{ active: isRouteActive(item.path) }" @click="handleNavClick(item.path)">
                        <i :class="`pi ${item.icon}`"></i>
                        {{ item.label }}
                    </router-link>
                </div>

                <!-- 用户操作区域 -->
                <div class="navbar-actions">
                    <template v-if="!isAuthenticated">
                        <Button label="登录" class="btn-ghost" @click="$router.push('/auth/login')" />
                        <Button label="注册" class="btn-primary" @click="$router.push('/auth/register')" />
                    </template>
                    <template v-else>
                        <Button label="进入空间" class="btn-primary" @click="$router.push('/dashboard')" />
                        <Avatar :image="userAvatar" class="avatar cursor-pointer" @click="$router.push('/user/profile')"
                            size="normal" />
                    </template>

                    <!-- 移动端菜单按钮 -->
                    <button class="mobile-menu-btn" @click="toggleMobileMenu" :aria-expanded="isMobileMenuOpen"
                        aria-label="切换导航菜单">
                        <i :class="isMobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'"></i>
                    </button>
                </div>
            </div>

            <!-- 移动端菜单 -->
            <div class="mobile-menu" :class="{ open: isMobileMenuOpen }">
                <div class="mobile-nav-links">
                    <router-link v-for="item in navItems" :key="item.path" :to="item.path" class="nav-link"
                        :class="{ active: isRouteActive(item.path) }" @click="handleNavClick(item.path)">
                        <i :class="`pi ${item.icon}`"></i>
                        {{ item.label }}
                    </router-link>
                </div>

                <div class="mobile-actions">
                    <template v-if="!isAuthenticated">
                        <router-link to="/auth/login" class="btn btn-ghost" @click="closeMobileMenu">
                            登录
                        </router-link>
                        <router-link to="/auth/register" class="btn btn-primary" @click="closeMobileMenu">
                            注册
                        </router-link>
                    </template>
                    <template v-else>
                        <router-link to="/dashboard" class="btn btn-primary" @click="closeMobileMenu">
                            进入空间
                        </router-link>
                        <router-link to="/user/profile" class="btn btn-ghost" @click="closeMobileMenu">
                            个人中心
                        </router-link>
                    </template>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import useAppNavbar from './AppNavbar.js'

// 使用组合式函数
const {
    isScrolled,
    isMobileMenuOpen,
    isAuthenticated,
    userAvatar,
    navItems,
    toggleMobileMenu,
    closeMobileMenu,
    isRouteActive,
    handleNavClick
} = useAppNavbar()
</script>

<style lang="scss" scoped>
@use '@styles/components/AppNavbar.scss';
</style>
