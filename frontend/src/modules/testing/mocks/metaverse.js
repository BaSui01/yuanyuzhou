import { rest } from 'msw'

export const metaverseHandlers = [
  // 获取元宇宙空间列表
  rest.get('/api/metaverse/spaces', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        spaces: [
          {
            id: 'space-1',
            name: '创意广场',
            description: '一个充满创意的开放空间',
            thumbnail: '/img/spaces/creative-plaza.svg',
            capacity: 50,
            currentUsers: 12,
            tags: ['创意', '社交', '开放']
          },
          {
            id: 'space-2',
            name: '科技中心',
            description: '探索最新科技的虚拟展示厅',
            thumbnail: '/img/spaces/tech-center.svg',
            capacity: 30,
            currentUsers: 8,
            tags: ['科技', '展示', '教育']
          },
          {
            id: 'space-3',
            name: '冥想花园',
            description: '一个放松身心的宁静空间',
            thumbnail: '/img/spaces/zen-garden.svg',
            capacity: 20,
            currentUsers: 5,
            tags: ['放松', '自然', '冥想']
          }
        ],
        total: 3
      })
    )
  }),

  // 获取单个元宇宙空间详情
  rest.get('/api/metaverse/spaces/:spaceId', (req, res, ctx) => {
    const { spaceId } = req.params

    return res(
      ctx.status(200),
      ctx.json({
        id: spaceId,
        name: '创意广场',
        description: '一个充满创意的开放空间，用户可以在这里展示自己的作品、交流创意想法。',
        thumbnail: '/img/spaces/creative-plaza.svg',
        capacity: 50,
        currentUsers: 12,
        creator: {
          id: 'user-123',
          username: '创意达人',
          avatar: '/avatars/creator.svg'
        },
        createdAt: '2023-05-10T14:30:00Z',
        tags: ['创意', '社交', '开放'],
        features: ['语音聊天', '3D画廊', '互动白板'],
        entryPoints: [
          { x: 0, y: 0, z: 0, name: '主入口' },
          { x: 100, y: 0, z: 100, name: '展览厅入口' }
        ]
      })
    )
  }),

  // 获取用户的虚拟形象
  rest.get('/api/metaverse/avatar', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        id: 'avatar-123',
        model: 'humanoid-1',
        skin: 'default',
        hair: {
          style: 'short',
          color: '#000000'
        },
        eyes: {
          shape: 'round',
          color: '#6B8E23'
        },
        outfit: {
          top: 'tshirt-blue',
          bottom: 'jeans-black',
          shoes: 'sneakers-white'
        },
        accessories: ['glasses-round'],
        animations: ['wave', 'dance', 'sit'],
        lastUpdated: '2023-08-15T10:20:00Z'
      })
    )
  }),

  // 获取虚拟物品列表
  rest.get('/api/metaverse/items', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        items: [
          {
            id: 'item-1',
            name: '太空头盔',
            description: '一个未来风格的太空头盔',
            thumbnail: '/img/items/space-helmet.svg',
            price: 500,
            category: 'accessories',
            rarity: 'rare'
          },
          {
            id: 'item-2',
            name: '霓虹翅膀',
            description: '会发光的霓虹风格翅膀',
            thumbnail: '/img/items/neon-wings.svg',
            price: 1200,
            category: 'accessories',
            rarity: 'epic'
          },
          {
            id: 'item-3',
            name: '悬浮滑板',
            description: '可以在虚拟世界中使用的悬浮滑板',
            thumbnail: '/img/items/hoverboard.svg',
            price: 800,
            category: 'transportation',
            rarity: 'uncommon'
          }
        ],
        total: 3
      })
    )
  }),

  // 获取元宇宙活动列表
  rest.get('/api/metaverse/events', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        events: [
          {
            id: 'event-1',
            title: '虚拟音乐节',
            description: '一场跨越现实的沉浸式音乐体验',
            thumbnail: '/img/events/music-festival.svg',
            startTime: new Date(Date.now() + 86400000).toISOString(),
            endTime: new Date(Date.now() + 86400000 + 10800000).toISOString(),
            location: {
              spaceId: 'space-1',
              name: '创意广场',
              coordinates: { x: 100, y: 10, z: 100 }
            },
            capacity: 200,
            registeredUsers: 87,
            host: {
              id: 'user-456',
              username: '活动策划师',
              avatar: '/avatars/event-planner.svg'
            }
          },
          {
            id: 'event-2',
            title: 'AI技术讲座',
            description: '探索人工智能的前沿技术和应用',
            thumbnail: '/img/events/ai-talk.svg',
            startTime: new Date(Date.now() + 172800000).toISOString(),
            endTime: new Date(Date.now() + 172800000 + 7200000).toISOString(),
            location: {
              spaceId: 'space-2',
              name: '科技中心',
              coordinates: { x: 50, y: 0, z: 50 }
            },
            capacity: 100,
            registeredUsers: 42,
            host: {
              id: 'user-789',
              username: '科技专家',
              avatar: '/avatars/tech-expert.svg'
            }
          }
        ],
        total: 2
      })
    )
  })
]
