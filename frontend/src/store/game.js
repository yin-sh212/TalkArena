import { defineStore } from 'pinia'
import api from '@/api'

export const useGameStore = defineStore('game', {
  state: () => ({
    sessionId: null,
    scenarioId: null,
    scenarioName: '',
    pancakeScore: 0,
    garlicScore: 0,
    round: 0,
    conversationHistory: [],
    gameStatus: 'idle' // idle, playing, ended
  }),

  actions: {
    async createSession(scenarioId, config = null) {
      try {
        const response = await api.createSession({
          scenario_id: scenarioId,
          config
        })

        this.sessionId = response.session_id
        this.scenarioId = response.scenario_id
        this.pancakeScore = response.pancake_score
        this.garlicScore = response.garlic_score
        this.gameStatus = 'playing'

        return response
      } catch (error) {
        console.error('创建会话失败:', error)
        throw error
      }
    },

    async sendMessage(message) {
      try {
        const response = await api.sendMessage({
          session_id: this.sessionId,
          message,
          message_type: 'text'
        })

        // 更新游戏状态
        this.pancakeScore = response.game_state.pancake_score
        this.garlicScore = response.game_state.garlic_score
        this.round = response.game_state.round

        // 添加到对话历史
        this.conversationHistory.push({
          role: 'user',
          content: message
        })
        this.conversationHistory.push({
          role: 'assistant',
          name: response.npc_name,
          content: response.message,
          judgment: response.judgment
        })

        return response
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
      this.pancakeScore = 0
      this.garlicScore = 0
      this.round = 0
      this.conversationHistory = []
      this.gameStatus = 'idle'
    }
  }
})
