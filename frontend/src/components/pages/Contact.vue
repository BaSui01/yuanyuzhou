<template>
    <div class="contact-page">
        <AppNavbar />

        <main class="main-content">
            <!-- 页面头部 -->
            <section class="page-header">
                <div class="container mx-auto px-6 py-20">
                    <div class="text-center">
                        <h1 class="page-title">联系我们</h1>
                        <p class="page-subtitle">与我们取得联系，我们期待为您提供帮助</p>
                    </div>
                </div>
            </section>

            <!-- 联系方式 -->
            <section class="contact-info py-20">
                <div class="container mx-auto px-6">
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
                        <div class="contact-card">
                            <div class="contact-icon">
                                <i class="pi pi-phone text-4xl text-cyan-400"></i>
                            </div>
                            <h3>电话咨询</h3>
                            <p class="contact-detail">
                                <a href="tel:400-123-4567">400-123-4567</a>
                            </p>
                            <p class="contact-desc">工作日 9:00-18:00</p>
                        </div>

                        <div class="contact-card">
                            <div class="contact-icon">
                                <i class="pi pi-envelope text-4xl text-purple-400"></i>
                            </div>
                            <h3>邮箱联系</h3>
                            <p class="contact-detail">
                                <a href="mailto:contact@metaverse.com">contact@metaverse.com</a>
                            </p>
                            <p class="contact-desc">24小时内回复</p>
                        </div>

                        <div class="contact-card">
                            <div class="contact-icon">
                                <i class="pi pi-map-marker text-4xl text-green-400"></i>
                            </div>
                            <h3>公司地址</h3>
                            <p class="contact-detail">北京市朝阳区科技园区</p>
                            <p class="contact-desc">欢迎预约拜访</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 联系表单 -->
            <section class="contact-form py-20 bg-black/20">
                <div class="container mx-auto px-6">
                    <div class="max-w-4xl mx-auto">
                        <div class="text-center mb-12">
                            <h2 class="section-title">发送消息</h2>
                            <p class="text-xl text-gray-300">填写下面的表单，我们会尽快回复您</p>
                        </div>

                        <form @submit.prevent="submitForm" class="contact-form-grid">
                            <div class="form-group">
                                <label for="name">姓名 *</label>
                                <input type="text" id="name" v-model="form.name" required class="form-input"
                                    placeholder="请输入您的姓名">
                            </div>

                            <div class="form-group">
                                <label for="email">邮箱 *</label>
                                <input type="email" id="email" v-model="form.email" required class="form-input"
                                    placeholder="请输入您的邮箱">
                            </div>

                            <div class="form-group">
                                <label for="phone">电话</label>
                                <input type="tel" id="phone" v-model="form.phone" class="form-input"
                                    placeholder="请输入您的电话">
                            </div>

                            <div class="form-group">
                                <label for="company">公司</label>
                                <input type="text" id="company" v-model="form.company" class="form-input"
                                    placeholder="请输入您的公司名称">
                            </div>

                            <div class="form-group full-width">
                                <label for="subject">主题 *</label>
                                <input type="text" id="subject" v-model="form.subject" required class="form-input"
                                    placeholder="请输入消息主题">
                            </div>

                            <div class="form-group full-width">
                                <label for="message">消息内容 *</label>
                                <textarea id="message" v-model="form.message" required rows="6" class="form-input"
                                    placeholder="请详细描述您的需求或问题"></textarea>
                            </div>

                            <div class="form-group full-width">
                                <button type="submit" class="submit-btn" :disabled="submitting">
                                    <i class="pi pi-send mr-2"></i>
                                    {{ submitting ? '发送中...' : '发送消息' }}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </section>

            <!-- 地图区域 -->
            <section class="map-section py-20">
                <div class="container mx-auto px-6">
                    <h2 class="section-title text-center mb-12">找到我们</h2>
                    <div class="map-container">
                        <div class="map-placeholder">
                            <i class="pi pi-map text-6xl text-gray-500"></i>
                            <p class="text-gray-500 mt-4">地图加载中...</p>
                            <p class="text-sm text-gray-600 mt-2">北京市朝阳区科技园区</p>
                        </div>
                    </div>
                </div>
            </section>
        </main>

        <AppFooter />
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

// 表单数据
const form = reactive({
    name: '',
    email: '',
    phone: '',
    company: '',
    subject: '',
    message: ''
})

// 提交状态
const submitting = ref(false)

// 提交表单
const submitForm = async () => {
    submitting.value = true

    try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 2000))

        // 这里添加实际的表单提交逻辑
        console.log('表单提交:', form)

        // 重置表单
        Object.keys(form).forEach(key => {
            form[key] = ''
        })

        alert('消息发送成功！我们会尽快回复您。')
    } catch (error) {
        console.error('提交失败:', error)
        alert('发送失败，请稍后再试。')
    } finally {
        submitting.value = false
    }
}
</script>

<style lang="scss" scoped>
.contact-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #ffffff;

    .main-content {
        padding-top: 80px;
    }

    .page-header {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.1));
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);

        .page-title {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #06b6d4, #8b5cf6);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;

            @media (max-width: 768px) {
                font-size: 2.5rem;
            }
        }

        .page-subtitle {
            font-size: 1.25rem;
            color: #d1d5db;
            max-width: 600px;
            margin: 0 auto;
        }
    }

    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;

        @media (max-width: 768px) {
            font-size: 2rem;
        }
    }

    .contact-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;

        &:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }

        .contact-icon {
            width: 80px;
            height: 80px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
        }

        h3 {
            font-size: 1.5rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 1rem;
        }

        .contact-detail {
            font-size: 1.125rem;
            margin-bottom: 0.5rem;

            a {
                color: #06b6d4;
                text-decoration: none;
                transition: color 0.3s ease;

                &:hover {
                    color: #67e8f9;
                }
            }
        }

        .contact-desc {
            color: #9ca3af;
            font-size: 0.875rem;
        }
    }

    .contact-form-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;

        @media (max-width: 768px) {
            grid-template-columns: 1fr;
        }

        .form-group {
            &.full-width {
                grid-column: span 2;

                @media (max-width: 768px) {
                    grid-column: span 1;
                }
            }

            label {
                display: block;
                font-weight: 500;
                color: #d1d5db;
                margin-bottom: 0.5rem;
            }

            .form-input {
                width: 100%;
                padding: 1rem;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 0.5rem;
                color: #ffffff;
                font-size: 1rem;
                transition: all 0.3s ease;

                &:focus {
                    outline: none;
                    border-color: #06b6d4;
                    background: rgba(255, 255, 255, 0.08);
                    box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
                }

                &::placeholder {
                    color: #9ca3af;
                }
            }

            textarea.form-input {
                resize: vertical;
                min-height: 120px;
            }
        }

        .submit-btn {
            background: linear-gradient(135deg, #06b6d4, #8b5cf6);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 0.5rem;
            font-weight: 500;
            font-size: 1.125rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;

            &:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(6, 182, 212, 0.3);
            }

            &:disabled {
                opacity: 0.7;
                cursor: not-allowed;
            }
        }
    }

    .map-container {
        height: 400px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        overflow: hidden;

        .map-placeholder {
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #9ca3af;
        }
    }
}
</style>
