<template>
  <div class="image-captioning-container">
    <AppNavbar />

    <div class="page-content">
      <div class="page-header">
        <h1>图像描述</h1>
        <p class="page-description">上传图片，AI将自动生成详细描述和标签</p>
      </div>

      <div class="captioning-section">
        <div class="upload-area"
             :class="{ 'drag-over': isDragging, 'has-image': selectedImage }"
             @dragover.prevent="handleDragOver"
             @dragleave.prevent="handleDragLeave"
             @drop.prevent="handleDrop">

          <div v-if="!selectedImage" class="upload-placeholder">
            <i class="pi pi-cloud-upload"></i>
            <p>拖放图片到此处，或 <span class="browse-link" @click="triggerFileInput">浏览文件</span></p>
            <p class="hint">支持 JPG, PNG, GIF 格式图片，最大 10MB</p>
            <input type="file" ref="fileInput" class="hidden-input" accept="image/*" @change="handleFileSelect" />
          </div>

          <div v-else class="image-preview">
            <img :src="selectedImage" alt="预览图片" class="preview-img" />
            <div class="image-actions">
              <Button icon="pi pi-times" class="p-button-rounded p-button-danger" @click="clearImage" />
            </div>
          </div>
        </div>

        <div class="action-controls">
          <Button label="生成描述" icon="pi pi-play" :disabled="!selectedImage || isProcessing" @click="generateCaption" class="p-button-primary" />
          <Button label="清除" icon="pi pi-trash" :disabled="!selectedImage || isProcessing" @click="clearImage" class="p-button-secondary" />
        </div>

        <ProgressBar v-if="isProcessing" mode="indeterminate" style="height: 6px; margin: 20px 0;" />

        <div v-if="caption" class="results-area">
          <h2>AI 描述结果</h2>

          <div class="caption-card">
            <h3>详细描述</h3>
            <p>{{ caption.description }}</p>

            <h3>图像标签</h3>
            <div class="tags-container">
              <Tag v-for="(tag, index) in caption.tags" :key="index" :value="tag" class="caption-tag" />
            </div>

            <h3>置信度</h3>
            <div class="confidence-bar">
              <div class="confidence-label">{{ Math.round(caption.confidence * 100) }}%</div>
              <ProgressBar :value="caption.confidence * 100" />
            </div>
          </div>

          <div class="action-buttons">
            <Button label="复制描述" icon="pi pi-copy" @click="copyDescription" />
            <Button label="下载结果" icon="pi pi-download" @click="downloadResults" />
            <Button label="分享" icon="pi pi-share-alt" @click="showShareDialog = true" />
          </div>
        </div>
      </div>

      <div class="examples-section" v-if="!selectedImage && !caption">
        <h2>示例</h2>
        <p>点击下方图片尝试图像描述功能</p>

        <div class="examples-grid">
          <div v-for="(example, index) in examples" :key="index" class="example-item" @click="selectExampleImage(example.image)">
            <img :src="example.image" :alt="example.alt" />
            <div class="example-overlay">
              <span>点击使用</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分享对话框 -->
    <Dialog v-model:visible="showShareDialog" header="分享结果" :style="{ width: '450px' }" :modal="true">
      <div class="share-options">
        <div class="share-option" @click="shareViaMethod('weixin')">
          <i class="pi pi-comments"></i>
          <span>微信</span>
        </div>
        <div class="share-option" @click="shareViaMethod('weibo')">
          <i class="pi pi-globe"></i>
          <span>微博</span>
        </div>
        <div class="share-option" @click="shareViaMethod('qq')">
          <i class="pi pi-user"></i>
          <span>QQ</span>
        </div>
        <div class="share-option" @click="shareViaMethod('link')">
          <i class="pi pi-link"></i>
          <span>复制链接</span>
        </div>
      </div>
      <div class="share-link-container" v-if="shareLink">
        <InputText v-model="shareLink" class="w-full" readonly />
        <Button icon="pi pi-copy" @click="copyShareLink" />
      </div>
    </Dialog>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import AppNavbar from '@/components/layout/AppNavbar.vue';
import AppFooter from '@/components/layout/AppFooter.vue';
import Button from 'primevue/button';
import ProgressBar from 'primevue/progressbar';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';

const toast = useToast();
const fileInput = ref(null);
const selectedImage = ref(null);
const caption = ref(null);
const isDragging = ref(false);
const isProcessing = ref(false);
const showShareDialog = ref(false);
const shareLink = ref('');

// 示例图片
const examples = [
  {
    image: '/images/examples/landscape.jpg',
    alt: '自然风景'
  },
  {
    image: '/images/examples/city.jpg',
    alt: '城市街景'
  },
  {
    image: '/images/examples/food.jpg',
    alt: '美食'
  },
  {
    image: '/images/examples/people.jpg',
    alt: '人物'
  }
];

// 触发文件选择对话框
const triggerFileInput = () => {
  fileInput.value.click();
};

// 处理文件选择
const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    validateAndProcessImage(file);
  }
};

// 拖放相关处理
const handleDragOver = (event) => {
  isDragging.value = true;
};

const handleDragLeave = (event) => {
  isDragging.value = false;
};

const handleDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file) {
    validateAndProcessImage(file);
  }
};

// 验证并处理图片
const validateAndProcessImage = (file) => {
  // 检查文件类型
  if (!file.type.match('image.*')) {
    toast.add({ severity: 'error', summary: '不支持的文件类型', detail: '请上传图片文件 (JPG, PNG, GIF)', life: 3000 });
    return;
  }

  // 检查文件大小
  if (file.size > 10 * 1024 * 1024) { // 10MB
    toast.add({ severity: 'error', summary: '文件过大', detail: '图片大小不能超过10MB', life: 3000 });
    return;
  }

  // 创建预览
  const reader = new FileReader();
  reader.onload = (e) => {
    selectedImage.value = e.target.result;
  };
  reader.readAsDataURL(file);
};

// 清除图片
const clearImage = () => {
  selectedImage.value = null;
  caption.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

// 生成描述
const generateCaption = async () => {
  if (!selectedImage.value) return;

  isProcessing.value = true;
  caption.value = null;

  try {
    // 此处模拟API调用，实际项目中应替换为真实API
    await new Promise(resolve => setTimeout(resolve, 2000));

    // 模拟结果
    caption.value = {
      description: '这张图片展示了一个风景优美的自然场景，有青翠的山脉和平静的湖水。画面中有几棵高大的松树在前景中，远处的山峰被薄雾笼罩。天空中飘着几朵白云，整个画面给人一种宁静祥和的感觉。',
      tags: ['自然', '山脉', '湖泊', '树木', '风景', '户外', '宁静'],
      confidence: 0.92
    };

    toast.add({ severity: 'success', summary: '成功', detail: '描述生成完成', life: 3000 });
  } catch (error) {
    toast.add({ severity: 'error', summary: '错误', detail: '描述生成失败，请重试', life: 3000 });
    console.error('生成描述时出错:', error);
  } finally {
    isProcessing.value = false;
  }
};

// 选择示例图片
const selectExampleImage = (imagePath) => {
  selectedImage.value = imagePath;
};

// 复制描述
const copyDescription = () => {
  if (!caption.value) return;

  navigator.clipboard.writeText(caption.value.description)
    .then(() => {
      toast.add({ severity: 'info', summary: '成功', detail: '描述已复制到剪贴板', life: 2000 });
    })
    .catch((err) => {
      console.error('无法复制文本: ', err);
      toast.add({ severity: 'error', summary: '错误', detail: '复制失败，请手动复制', life: 3000 });
    });
};

// 下载结果
const downloadResults = () => {
  if (!caption.value) return;

  const content = `
图像描述结果
=============

详细描述:
${caption.value.description}

图像标签:
${caption.value.tags.join(', ')}

置信度:
${Math.round(caption.value.confidence * 100)}%

生成时间: ${new Date().toLocaleString()}
  `;

  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'image-description-result.txt';
  a.click();
  URL.revokeObjectURL(url);

  toast.add({ severity: 'info', summary: '成功', detail: '结果已下载', life: 2000 });
};

// 分享
const shareViaMethod = (method) => {
  // 生成分享链接 (实际应用中可能需要调用后端API)
  shareLink.value = `https://yoursite.com/share/image-caption/${Date.now()}`;

  switch (method) {
    case 'weixin':
      toast.add({ severity: 'info', summary: '分享', detail: '微信分享功能已启动', life: 2000 });
      break;
    case 'weibo':
      toast.add({ severity: 'info', summary: '分享', detail: '微博分享功能已启动', life: 2000 });
      break;
    case 'qq':
      toast.add({ severity: 'info', summary: '分享', detail: 'QQ分享功能已启动', life: 2000 });
      break;
    case 'link':
      copyShareLink();
      break;
  }
};

// 复制分享链接
const copyShareLink = () => {
  navigator.clipboard.writeText(shareLink.value)
    .then(() => {
      toast.add({ severity: 'info', summary: '成功', detail: '链接已复制到剪贴板', life: 2000 });
    })
    .catch((err) => {
      console.error('无法复制链接: ', err);
      toast.add({ severity: 'error', summary: '错误', detail: '复制失败，请手动复制', life: 3000 });
    });
};

onMounted(() => {
  // 页面初始化逻辑
});
</script>

<style lang="scss" scoped>
.image-captioning-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--surface-ground);
}

.page-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;

  h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: var(--text-color);
  }

  .page-description {
    font-size: 1.1rem;
    color: var(--text-color-secondary);
    max-width: 600px;
    margin: 0 auto;
  }
}

.captioning-section {
  background: var(--surface-card);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  margin-bottom: 2rem;
}

.upload-area {
  border: 2px dashed var(--surface-border);
  border-radius: 8px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
  background-color: var(--surface-section);
  margin-bottom: 1.5rem;

  &.drag-over {
    border-color: var(--primary-color);
    background-color: rgba(var(--primary-color-rgb), 0.05);
  }

  &.has-image {
    border-style: solid;
    padding: 0;
    overflow: hidden;
  }
}

.upload-placeholder {
  .pi-cloud-upload {
    font-size: 3rem;
    color: var(--text-color-secondary);
    margin-bottom: 1rem;
  }

  p {
    margin: 0.5rem 0;
    color: var(--text-color-secondary);
  }

  .browse-link {
    color: var(--primary-color);
    cursor: pointer;
    text-decoration: underline;

    &:hover {
      color: var(--primary-600);
    }
  }

  .hint {
    font-size: 0.9rem;
    opacity: 0.7;
    margin-top: 1rem;
  }
}

.hidden-input {
  display: none;
}

.image-preview {
  position: relative;
  width: 100%;
  height: 400px;

  .preview-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .image-actions {
    position: absolute;
    top: 10px;
    right: 10px;
  }
}

.action-controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.results-area {
  margin-top: 2rem;

  h2 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: var(--text-color);
    font-size: 1.8rem;
  }
}

.caption-card {
  background: var(--surface-section);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;

  h3 {
    color: var(--text-color);
    margin-bottom: 0.5rem;
    font-size: 1.2rem;
  }

  p {
    color: var(--text-color);
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;

  .caption-tag {
    margin-right: 0;
  }
}

.confidence-bar {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  .confidence-label {
    font-weight: bold;
    color: var(--primary-color);
  }
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.examples-section {
  margin-top: 3rem;
  text-align: center;

  h2 {
    margin-bottom: 0.5rem;
    color: var(--text-color);
  }

  p {
    color: var(--text-color-secondary);
    margin-bottom: 1.5rem;
  }
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.example-item {
  position: relative;
  height: 150px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
  }

  .example-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;

    span {
      color: white;
      font-weight: bold;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      background: rgba(0, 0, 0, 0.5);
    }
  }

  &:hover {
    img {
      transform: scale(1.1);
    }

    .example-overlay {
      opacity: 1;
    }
  }
}

.share-options {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.share-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: var(--surface-hover);
  }

  i {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: var(--primary-color);
  }

  span {
    font-size: 0.9rem;
  }
}

.share-link-container {
  display: flex;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .page-content {
    padding: 1rem;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .captioning-section {
    padding: 1.5rem;
  }

  .upload-area {
    padding: 2rem 1rem;
  }

  .action-controls {
    flex-direction: column;
  }

  .share-options {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
