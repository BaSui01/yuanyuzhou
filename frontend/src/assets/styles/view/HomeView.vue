<template>
    <div class="home-view min-h-screen flex flex-col">
        <!-- 导航栏 -->
        <nav class="fixed top-0 left-0 right-0 z-50 glass-dark">
            <div class="container mx-auto px-6 py-4">
                <div class="flex items-center justify-between">
                    <!-- Logo -->
                    <div class="flex items-center space-x-2">
                        <div
                            class="w-10 h-10 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg flex items-center justify-center">
                            <i class="pi pi-sparkles text-white text-xl"></i>
                        </div>
                        <h1 class="text-xl font-bold text-gradient">元宇宙社交空间</h1>
                    </div>

                    <!-- 导航菜单 -->
                    <div class="hidden md:flex items-center space-x-6">
                        <router-link to="/" class="nav-link active">首页</router-link>
                        <router-link to="/metaverse" class="nav-link">元宇宙</router-link>
                        <router-link to="/ai-chat" class="nav-link">AI助手</router-link>
                        <router-link to="/social" class="nav-link">社交空间</router-link>
                    </div>

                    <!-- 用户操作 -->
                    <div class="flex items-center space-x-4">
                        <template v-if="!isAuthenticated">
                            <Button label="登录" class="btn-ghost" @click="$router.push('/auth/login')" />
                            <Button label="注册" class="btn-primary" @click="$router.push('/auth/register')" />
                        </template>
                        <template v-else>
                            <Button label="进入空间" class="btn-primary" @click="$router.push('/dashboard')" />
                            <Avatar :image="userAvatar" class="avatar cursor-pointer" @click="$router.push('/profile')"
                                size="normal" />
                        </template>
                    </div>
                </div>
            </div>
        </nav>

        <!-- 主要内容 -->
        <main class="flex-1 pt-20">
            <!-- 英雄区域 -->
            <section class="hero-section min-h-screen flex items-center justify-center relative overflow-hidden">
                <div class="container mx-auto px-6 text-center relative z-10">
                    <div class="max-w-4xl mx-auto">
                        <!-- 主标题 -->
                        <h1 class="text-5xl md:text-7xl font-bold mb-6 float-animation">
                            <span class="text-gradient">元宇宙</span>
                            <br>
                            <span class="text-white">AI桌宠社交空间</span>
                        </h1>

                        <!-- 副标题 -->
                        <p class="text-xl md:text-2xl text-gray-300 mb-8 leading-relaxed">
                            与智能AI伴侣互动，探索无限可能的虚拟世界
                            <br>
                            体验前所未有的沉浸式社交体验
                        </p>

                        <!-- 特性标签 -->
                        <div class="flex flex-wrap justify-center gap-4 mb-12">
                            <div class="feature-tag">
                                <i class="pi pi-robot mr-2"></i>
                                智能AI桌宠
                            </div>
                            <div class="feature-tag">
                                <i class="pi pi-volume-up mr-2"></i>
                                语音交互
                            </div>
                            <div class="feature-tag">
                                <i class="pi pi-globe mr-2"></i>
                                3D虚拟空间
                            </div>
                            <div class="feature-tag">
                                <i class="pi pi-users mr-2"></i>
                                社交互动
                            </div>
                        </div>

                        <!-- 操作按钮 -->
                        <div class="flex flex-col sm:flex-row gap-4 justify-center">
                            <Button v-if="!isAuthenticated" label="立即开始" icon="pi pi-play"
                                class="btn-primary text-lg px-8 py-4" @click="$router.push('/auth/register')" />
                            <Button v-else label="进入我的空间" icon="pi pi-home" class="btn-primary text-lg px-8 py-4"
                                @click="$router.push('/dashboard')" />
                            <Button label="观看演示" icon="pi pi-play-circle" class="btn-ghost text-lg px-8 py-4"
                                @click="playDemo" />
                        </div>
                    </div>
                </div>

                <!-- 浮动装饰元素 -->
                <div class="floating-elements">
                    <div class="floating-orb orb-1"></div>
                    <div class="floating-orb orb-2"></div>
                    <div class="floating-orb orb-3"></div>
                </div>
            </section>

            <!-- 特性介绍 -->
            <section class="features-section py-20 relative">
                <div class="container mx-auto px-6">
                    <div class="text-center mb-16">
                        <h2 class="text-4xl font-bold text-white mb-4">核心特性</h2>
                        <p class="text-xl text-gray-300">探索我们的创新功能</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        <!-- AI桌宠 -->
                        <div class="feature-card card p-8 text-center">
                            <div class="feature-icon mb-6">
                                <i class="pi pi-android text-6xl text-cyan-400"></i>
                            </div>
                            <h3 class="text-2xl font-bold text-white mb-4">智能AI桌宠</h3>
                            <p class="text-gray-300 leading-relaxed">
                                个性化AI伴侣，具备学习能力和情感表达，陪伴您的每一天
                            </p>
                        </div>

                        <!-- 语音交互 -->
                        <div class="feature-card card p-8 text-center">
                            <div class="feature-icon mb-6">
                                <i class="pi pi-microphone text-6xl text-purple-400"></i>
                            </div>
                            <h3 class="text-2xl font-bold text-white mb-4">语音交互</h3>
                            <p class="text-gray-300 leading-relaxed">
                                先进的语音识别和合成技术，让对话更自然、更真实
                            </p>
                        </div>

                        <!-- 3D空间 -->
                        <div class="feature-card card p-8 text-center">
                            <div class="feature-icon mb-6">
                                <i class="pi pi-box text-6xl text-pink-400"></i>
                            </div>
                            <h3 class="text-2xl font-bold text-white mb-4">3D虚拟空间</h3>
                            <p class="text-gray-300 leading-relaxed">
                                沉浸式3D环境，自由探索和自定义您的专属虚拟世界
                            </p>
                        </div>

                        <!-- 社交功能 -->
                        <div class="feature-card card p-8 text-center">
                            <div class="feature-icon mb-6">
                                <i class="pi pi-users text-6xl text-green-400"></i>
                            </div>
                            <h3 class="text-2xl font-bold text-white mb-4">社交互动</h3>
                            <p class="text-gray-300 leading-relaxed">
                                与其他用户和AI伙伴互动，建立有意义的虚拟关系
                            </p>
                        </div>

                        <!-- 个性化定制 -->
                        <div class="feature-card card p-8 text-center">
                            <div class="feature-icon mb-6">
                                <i class="pi pi-palette text-6xl text-yellow-400"></i>
                            </div>
                            <h3 class="text-2xl font-bold text-white mb-4">个性化定制</h3>
                            <p class="text-gray-300 leading-relaxed">
                                自定义AI性格、外观和行为，打造独一无二的专属伴侣
                            </p>
                        </div>

                        <!-- 智能学习 -->
                        <div class="feature-card card p-8 text-center">
                            <div class="feature-icon mb-6">
                                <i class="pi pi-brain text-6xl text-red-400"></i>
                            </div>
                            <h3 class="text-2xl font-bold text-white mb-4">智能学习</h3>
                            <p class="text-gray-300 leading-relaxed">
                                AI持续学习您的偏好和习惯，提供越来越贴心的服务
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 用户统计 -->
            <section class="stats-section py-20 relative">
                <div class="container mx-auto px-6">
                    <div class="glass-dark rounded-2xl p-8">
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
                            <div class="stat-item">
                                <div class="text-4xl font-bold text-cyan-400 mb-2">
                                    {{ formatNumber(stats.users) }}+
                                </div>
                                <div class="text-gray-300">活跃用户</div>
                            </div>
                            <div class="stat-item">
                                <div class="text-4xl font-bold text-purple-400 mb-2">
                                    {{ formatNumber(stats.aiPets) }}+
                                </div>
                                <div class="text-gray-300">AI桌宠</div>
                            </div>
                            <div class="stat-item">
                                <div class="text-4xl font-bold text-pink-400 mb-2">
                                    {{ formatNumber(stats.conversations) }}+
                                </div>
                                <div class="text-gray-300">对话次数</div>
                            </div>
                            <div class="stat-item">
                                <div class="text-4xl font-bold text-green-400 mb-2">
                                    {{ formatNumber(stats.online) }}
                                </div>
                                <div class="text-gray-300">在线用户</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- CTA区域 -->
            <section class="cta-section py-20 relative">
                <div class="container mx-auto px-6 text-center">
                    <div class="max-w-3xl mx-auto">
                        <h2 class="text-4xl font-bold text-white mb-6">
                            准备好开始您的<span class="text-gradient">元宇宙</span>之旅了吗？
                        </h2>
                        <p class="text-xl text-gray-300 mb-8">
                            加入我们，与AI伙伴一起探索无限可能的虚拟世界
                        </p>
                        <Button v-if="!isAuthenticated" label="免费注册" icon="pi pi-user-plus"
                            class="btn-primary text-xl px-12 py-4" @click="$router.push('/auth/register')" />
                        <Button v-else label="立即体验" icon="pi pi-rocket" class="btn-primary text-xl px-12 py-4"
                            @click="$router.push('/dashboard')" />
                    </div>
                </div>
            </section>
        </main>

        <!-- 页脚 -->
        <footer class="footer bg-black/20 backdrop-blur-sm py-8">
            <div class="container mx-auto px-6">
                <div class="text-center text-gray-400">
                    <p>&copy; 2024 元宇宙社交空间. 保留所有权利.</p>
                    <div class="flex justify-center space-x-6 mt-4">
                        <a href="#" class="hover:text-cyan-400 transition-colors">隐私政策</a>
                        <a href="#" class="hover:text-cyan-400 transition-colors">服务条款</a>
                        <a href="#" class="hover:text-cyan-400 transition-colors">联系我们</a>
                    </div>
                </div>
            </div>
        </footer>

        <!-- 演示视频弹窗 -->
        <Dialog v-model:visible="showDemo" modal header="产品演示" class="w-full max-w-4xl">
            <div class="aspect-video bg-gray-900 rounded-lg flex items-center justify-center">
                <div class="text-center text-gray-400">
                    <i class="pi pi-play-circle text-6xl mb-4"></i>
                    <p>演示视频即将推出</p>
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script setup>
import HomeViews from '@/server/view/HomeViews'
</script>

<style lang="scss" scoped>
@use '../styles/view/home.scss'
</style>
