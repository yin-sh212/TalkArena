import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  // 场景相关
  getScenarios() {
    return api.get('/scenarios/')
  },

  getScenario(scenarioId) {
    return api.get(`/scenarios/${scenarioId}`)
  },

  // 会话相关
  createSession(data) {
    return api.post('/sessions/', data)
  },

  getSession(sessionId) {
    return api.get(`/sessions/${sessionId}`)
  },

  endSession(sessionId) {
    return api.post(`/sessions/${sessionId}/end`)
  },

  // 对话相关
  sendMessage(data) {
    return api.post('/chat/message', data)
  },

  // 流式发送消息
  async sendMessageStream(data, onEvent) {
    const response = await fetch('/api/chat/message/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const text = decoder.decode(value)
      const lines = text.split('\n\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6))
          onEvent(data)
        }
      }
    }
  },

  requestRescue(sessionId) {
    return api.post('/chat/rescue', { session_id: sessionId })
  }
}
