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

  requestRescue(sessionId) {
    return api.post('/chat/rescue', { session_id: sessionId })
  }
}
