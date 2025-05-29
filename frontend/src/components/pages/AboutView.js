import { ref, reactive } from 'vue'

export default function useAboutPage() {
    // 页面数据
    const pageData = reactive({
        companyInfo: {
            name: '元宇宙社交空间',
            founded: '2022',
            mission: '通过先进的AI技术和沉浸式3D体验，为用户创造充满无限可能的数字世界',
            vision: '成为全球领先的AI驱动虚拟社交平台'
        },
        timeline: [
            {
                year: '2024',
                title: '平台正式发布',
                description: '元宇宙社交空间正式上线，为用户提供全新的AI社交体验',
                achievements: ['用户突破10万', '日活跃用户5万+', '获得A轮融资']
            },
            {
                year: '2023',
                title: '技术研发阶段',
                description: '核心AI技术研发完成，3D虚拟环境构建系统搭建',
                achievements: ['AI模型训练完成', '3D引擎开发', '语音交互系统']
            },
            {
                year: '2022',
                title: '公司成立',
                description: '元宇宙社交空间项目启动，核心团队组建完成',
                achievements: ['团队组建', '天使轮融资', '技术架构设计']
            }
        ],
        coreValues: [
            {
                icon: 'pi-heart',
                color: 'red-400',
                title: '以人为本',
                description: '始终把用户体验和情感需求放在首位，用技术服务于人性',
                details: [
                    '用户体验至上',
                    '情感化交互设计',
                    '个性化服务定制'
                ]
            },
            {
                icon: 'pi-lightbulb',
                color: 'yellow-400',
                title: '创新驱动',
                description: '持续探索前沿技术，为用户带来突破性的社交体验',
                details: [
                    'AI技术创新',
                    '3D虚拟现实',
                    '语音交互革新'
                ]
            },
            {
                icon: 'pi-shield',
                color: 'green-400',
                title: '安全可信',
                description: '保护用户隐私和数据安全，建立可信赖的虚拟社交环境',
                details: [
                    '端到端加密',
                    '隐私保护机制',
                    '安全认证体系'
                ]
            }
        ],
        statistics: {
            users: 100000,
            countries: 50,
            dailyActive: 50000,
            satisfaction: 98
        }
    })

    // 加载状态
    const loading = ref(false)
    const error = ref(null)

    // 加载页面数据
    const loadPageData = async () => {
        loading.value = true
        error.value = null

        try {
            // 模拟API调用
            await new Promise(resolve => setTimeout(resolve, 500))

            // 这里可以添加实际的API调用
            // const response = await apiService.getAboutPageData()
            // pageData.value = response.data

            console.log('关于我们页面数据加载完成')
        } catch (err) {
            error.value = err.message || '数据加载失败'
            console.error('加载页面数据失败:', err)
        } finally {
            loading.value = false
        }
    }

    // 格式化数字
    const formatNumber = (num) => {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M'
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K'
        }
        return num.toString()
    }

    // 跳转到联系页面
    const goToContact = () => {
        // 这里可以使用路由跳转
        console.log('跳转到联系页面')
    }

    // 下载公司资料
    const downloadCompanyProfile = () => {
        console.log('下载公司资料')
    }

    // 分享页面
    const sharePage = (platform) => {
        const url = window.location.href
        const title = '关于元宇宙社交空间'

        const shareUrls = {
            weibo: `https://service.weibo.com/share/share.php?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`,
            wechat: 'javascript:void(0)', // 微信分享需要特殊处理
            qq: `https://connect.qq.com/widget/shareqq/index.html?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`
        }

        if (platform === 'wechat') {
            // 显示微信分享二维码
            console.log('显示微信分享二维码')
            return
        }

        const shareUrl = shareUrls[platform]
        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400')
        }
    }

    return {
        // 数据
        pageData,
        loading,
        error,

        // 方法
        loadPageData,
        formatNumber,
        goToContact,
        downloadCompanyProfile,
        sharePage
    }
}
