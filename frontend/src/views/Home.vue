<template>
  <div>
    <!-- 导航栏 -->
    <AppNavbar />

    <!-- 加载动画 -->
    <LoadingSpinner v-if="loading" variant="dots" size="lg" text="页面加载中..." />

    <div v-else class="home-container">
      <!-- 头部横幅 -->
      <section class="hero" v-scroll-reveal="{ delay: 200 }">
        <div class="hero-content">
          <h1 class="title">探索无限可能的元宇宙世界</h1>
          <p class="subtitle">连接虚拟与现实，创造无限可能</p>
          <div class="cta-buttons">
            <Button label="开始探索" class="p-button-rounded p-button-lg" @click="navigateTo('/metaverse')" />
            <Button label="了解更多" class="p-button-outlined p-button-rounded p-button-lg"
              @click="scrollToSection('features')" />
          </div>
        </div>
      </section>

      <!-- 特色内容区 -->
      <section id="features" class="features" v-scroll-reveal="{ delay: 300 }">
        <h2 class="section-title">平台特色</h2>
        <div class="feature-cards">
          <div class="feature-card" v-for="(feature, index) in features" :key="index"
            v-scroll-reveal="{ delay: 200 + (index * 100) }">
            <i :class="`pi ${feature.icon} feature-icon`"></i>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </section>

      <!-- 元宇宙展示区 -->
      <section class="metaverse-showcase" v-scroll-reveal="{ delay: 400 }">
        <div class="showcase-content">
          <h2 class="section-title">沉浸式体验</h2>
          <p class="section-description">通过最新的VR/AR技术，带给您身临其境的元宇宙体验</p>
          <ul class="feature-list">
            <li v-for="(item, index) in experienceFeatures" :key="index"
              v-scroll-reveal="{ delay: 200 + (index * 100) }">
              <i class="pi pi-check"></i> {{ item }}
            </li>
          </ul>
          <Button label="体验演示" icon="pi pi-play" class="p-button-rounded" @click="showDemo" />
        </div>
        <div class="showcase-image" v-scroll-reveal="{ delay: 500 }">
          <img src="/img/metaverse-preview.svg" alt="元宇宙场景预览" class="preview-image" />
        </div>
      </section>

      <!-- 最新动态 -->
      <section class="news" v-scroll-reveal="{ delay: 500 }">
        <h2 class="section-title">最新动态</h2>
        <div class="news-cards">
          <div class="news-card" v-for="(article, index) in news" :key="index"
            v-scroll-reveal="{ delay: 200 + (index * 150) }">
            <div class="news-image">
              <img :src="article.image" :alt="article.title" class="article-image" />
            </div>
            <div class="news-content">
              <span class="news-date">{{ article.date }}</span>
              <h3 class="news-title">{{ article.title }}</h3>
              <p class="news-excerpt">{{ article.excerpt }}</p>
              <router-link :to="article.link" class="news-link">阅读更多 <i class="pi pi-arrow-right"></i></router-link>
            </div>
          </div>
        </div>
        <div class="view-all" v-scroll-reveal="{ delay: 600 }">
          <router-link to="/news" class="view-all-link">查看全部动态 <i class="pi pi-arrow-right"></i></router-link>
        </div>
      </section>

      <!-- 注册引导 -->
      <section class="signup-cta" v-scroll-reveal="{ delay: 700 }">
        <div class="cta-content">
          <h2>准备好开始您的元宇宙之旅了吗？</h2>
          <p>立即注册，开启您的虚拟世界探索</p>
          <div class="cta-buttons">
            <Button label="免费注册" icon="pi pi-user-plus" class="p-button-rounded p-button-lg"
              @click="navigateTo('/auth/register')" />
            <Button label="联系我们" icon="pi pi-envelope" class="p-button-outlined p-button-rounded p-button-lg"
              @click="navigateTo('/contact')" />
          </div>
        </div>
      </section>

      <!-- 页脚 -->
      <AppFooter />

      <!-- 返回顶部按钮 -->
      <Button icon="pi pi-arrow-up" class="back-to-top" :class="{ visible: showBackToTop }" @click="scrollToTop" />
    </div>

    <!-- 演示对话框 -->
    <Dialog v-model:visible="demoVisible" header="元宇宙演示" modal class="demo-dialog">
      <div class="demo-content">
        <p>此处将展示元宇宙空间的演示视频或交互体验。</p>
        <div class="demo-placeholder">
          <i class="pi pi-play-circle"></i>
          <span>演示视频</span>
        </div>
      </div>
    </Dialog>

    <!-- AI助手 -->
    <FloatingAIAssistant />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { routerUtils } from '@/modules/navigation/router'

// 导入组件
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import FloatingAIAssistant from '@/components/ui/FloatingAIAssistant.vue'

// 路由导航函数
const navigateTo = (path) => {
  routerUtils.navigate(path)
}

// 页面状态
const loading = ref(false)
const demoVisible = ref(false)
const showBackToTop = ref(false)

// 特色内容数据
const features = ref([
  {
    icon: 'pi-globe',
    title: '虚拟世界',
    description: '探索由AI生成的无限虚拟世界，与全球用户实时互动'
  },
  {
    icon: 'pi-users',
    title: '社交连接',
    description: '与朋友和新认识的人一起参与虚拟活动，建立真实的社交连接'
  },
  {
    icon: 'pi-desktop',
    title: '沉浸体验',
    description: '通过最新的VR/AR技术，带给您身临其境的元宇宙体验'
  },
  {
    icon: 'pi-wallet',
    title: '数字资产',
    description: '创建、交易和收集独特的数字资产，建立您的虚拟财富'
  }
])

// 体验特性
const experienceFeatures = ref([
  '高清3D图形和逼真的物理效果',
  '多平台支持：VR、AR、PC和移动设备',
  '实时语音和文字交流',
  '个性化虚拟形象定制',
  'AI驱动的NPC互动'
])

// 新闻数据
const news = ref([
  {
    title: '元宇宙平台正式发布',
    excerpt: '我们很高兴地宣布，经过两年的开发，元宇宙平台正式向公众开放...',
    date: '2023-10-15',
    image: '/img/news/launch.svg',
    link: '/news/1'
  },
  {
    title: '虚拟音乐会吸引超过10万用户',
    excerpt: '上周末在我们的虚拟世界中举办的音乐会创下了新的参与记录...',
    date: '2023-09-28',
    image: '/img/news/concert.svg',
    link: '/news/2'
  },
  {
    title: '新的AR功能即将推出',
    excerpt: '下个月，我们将推出革命性的AR功能，让虚拟世界与现实世界无缝融合...',
    date: '2023-09-10',
    image: '/img/news/ar-update.svg',
    link: '/news/3'
  }
])

// 滚动到指定部分
const scrollToSection = (sectionId) => {
  const section = document.getElementById(sectionId)
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' })
  }
}

// 返回顶部
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 显示演示对话框
const showDemo = () => {
  demoVisible.value = true
}

// 监听滚动事件
onMounted(() => {
  window.addEventListener('scroll', () => {
    showBackToTop.value = window.scrollY > 300
  })
})
</script>

<style lang="scss" scoped>
@use '@styles/view/home.scss';
</style>
