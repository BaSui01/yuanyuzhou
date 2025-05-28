<template>
  <div class="dashboard-container">
    <div class="welcome-section">
      <h1>欢迎回来, {{ user.username }}</h1>
      <p>这是您的个人仪表盘，您可以在这里管理您的元宇宙社交空间和AI助手。</p>
    </div>

    <div class="dashboard-grid">
      <div class="dashboard-card">
        <div class="card-header">
          <i class="pi pi-users"></i>
          <h3>我的社交空间</h3>
        </div>
        <div class="card-content">
          <p>您的社交空间已经有 {{ stats.visitors || 0 }} 位访客。</p>
        </div>
        <div class="card-footer">
          <Button label="进入空间" icon="pi pi-arrow-right" @click="goToMetaverse" />
        </div>
      </div>

      <div class="dashboard-card">
        <div class="card-header">
          <i class="pi pi-comments"></i>
          <h3>AI助手对话</h3>
        </div>
        <div class="card-content">
          <p>您已经与AI助手进行了 {{ stats.conversations || 0 }} 次对话。</p>
        </div>
        <div class="card-footer">
          <Button label="开始聊天" icon="pi pi-comment" @click="goToAIChat" />
        </div>
      </div>

      <div class="dashboard-card">
        <div class="card-header">
          <i class="pi pi-volume-up"></i>
          <h3>语音实验室</h3>
        </div>
        <div class="card-content">
          <p>定制您的AI助手的声音和语言模式。</p>
        </div>
        <div class="card-footer">
          <Button label="调整声音" icon="pi pi-sliders-h" @click="goToVoiceLab" />
        </div>
      </div>

      <div class="dashboard-card">
        <div class="card-header">
          <i class="pi pi-heart"></i>
          <h3>我的AI伙伴</h3>
        </div>
        <div class="card-content">
          <p>定制您的AI伙伴的外观、性格和行为。</p>
        </div>
        <div class="card-footer">
          <Button label="定制伙伴" icon="pi pi-pencil" @click="goToAICompanion" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const user = ref({
  username: '用户',
  avatar: ''
});

const stats = ref({
  visitors: 0,
  conversations: 0
});

onMounted(async () => {
  try {
    // 获取用户信息
    const userData = await authStore.getUserProfile();
    user.value = userData;

    // 获取统计数据
    // 这里应该调用API获取实际数据
    stats.value = {
      visitors: Math.floor(Math.random() * 100),
      conversations: Math.floor(Math.random() * 50)
    };
  } catch (error) {
    console.error('获取用户数据失败:', error);
  }
});

const goToMetaverse = () => {
  router.push('/metaverse');
};

const goToAIChat = () => {
  router.push('/ai/chat');
};

const goToVoiceLab = () => {
  router.push('/ai/voice-lab');
};

const goToAICompanion = () => {
  router.push('/ai/companion');
};
</script>

<style lang="scss">
@import '@/assets/styles/view/dashboard.scss';
</style>
