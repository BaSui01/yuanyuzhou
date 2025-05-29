<template>
    <div class="privacy-page">
        <AppNavbar />

        <main class="main-content">
            <!-- 页面头部 -->
            <section class="page-header">
                <div class="container mx-auto px-6 py-20">
                    <div class="text-center">
                        <h1 class="page-title">隐私政策</h1>
                        <p class="page-subtitle">了解我们如何保护您的个人信息</p>
                        <p class="last-updated">最后更新时间：2024年{{ currentMonth }}月{{ currentDay }}日</p>
                    </div>
                </div>
            </section>

            <!-- 政策内容 -->
            <section class="policy-content py-20">
                <div class="container mx-auto px-6">
                    <div class="max-w-4xl mx-auto">
                        <!-- 概述 -->
                        <div class="policy-section">
                            <h2>概述</h2>
                            <p>
                                元宇宙社交空间（以下简称"我们"）致力于保护用户的隐私和个人信息安全。
                                本隐私政策详细说明了我们如何收集、使用、存储和保护您的个人信息。
                            </p>
                            <p>
                                使用我们的服务即表示您同意本隐私政策。如果您不同意本政策的任何条款，
                                请勿使用我们的服务。
                            </p>
                        </div>

                        <!-- 信息收集 -->
                        <div class="policy-section">
                            <h2>我们收集的信息</h2>
                            <h3>1. 您主动提供的信息</h3>
                            <ul>
                                <li>注册账户时提供的基本信息（用户名、邮箱、电话号码等）</li>
                                <li>个人资料信息（头像、昵称、个人介绍等）</li>
                                <li>与AI助手的对话内容</li>
                                <li>反馈和客服沟通记录</li>
                            </ul>

                            <h3>2. 自动收集的信息</h3>
                            <ul>
                                <li>设备信息（设备型号、操作系统、浏览器类型等）</li>
                                <li>使用数据（访问时间、使用功能、操作记录等）</li>
                                <li>网络信息（IP地址、网络类型等）</li>
                                <li>位置信息（在您授权的情况下）</li>
                            </ul>
                        </div>

                        <!-- 信息使用 -->
                        <div class="policy-section">
                            <h2>信息使用目的</h2>
                            <div class="purpose-grid">
                                <div class="purpose-card">
                                    <i class="pi pi-cog"></i>
                                    <h4>服务提供</h4>
                                    <p>提供和维护我们的服务功能</p>
                                </div>
                                <div class="purpose-card">
                                    <i class="pi pi-chart-line"></i>
                                    <h4>服务改进</h4>
                                    <p>分析使用数据以改进产品和用户体验</p>
                                </div>
                                <div class="purpose-card">
                                    <i class="pi pi-shield"></i>
                                    <h4>安全保障</h4>
                                    <p>检测和防范安全威胁和欺诈行为</p>
                                </div>
                                <div class="purpose-card">
                                    <i class="pi pi-envelope"></i>
                                    <h4>沟通联系</h4>
                                    <p>发送重要通知和产品更新信息</p>
                                </div>
                            </div>
                        </div>

                        <!-- 信息共享 -->
                        <div class="policy-section">
                            <h2>信息共享</h2>
                            <p>我们不会出售、交易或租赁您的个人信息给第三方。在以下情况下，我们可能会共享您的信息：</p>
                            <ul>
                                <li><strong>获得您的明确同意</strong></li>
                                <li><strong>法律要求：</strong>遵守法律法规、法院命令或政府要求</li>
                                <li><strong>服务提供商：</strong>与可信的第三方服务提供商共享，以提供技术支持</li>
                                <li><strong>业务转让：</strong>在公司合并、收购或资产转让的情况下</li>
                            </ul>
                        </div>

                        <!-- 数据安全 -->
                        <div class="policy-section">
                            <h2>数据安全</h2>
                            <div class="security-measures">
                                <div class="security-item">
                                    <i class="pi pi-lock text-cyan-400"></i>
                                    <div>
                                        <h4>加密传输</h4>
                                        <p>使用SSL/TLS加密技术保护数据传输</p>
                                    </div>
                                </div>
                                <div class="security-item">
                                    <i class="pi pi-database text-purple-400"></i>
                                    <div>
                                        <h4>安全存储</h4>
                                        <p>采用行业标准的加密技术存储数据</p>
                                    </div>
                                </div>
                                <div class="security-item">
                                    <i class="pi pi-eye text-green-400"></i>
                                    <div>
                                        <h4>访问控制</h4>
                                        <p>严格控制内部人员的数据访问权限</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 您的权利 -->
                        <div class="policy-section">
                            <h2>您的权利</h2>
                            <p>您对您的个人信息享有以下权利：</p>
                            <div class="rights-grid">
                                <div class="right-item">
                                    <h4>访问权</h4>
                                    <p>查看我们持有的您的个人信息</p>
                                </div>
                                <div class="right-item">
                                    <h4>更正权</h4>
                                    <p>更正不准确或不完整的信息</p>
                                </div>
                                <div class="right-item">
                                    <h4>删除权</h4>
                                    <p>要求删除您的个人信息</p>
                                </div>
                                <div class="right-item">
                                    <h4>反对权</h4>
                                    <p>反对某些处理活动</p>
                                </div>
                            </div>
                        </div>

                        <!-- Cookie政策 -->
                        <div class="policy-section">
                            <h2>Cookie政策</h2>
                            <p>
                                我们使用Cookie和类似技术来改善您的使用体验。Cookie是存储在您设备上的小型文本文件，
                                帮助我们记住您的偏好设置和提供个性化服务。
                            </p>
                            <p>您可以通过浏览器设置控制Cookie的使用，但请注意这可能会影响某些功能的正常使用。</p>
                        </div>

                        <!-- 联系我们 -->
                        <div class="policy-section">
                            <h2>联系我们</h2>
                            <p>如果您对本隐私政策有任何疑问或需要行使您的权利，请通过以下方式联系我们：</p>
                            <div class="contact-info">
                                <div class="contact-item">
                                    <i class="pi pi-envelope"></i>
                                    <span>邮箱：privacy@metaverse.com</span>
                                </div>
                                <div class="contact-item">
                                    <i class="pi pi-phone"></i>
                                    <span>电话：400-123-4567</span>
                                </div>
                                <div class="contact-item">
                                    <i class="pi pi-map-marker"></i>
                                    <span>地址：北京市朝阳区科技园区</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>

        <AppFooter />
    </div>
</template>

<script setup>
import { computed } from 'vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

// 当前日期
const currentDate = new Date()
const currentMonth = computed(() => currentDate.getMonth() + 1)
const currentDay = computed(() => currentDate.getDate())
</script>

<style lang="scss" scoped>
.privacy-page {
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
            margin-bottom: 0.5rem;
        }

        .last-updated {
            color: #9ca3af;
            font-size: 0.875rem;
        }
    }

    .policy-content {
        .policy-section {
            margin-bottom: 3rem;

            h2 {
                font-size: 2rem;
                font-weight: 700;
                color: #06b6d4;
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid rgba(6, 182, 212, 0.3);
            }

            h3 {
                font-size: 1.5rem;
                font-weight: 600;
                color: #ffffff;
                margin: 2rem 0 1rem;
            }

            h4 {
                font-size: 1.25rem;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 0.5rem;
            }

            p {
                color: #d1d5db;
                line-height: 1.8;
                margin-bottom: 1rem;
                font-size: 1.1rem;
            }

            ul, ol {
                color: #d1d5db;
                margin-left: 2rem;
                margin-bottom: 1rem;

                li {
                    margin-bottom: 0.5rem;
                    line-height: 1.6;
                }
            }

            strong {
                color: #06b6d4;
                font-weight: 600;
            }
        }

        .purpose-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;

            .purpose-card {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 1rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 1.5rem;
                text-align: center;
                transition: all 0.3s ease;

                &:hover {
                    background: rgba(255, 255, 255, 0.08);
                    transform: translateY(-5px);
                }

                i {
                    font-size: 2.5rem;
                    color: #06b6d4;
                    margin-bottom: 1rem;
                    display: block;
                }

                h4 {
                    margin-bottom: 0.5rem;
                }

                p {
                    margin: 0;
                    font-size: 0.875rem;
                }
            }
        }

        .security-measures {
            .security-item {
                display: flex;
                align-items: flex-start;
                gap: 1rem;
                margin-bottom: 1.5rem;
                padding: 1rem;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 0.5rem;
                border: 1px solid rgba(255, 255, 255, 0.1);

                i {
                    font-size: 1.5rem;
                    margin-top: 0.25rem;
                }

                h4 {
                    margin-bottom: 0.5rem;
                }

                p {
                    margin: 0;
                    color: #9ca3af;
                }
            }
        }

        .rights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;

            .right-item {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 0.5rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 1rem;

                h4 {
                    color: #06b6d4;
                    margin-bottom: 0.5rem;
                }

                p {
                    margin: 0;
                    font-size: 0.875rem;
                    color: #9ca3af;
                }
            }
        }

        .contact-info {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem;
            margin-top: 1.5rem;

            .contact-item {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1rem;

                &:last-child {
                    margin-bottom: 0;
                }

                i {
                    color: #06b6d4;
                    font-size: 1.2rem;
                }

                span {
                    color: #d1d5db;
                }
            }
        }
    }
}

@media (max-width: 768px) {
    .privacy-page {
        .policy-content {
            .purpose-grid {
                grid-template-columns: 1fr;
            }

            .rights-grid {
                grid-template-columns: 1fr;
            }
        }
    }
}
</style>
