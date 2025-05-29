import { rest } from 'msw'

export const aiHandlers = [
  // 处理 AI 聊天请求
  rest.post('/api/ai/chat', (req, res, ctx) => {
    // 模拟延迟
    return res(
      ctx.delay(1000),
      ctx.status(200),
      ctx.json({
        message: `这是一个模拟回复。您发送的消息是: "${req.body.message}"`,
        timestamp: new Date().toISOString()
      })
    )
  }),

  // AI 模型列表
  rest.get('/api/ai/models', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        models: [
          { id: 'gpt-3.5', name: 'GPT-3.5', description: '通用AI模型' },
          { id: 'gpt-4', name: 'GPT-4', description: '高级AI模型' },
          { id: 'claude-2', name: 'Claude 2', description: '专注于对话的AI' }
        ]
      })
    )
  }),

  // 语音转文本
  rest.post('/api/ai/stt', (req, res, ctx) => {
    return res(
      ctx.delay(800),
      ctx.status(200),
      ctx.json({
        text: '这是从语音识别出的文本内容。',
        confidence: 0.92
      })
    )
  }),

  // 文本转语音
  rest.post('/api/ai/tts', (req, res, ctx) => {
    return res(
      ctx.delay(800),
      ctx.status(200),
      ctx.json({
        audioUrl: 'https://example.com/tts-audio.mp3',
        duration: 3.5
      })
    )
  })
]
