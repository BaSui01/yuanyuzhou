import { rest } from 'msw'

export const userHandlers = [
  // 获取用户资料
  rest.get('/api/user/profile', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        id: 'user-123',
        username: '测试用户',
        email: 'test@example.com',
        avatar: '/avatars/default-user.svg',
        createdAt: '2023-01-15T08:30:00Z',
        bio: '这是一个测试用户账号',
        preferences: {
          theme: 'dark',
          language: 'zh-CN',
          notifications: true
        }
      })
    )
  }),

  // 更新用户资料
  rest.put('/api/user/profile', (req, res, ctx) => {
    const { username, bio } = req.body

    return res(
      ctx.delay(500),
      ctx.status(200),
      ctx.json({
        id: 'user-123',
        username: username || '测试用户',
        email: 'test@example.com',
        avatar: '/avatars/default-user.svg',
        bio: bio || '这是一个测试用户账号',
        updatedAt: new Date().toISOString()
      })
    )
  }),

  // 获取用户设置
  rest.get('/api/user/settings', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        theme: 'dark',
        language: 'zh-CN',
        notifications: {
          email: true,
          push: true,
          messages: true,
          updates: false
        },
        privacy: {
          profileVisibility: 'public',
          activityVisibility: 'friends'
        }
      })
    )
  }),

  // 获取好友列表
  rest.get('/api/user/friends', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        friends: [
          {
            id: 'user-456',
            username: '张三',
            avatar: '/avatars/user1.svg',
            status: 'online'
          },
          {
            id: 'user-789',
            username: '李四',
            avatar: '/avatars/user2.svg',
            status: 'offline'
          }
        ],
        total: 2
      })
    )
  }),

  // 获取通知
  rest.get('/api/user/notifications', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        notifications: [
          {
            id: 'notif-1',
            type: 'friend_request',
            content: '王五请求添加您为好友',
            isRead: false,
            createdAt: new Date(Date.now() - 3600000).toISOString()
          },
          {
            id: 'notif-2',
            type: 'system',
            content: '欢迎使用我们的平台！',
            isRead: true,
            createdAt: new Date(Date.now() - 86400000).toISOString()
          }
        ],
        unreadCount: 1,
        total: 2
      })
    )
  })
]
