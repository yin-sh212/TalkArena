import { defineStore } from 'pinia'

export const useLoadingStore = defineStore('loading', {
  state: () => ({
    global: false,
    message: '加载中...'
  }),

  actions: {
    show(message = '加载中...') {
      this.global = true
      this.message = message
    },

    hide() {
      this.global = false
      this.message = '加载中...'
    }
  }
})
