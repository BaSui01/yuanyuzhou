<template>
    <footer class="app-footer">
        <div class="footer-content">
            <!-- 主要内容区域 -->
            <div class="footer-main">
                <!-- 关于我们 -->
                <div class="footer-section">
                    <h3>
                        <i class="pi pi-sparkles icon"></i>
                        关于我们
                    </h3>
                    <ul class="footer-links">
                        <li>
                            <router-link to="/about">
                                <i class="pi pi-info-circle link-icon"></i>
                                公司介绍
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/team">
                                <i class="pi pi-users link-icon"></i>
                                团队成员
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/careers">
                                <i class="pi pi-briefcase link-icon"></i>
                                加入我们
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/news">
                                <i class="pi pi-calendar link-icon"></i>
                                新闻资讯
                            </router-link>
                        </li>
                    </ul>
                </div>

                <!-- 产品服务 -->
                <div class="footer-section">
                    <h3>
                        <i class="pi pi-cog icon"></i>
                        产品服务
                    </h3>
                    <ul class="footer-links">
                        <li>
                            <router-link to="/metaverse">
                                <i class="pi pi-globe link-icon"></i>
                                元宇宙空间
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/ai/chat">
                                <i class="pi pi-android link-icon"></i>
                                AI智能助手
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/ai/voice-lab">
                                <i class="pi pi-microphone link-icon"></i>
                                语音实验室
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/user/friends">
                                <i class="pi pi-heart link-icon"></i>
                                社交互动
                            </router-link>
                        </li>
                    </ul>
                </div>

                <!-- 支持帮助 -->
                <div class="footer-section">
                    <h3>
                        <i class="pi pi-question-circle icon"></i>
                        支持帮助
                    </h3>
                    <ul class="footer-links">
                        <li>
                            <router-link to="/help">
                                <i class="pi pi-book link-icon"></i>
                                帮助中心
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/faq">
                                <i class="pi pi-comments link-icon"></i>
                                常见问题
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/contact">
                                <i class="pi pi-envelope link-icon"></i>
                                联系客服
                            </router-link>
                        </li>
                        <li>
                            <a href="#" @click="openFeedback">
                                <i class="pi pi-star link-icon"></i>
                                意见反馈
                            </a>
                        </li>
                    </ul>
                </div>

                <!-- 联系信息 -->
                <div class="footer-section">
                    <h3>
                        <i class="pi pi-map-marker icon"></i>
                        联系我们
                    </h3>
                    <div class="contact-info">
                        <div class="contact-item">
                            <i class="pi pi-phone contact-icon"></i>
                            <a href="tel:400-123-4567">400-123-4567</a>
                        </div>
                        <div class="contact-item">
                            <i class="pi pi-envelope contact-icon"></i>
                            <a href="mailto:contact@metaverse.com">contact@metaverse.com</a>
                        </div>
                        <div class="contact-item">
                            <i class="pi pi-map-marker contact-icon"></i>
                            <span>北京市朝阳区科技园区</span>
                        </div>
                    </div>

                    <!-- 社交媒体链接 -->
                    <div class="social-links">
                        <a href="#" @click="openSocial('weibo')" title="微博">
                            <i class="pi pi-share-alt"></i>
                        </a>
                        <a href="#" @click="openSocial('wechat')" title="微信">
                            <i class="pi pi-comments"></i>
                        </a>
                        <a href="#" @click="openSocial('qq')" title="QQ">
                            <i class="pi pi-users"></i>
                        </a>
                        <a href="#" @click="openSocial('github')" title="GitHub">
                            <i class="pi pi-github"></i>
                        </a>
                    </div>
                </div>
            </div>

            <!-- 页脚底部 -->
            <div class="footer-bottom">
                <div class="copyright">
                    &copy; {{ currentYear }} 元宇宙社交空间. 保留所有权利.
                </div>
                <div class="footer-legal">
                    <router-link to="/privacy">隐私政策</router-link>
                    <router-link to="/terms">服务条款</router-link>
                    <router-link to="/security">安全声明</router-link>
                    <router-link to="/sitemap">网站地图</router-link>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup>
import { computed } from 'vue'

// 当前年份
const currentYear = computed(() => new Date().getFullYear())

// 打开意见反馈
const openFeedback = () => {
    // 这里可以打开反馈弹窗或跳转到反馈页面
    console.log('打开意见反馈')
}

// 打开社交媒体链接
const openSocial = (platform) => {
    const socialLinks = {
        weibo: 'https://weibo.com/metaverse',
        wechat: 'javascript:void(0)', // 微信可以显示二维码
        qq: 'https://im.qq.com/index/',
        github: 'https://github.com/metaverse'
    }

    if (platform === 'wechat') {
        // 显示微信二维码或提示
        console.log('显示微信二维码')
        return
    }

    const url = socialLinks[platform]
    if (url) {
        window.open(url, '_blank')
    }
}
</script>

<style lang="scss" scoped>
@use '@styles/components/AppFooter.scss';
</style>
