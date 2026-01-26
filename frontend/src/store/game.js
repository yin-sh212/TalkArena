import { defineStore } from 'pinia'
import api from '@/api'

export const useGameStore = defineStore('game', {
  state: () => ({
    sessionId: null,
    scenarioId: null,
    scenarioName: '',
    sessionConfig: null, // 保存会话配置（场景、角色等）
    pancakeScore: 0,
    garlicScore: 0,
    round: 0,
    conversationHistory: [],
    gameStatus: 'idle' // idle, playing, ended
  }),

  actions: {
    async createSession(scenarioId, config = null) {
      try {
        // 先清空旧的会话状态
        this.resetGame()

        const response = await api.createSession({
          scenario_id: scenarioId,
          config
        })

        this.sessionId = response.session_id
        this.scenarioId = response.scenario_id
        this.sessionConfig = config // 保存配置信息
        this.pancakeScore = response.pancake_score || 0
        this.garlicScore = response.garlic_score || 0
        this.round = 0
        // 保存开场白到对话历史
        this.conversationHistory = response.conversation_history || []
        this.gameStatus = 'playing'

        return response
      } catch (error) {
        console.error('创建会话失败:', error)
        throw error
      }
    },

    async sendMessage(message, onStream) {
      try {
        // 添加用户消息到历史
        this.conversationHistory.push({
          role: 'user',
          content: message
        })

        // 创建AI消息占位符
        const aiMessageIndex = this.conversationHistory.length
        this.conversationHistory.push({
          role: 'assistant',
          name: '',
          content: '',
          judgment: null,
          streaming: true
        })

        let finalResponse = null

        // 使用流式API
        await api.sendMessageStream(
          {
            session_id: this.sessionId,
            message,
            message_type: 'text'
          },
          (event) => {
            if (onStream) {
              onStream(event)
            }

            // 更新AI消息内容 - 响应 orchestrator 的事件
            if (event.stage === 'ai_thinking') {
              // AI开始思考，保持streaming状态
              this.conversationHistory[aiMessageIndex].streaming = true
            } else if (event.stage === 'ai_response') {
              // AI流式生成中，实时更新文本
              if (event.data && event.data.ai_text) {
                this.conversationHistory[aiMessageIndex].content = event.data.ai_text
                this.conversationHistory[aiMessageIndex].streaming = true  // 保持流式状态
              }
            } else if (event.stage === 'complete') {
              // Orchestrator完成生成，显示AI文本
              if (event.data && event.data.ai_text) {
                this.conversationHistory[aiMessageIndex].content = event.data.ai_text
                this.conversationHistory[aiMessageIndex].streaming = false
              }
            } else if (event.stage === 'final') {
              // 最终响应
              finalResponse = event.data
              this.conversationHistory[aiMessageIndex] = {
                role: 'assistant',
                name: event.data.npc_name,
                content: event.data.message,
                judgment: event.data.judgment,
                streaming: false
              }

              // 更新游戏状态
              this.pancakeScore = event.data.game_state.pancake_score
              this.garlicScore = event.data.game_state.garlic_score
              this.round = event.data.game_state.round
            }
          }
        )

        return finalResponse
      } catch (error) {
        console.error('发送消息失败:', error)
        throw error
      }
    },

    async endSession() {
      try {
        await api.endSession(this.sessionId)
        this.gameStatus = 'ended'
      } catch (error) {
        console.error('结束会话失败:', error)
        throw error
      }
    },

    resetGame() {
      this.sessionId = null
      this.scenarioId = null
      this.scenarioName = ''
      this.sessionConfig = null
      this.pancakeScore = 0
      this.garlicScore = 0
      this.round = 0
      this.conversationHistory = []
      this.gameStatus = 'idle'
    }
  }
})
