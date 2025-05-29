import { rest } from 'msw'

export const authHandlers = [
  // 用户登录
  rest.post('/api/auth/login', (req, res, ctx) => {
    const { email, password } = req.body

    // 模拟简单的登录验证
    if (email === 'test@example.com' && password === 'password') {
      return res(
        ctx.delay(500),
        ctx.status(200),
        ctx.json({
          token: 'mock-jwt-token-xyz',
          user: {
            id: 'user-123',
            username: '测试用户',
            email: 'test@example.com',
            avatar: '/avatars/default-user.svg',
            role: 'user'
          },
          expiresIn: 3600
        })
      )
    } else {
      return res(
        ctx.delay(500),
        ctx.status(401),
        ctx.json({
          message: '邮箱或密码错误'
        })
      )
    }
  }),

  // 用户注册
  rest.post('/api/auth/register', (req, res, ctx) => {
    const { email, username, password } = req.body

    // 模拟邮箱已存在的情况
    if (email === 'test@example.com') {
      return res(
        ctx.delay(500),
        ctx.status(409),
        ctx.json({
          message: '该邮箱已被注册'
        })
      )
    }

    return res(
      ctx.delay(800),
      ctx.status(201),
      ctx.json({
        message: '注册成功',
        user: {
          id: 'new-user-' + Date.now(),
          username,
          email,
          avatar: '/avatars/default-user.svg',
          role: 'user',
          createdAt: new Date().toISOString()
        }
      })
    )
  }),

  // 重置密码
  rest.post('/api/auth/reset-password', (req, res, ctx) => {
    const { email } = req.body

    return res(
      ctx.delay(500),
      ctx.status(200),
      ctx.json({
        message: '密码重置邮件已发送，请检查您的邮箱'
      })
    )
  }),

  // 验证令牌
  rest.post('/api/auth/verify-token', (req, res, ctx) => {
    const { token } = req.body

    if (token === 'mock-jwt-token-xyz') {
      return res(
        ctx.status(200),
        ctx.json({
          valid: true,
          user: {
            id: 'user-123',
            username: '测试用户',
            email: 'test@example.com'
          }
        })
      )
    } else {
      return res(
        ctx.status(401),
        ctx.json({
          valid: false,
          message: '无效或过期的令牌'
        })
      )
    }
  }),

  // 刷新令牌
  rest.post('/api/auth/refresh-token', (req, res, ctx) => {
    const { refreshToken } = req.body

    return res(
      ctx.status(200),
      ctx.json({
        token: 'new-mock-jwt-token-xyz',
        refreshToken: 'new-refresh-token',
        expiresIn: 3600
      })
    )
  }),

  // 退出登录
  rest.post('/api/auth/logout', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        message: '成功退出登录'
      })
    )
  })
]
