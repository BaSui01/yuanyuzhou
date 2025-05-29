<template>
    <div class="image-analysis-container">
        <div class="page-header">
            <h1>图像分析</h1>
            <p>上传图片并获得AI智能分析结果</p>
        </div>

        <div class="analysis-content">
            <div class="upload-section">
                <div class="upload-area" @click="triggerFileInput" @drop="handleDrop" @dragover.prevent
                    @dragenter.prevent>
                    <i class="pi pi-cloud-upload" style="font-size: 3rem; color: #6c757d;"></i>
                    <p>点击或拖拽图片到此处上传</p>
                    <small>支持 JPG、PNG、GIF 格式，最大 10MB</small>
                </div>
                <input ref="fileInput" type="file" @change="handleFileSelect" accept="image/*" style="display: none;" />
            </div>

            <div v-if="selectedImage" class="image-preview">
                <img :src="selectedImage" alt="预览图片" />
            </div>

            <div v-if="analysisResult" class="analysis-result">
                <h3>分析结果</h3>
                <div class="result-content">
                    {{ analysisResult }}
                </div>
            </div>

            <div v-if="loading" class="loading-state">
                <ProgressSpinner />
                <p>正在分析图片...</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import ProgressSpinner from 'primevue/progressspinner'

const fileInput = ref(null)
const selectedImage = ref(null)
const analysisResult = ref(null)
const loading = ref(false)

const triggerFileInput = () => {
    fileInput.value.click()
}

const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
        processImage(file)
    }
}

const handleDrop = (event) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
        processImage(file)
    }
}

const processImage = (file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
        selectedImage.value = e.target.result
        analyzeImage(file)
    }
    reader.readAsDataURL(file)
}

const analyzeImage = async (file) => {
    loading.value = true
    try {
        // 这里将调用 AI 图像分析 API
        // 暂时使用模拟数据
        await new Promise(resolve => setTimeout(resolve, 2000))
        analysisResult.value = '这是一张风景照片，包含蓝天、白云和绿色植物。图片构图良好，色彩饱满。'
    } catch (error) {
        console.error('图像分析失败:', error)
        analysisResult.value = '分析失败，请重试。'
    } finally {
        loading.value = false
    }
}
</script>

<style lang="scss" scoped>
.image-analysis-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.page-header {
    text-align: center;
    margin-bottom: 30px;

    h1 {
        font-size: 2.5rem;
        margin-bottom: 10px;
        color: #2c3e50;
    }

    p {
        color: #6c757d;
        font-size: 1.1rem;
    }
}

.upload-section {
    margin-bottom: 30px;
}

.upload-area {
    border: 2px dashed #dee2e6;
    border-radius: 8px;
    padding: 40px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
        border-color: #007bff;
        background-color: #f8f9fa;
    }

    p {
        margin: 15px 0 5px;
        font-size: 1.1rem;
        color: #495057;
    }

    small {
        color: #6c757d;
    }
}

.image-preview {
    text-align: center;
    margin-bottom: 30px;

    img {
        max-width: 100%;
        max-height: 400px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
}

.analysis-result {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #007bff;

    h3 {
        margin-top: 0;
        color: #2c3e50;
    }

    .result-content {
        line-height: 1.6;
        color: #495057;
    }
}

.loading-state {
    text-align: center;
    padding: 40px;

    p {
        margin-top: 15px;
        color: #6c757d;
    }
}
</style>
