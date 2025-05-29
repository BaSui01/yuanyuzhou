<template>
    <div class="about-page">
        <AppNavbar />

        <main class="main-content">
            <!-- 页面头部 -->
            <section class="page-header">
                <div class="container mx-auto px-6 py-20">
                    <div class="text-center">
                        <h1 class="page-title">关于我们</h1>
                        <p class="page-subtitle">了解元宇宙社交空间的愿景与使命</p>
                    </div>
                </div>
            </section>

            <!-- 公司介绍 -->
            <section class="company-intro py-20">
                <div class="container mx-auto px-6">
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                        <div class="content">
                            <h2 class="section-title">我们的愿景</h2>
                            <p class="text-lg text-gray-300 mb-6">
                                元宇宙社交空间致力于打造下一代虚拟社交平台，通过先进的AI技术和沉浸式3D体验，
                                为用户创造一个充满无限可能的数字世界。
                            </p>
                            <p class="text-lg text-gray-300 mb-6">
                                我们相信技术应该服务于人类的情感需求和社交欲望，通过智能AI伙伴和丰富的虚拟环境，
                                让每个人都能在数字空间中找到归属感和成就感。
                            </p>
                            <div class="features-list">
                                <div class="feature-item">
                                    <i class="pi pi-check-circle text-cyan-400"></i>
                                    <span>创新的AI社交体验</span>
                                </div>
                                <div class="feature-item">
                                    <i class="pi pi-check-circle text-cyan-400"></i>
                                    <span>沉浸式3D虚拟环境</span>
                                </div>
                                <div class="feature-item">
                                    <i class="pi pi-check-circle text-cyan-400"></i>
                                    <span>个性化定制服务</span>
                                </div>
                            </div>
                        </div>
                        <div class="image-container">
                            <div class="placeholder-image">
                                <i class="pi pi-image text-6xl text-gray-500"></i>
                                <p class="text-gray-500 mt-4">公司愿景图片</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 发展历程 -->
            <section class="company-history py-20 bg-black/20">
                <div class="container mx-auto px-6">
                    <h2 class="section-title text-center mb-16">发展历程</h2>
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">2024</div>
                            <div class="timeline-content">
                                <h3>平台正式发布</h3>
                                <p>元宇宙社交空间正式上线，为用户提供全新的AI社交体验</p>
                            </div>
                        </div>
                        <div class="timeline-item">
                            <div class="timeline-date">2023</div>
                            <div class="timeline-content">
                                <h3>技术研发阶段</h3>
                                <p>核心AI技术研发完成，3D虚拟环境构建系统搭建</p>
                            </div>
                        </div>
                        <div class="timeline-item">
                            <div class="timeline-date">2022</div>
                            <div class="timeline-content">
                                <h3>公司成立</h3>
                                <p>元宇宙社交空间项目启动，核心团队组建完成</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 核心价值 -->
            <section class="core-values py-20">
                <div class="container mx-auto px-6">
                    <h2 class="section-title text-center mb-16">核心价值</h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div class="value-card">
                            <div class="value-icon">
                                <i class="pi pi-heart text-4xl text-red-400"></i>
                            </div>
                            <h3>以人为本</h3>
                            <p>始终把用户体验和情感需求放在首位，用技术服务于人性</p>
                        </div>
                        <div class="value-card">
                            <div class="value-icon">
                                <i class="pi pi-lightbulb text-4xl text-yellow-400"></i>
                            </div>
                            <h3>创新驱动</h3>
                            <p>持续探索前沿技术，为用户带来突破性的社交体验</p>
                        </div>
                        <div class="value-card">
                            <div class="value-icon">
                                <i class="pi pi-shield text-4xl text-green-400"></i>
                            </div>
                            <h3>安全可信</h3>
                            <p>保护用户隐私和数据安全，建立可信赖的虚拟社交环境</p>
                        </div>
                    </div>
                </div>
            </section>
        </main>

        <AppFooter />
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import useAboutPage from './AboutView.js'

// 使用页面逻辑
const { pageData, loadPageData } = useAboutPage()

onMounted(() => {
    loadPageData()
})
</script>

<style lang="scss" scoped>
@use '@styles/components/pages/AboutView.scss';
</style>
