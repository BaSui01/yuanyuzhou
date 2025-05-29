<template>
    <div class="team-page">
        <AppNavbar />

        <main class="main-content">
            <!-- 页面头部 -->
            <section class="page-header">
                <div class="container mx-auto px-6 py-20">
                    <div class="text-center">
                        <h1 class="page-title">团队成员</h1>
                        <p class="page-subtitle">认识推动元宇宙社交空间发展的优秀团队</p>
                    </div>
                </div>
            </section>

            <!-- 核心团队 -->
            <section class="core-team py-20">
                <div class="container mx-auto px-6">
                    <h2 class="section-title text-center mb-16">核心团队</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        <div
                            v-for="member in coreTeam"
                            :key="member.id"
                            class="team-card"
                        >
                            <div class="member-avatar">
                                <img :src="member.avatar" :alt="member.name" v-if="member.avatar">
                                <div v-else class="avatar-placeholder">
                                    <i class="pi pi-user text-4xl"></i>
                                </div>
                            </div>
                            <div class="member-info">
                                <h3 class="member-name">{{ member.name }}</h3>
                                <p class="member-title">{{ member.title }}</p>
                                <p class="member-description">{{ member.description }}</p>
                                <div class="member-skills">
                                    <span
                                        v-for="skill in member.skills"
                                        :key="skill"
                                        class="skill-tag"
                                    >
                                        {{ skill }}
                                    </span>
                                </div>
                                <div class="member-social">
                                    <a
                                        v-for="social in member.socials"
                                        :key="social.platform"
                                        :href="social.url"
                                        :title="social.platform"
                                        class="social-link"
                                        target="_blank"
                                    >
                                        <i :class="`pi ${social.icon}`"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 团队统计 -->
            <section class="team-stats py-20 bg-black/20">
                <div class="container mx-auto px-6">
                    <h2 class="section-title text-center mb-16">团队力量</h2>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
                        <div class="stat-card">
                            <div class="stat-number">{{ teamStats.totalMembers }}+</div>
                            <div class="stat-label">团队成员</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{{ teamStats.departments }}</div>
                            <div class="stat-label">部门</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{{ teamStats.avgExperience }}年</div>
                            <div class="stat-label">平均经验</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{{ teamStats.satisfaction }}%</div>
                            <div class="stat-label">团队满意度</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 加入我们 -->
            <section class="join-us py-20">
                <div class="container mx-auto px-6 text-center">
                    <h2 class="section-title mb-8">加入我们</h2>
                    <p class="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
                        我们正在寻找充满激情的人才加入我们的团队，一起打造未来的虚拟社交体验
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <button class="btn-primary">
                            <i class="pi pi-briefcase mr-2"></i>
                            查看职位
                        </button>
                        <button class="btn-ghost">
                            <i class="pi pi-envelope mr-2"></i>
                            投递简历
                        </button>
                    </div>
                </div>
            </section>
        </main>

        <AppFooter />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

// 核心团队数据
const coreTeam = ref([
    {
        id: 1,
        name: '张三',
        title: '创始人 & CEO',
        description: '拥有15年互联网行业经验，曾在多家知名科技公司担任高级管理职位',
        skills: ['战略规划', '产品管理', '团队领导'],
        avatar: null,
        socials: [
            { platform: 'LinkedIn', icon: 'pi-linkedin', url: '#' },
            { platform: 'Twitter', icon: 'pi-twitter', url: '#' }
        ]
    },
    {
        id: 2,
        name: '李四',
        title: '技术总监 & CTO',
        description: '前Google工程师，专注于AI和机器学习领域，拥有多项技术专利',
        skills: ['AI技术', '架构设计', '技术管理'],
        avatar: null,
        socials: [
            { platform: 'GitHub', icon: 'pi-github', url: '#' },
            { platform: 'LinkedIn', icon: 'pi-linkedin', url: '#' }
        ]
    },
    {
        id: 3,
        name: '王五',
        title: '产品总监',
        description: '资深产品经理，曾主导多个千万级用户产品的设计和开发',
        skills: ['产品设计', '用户体验', '数据分析'],
        avatar: null,
        socials: [
            { platform: 'LinkedIn', icon: 'pi-linkedin', url: '#' }
        ]
    }
])

// 团队统计数据
const teamStats = ref({
    totalMembers: 50,
    departments: 6,
    avgExperience: 8,
    satisfaction: 95
})
</script>

<style lang="scss" scoped>
// 团队页面样式
.team-page {
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

    .team-card {
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

        .member-avatar {
            width: 120px;
            height: 120px;
            margin: 0 auto 1.5rem;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #06b6d4;

            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }

            .avatar-placeholder {
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.1);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #9ca3af;
            }
        }

        .member-name {
            font-size: 1.5rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0.5rem;
        }

        .member-title {
            font-size: 1rem;
            color: #06b6d4;
            font-weight: 500;
            margin-bottom: 1rem;
        }

        .member-description {
            color: #d1d5db;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }

        .member-skills {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
            margin-bottom: 1.5rem;

            .skill-tag {
                background: rgba(6, 182, 212, 0.2);
                color: #06b6d4;
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.875rem;
                font-weight: 500;
            }
        }

        .member-social {
            display: flex;
            gap: 1rem;
            justify-content: center;

            .social-link {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.1);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #9ca3af;
                transition: all 0.3s ease;

                &:hover {
                    background: #06b6d4;
                    color: #ffffff;
                    transform: scale(1.1);
                }
            }
        }
    }

    .team-stats {
        .stat-card {
            text-align: center;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;

            &:hover {
                background: rgba(255, 255, 255, 0.08);
                transform: translateY(-5px);
            }

            .stat-number {
                font-size: 2.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #06b6d4, #8b5cf6);
                background-clip: text;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            }

            .stat-label {
                color: #d1d5db;
                font-weight: 500;
            }
        }
    }

    .btn-primary, .btn-ghost {
        padding: 1rem 2rem;
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        text-decoration: none;
    }

    .btn-primary {
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        color: white;

        &:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(6, 182, 212, 0.3);
        }
    }

    .btn-ghost {
        background: transparent;
        border: 2px solid rgba(255, 255, 255, 0.2);
        color: #d1d5db;

        &:hover {
            border-color: #06b6d4;
            color: #06b6d4;
            background: rgba(6, 182, 212, 0.1);
        }
    }
}
</style>
