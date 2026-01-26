<template>
  <div class="chat-page">
    <!-- 顶部视觉舞台 -->
    <div class="visual-stage" v-html="visualStageHTML"></div>

    <div class="chat-container">
      <!-- 左侧控制栏 -->
      <aside class="sidebar">
        <button class="rescue-btn" @click="onRescue" :disabled="loading">
          🆘 救场
        </button>
        <button class="end-btn" @click="onEndGame" :disabled="loading">
          🏁 结束对决
        </button>

        <!-- 气场侧边栏 -->
        <div class="aura-sidebar">
          <div class="aura-item pancake">
            <div class="aura-icon">🥞</div>
            <div class="aura-label">煎饼</div>
            <div class="aura-value">{{ gameStore.pancakeScore }}</div>
          </div>
          <div class="aura-item garlic">
            <div class="aura-icon">🧄</div>
            <div class="aura-label">大蒜</div>
            <div class="aura-value">{{ gameStore.garlicScore }}</div>
          </div>
          <div class="round-info">第 {{ gameStore.round }} 轮</div>
        </div>
      </aside>

      <!-- 主对话区 -->
      <main class="chat-main">
        <!-- 判定反馈框 -->
        <div
          v-if="critiqueVisible"
          class="critique-box"
          :class="critiqueType"
        >
          <div class="critique-icon">{{ critiqueIcon }}</div>
          <div class="critique-content">
            <div class="critique-title">{{ critiqueTitle }}</div>
            <div class="critique-text">{{ critiqueText }}</div>
          </div>
        </div>

        <!-- 聊天记录区 -->
        <div class="chat-history" ref="chatHistory">
          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="message"
            :class="msg.role"
          >
            <div class="message-avatar">
              <span v-if="msg.role === 'user'">👤</span>
              <span v-else>{{ msg.avatar || '🤖' }}</span>
            </div>
            <div class="message-content">
              <div class="message-name">{{ msg.name || (msg.role === 'user' ? '你' : 'AI') }}</div>
              <!-- 如果正在流式加载，显示加载动画 -->
              <div v-if="msg.streaming" class="typing-indicator">
                <span></span><span></span><span></span>
              </div>
              <!-- 否则显示消息内容 -->
              <div v-else class="message-text">{{ msg.content }}</div>
              <div v-if="msg.judgment" class="message-judgment">
                <span :class="msg.judgment.type">
                  {{ msg.judgment.type === 'pancake' ? '🥞' : '🧄' }}
                  {{ msg.judgment.comment }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区 -->
        <div class="input-area">
          <button
            class="mic-btn"
            @click="toggleMic"
            title="语音输入"
          >
            🎙️
          </button>
          <input
            v-model="userInput"
            type="text"
            class="message-input"
            placeholder="输入你的回答..."
            @keyup.enter="sendMessage"
            :disabled="loading"
          />
          <button
            class="send-btn"
            @click="sendMessage"
            :disabled="loading || !userInput.trim()"
          >
            发送
          </button>
        </div>
      </main>
    </div>

    <!-- 语音输入弹窗（占位） -->
    <div v-if="showMicModal" class="mic-modal">
      <div class="mic-modal-content">
        <h3>语音输入</h3>
        <p>语音功能开发中...</p>
        <button @click="showMicModal = false">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useGameStore } from '@/store/game'
import api from '@/api'

const router = useRouter()
const route = useRoute()
const gameStore = useGameStore()

const userInput = ref('')
const loading = ref(false)
const showMicModal = ref(false)
const critiqueVisible = ref(false)
const critiqueType = ref('') // 'pancake' or 'garlic'
const critiqueTitle = ref('')
const critiqueText = ref('')
const critiqueIcon = ref('')
const chatHistory = ref(null)

const messages = computed(() => gameStore.conversationHistory)

const visualStageHTML = computed(() => {
  // 简化版视觉舞台
  return `
    <div class="stage-content">
      <h2 class="stage-title">${gameStore.scenarioName || '对话中'}</h2>
      <div class="stage-characters">
        <div class="character-avatar">👨‍💼</div>
      </div>
    </div>
  `
})

const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value) return

  const message = userInput.value.trim()
  userInput.value = ''
  loading.value = true
  critiqueVisible.value = false

  try {
    const response = await gameStore.sendMessage(message, (event) => {
      // 实时滚动到底部
      nextTick(() => {
        scrollToBottom()
      })

      // 当收到最终响应时显示判定
      if (event.stage === 'final' && event.data.judgment) {
        showCritique(event.data.judgment)
      }
    })

    // 滚动到底部
    await nextTick()
    scrollToBottom()

  } catch (error) {
    console.error('发送消息失败:', error)
    alert('发送失败，请重试')
  } finally {
    loading.value = false
  }
}

const showCritique = (judgment) => {
  critiqueType.value = judgment.type
  critiqueTitle.value = judgment.type === 'pancake' ? '回答得体！' : '踩雷了！'
  critiqueText.value = judgment.comment
  critiqueIcon.value = judgment.type === 'pancake' ? '🥞' : '🧄'
  critiqueVisible.value = true

  // 3秒后自动隐藏
  setTimeout(() => {
    critiqueVisible.value = false
  }, 3000)
}

const onRescue = async () => {
  if (loading.value) return

  loading.value = true
  try {
    const rescue = await api.requestRescue(gameStore.sessionId)
    alert(`💡 救场建议：\n${rescue.suggestion}\n\n📝 说明：\n${rescue.explanation}`)
  } catch (error) {
    console.error('救场失败:', error)
    alert('救场失败，请重试')
  } finally {
    loading.value = false
  }
}

const onEndGame = async () => {
  if (!confirm('确定要结束对决吗？')) return

  if (loading.value) return

  loading.value = true
  try {
    await gameStore.endSession()

    // 通过路由参数传递配置，避免store数据丢失
    router.push({
      path: '/report',
      query: {
        config: JSON.stringify(gameStore.sessionConfig || {})
      }
    })
  } catch (error) {
    console.error('结束游戏失败:', error)
    alert('操作失败，请重试')
  } finally {
    loading.value = false
  }
}

const toggleMic = () => {
  showMicModal.value = true
}

const scrollToBottom = () => {
  if (chatHistory.value) {
    chatHistory.value.scrollTop = chatHistory.value.scrollHeight
  }
}

onMounted(async () => {
  // 如果没有 sessionId，返回首页
  if (!gameStore.sessionId) {
    router.push('/')
    return
  }

  await nextTick()
  scrollToBottom()
})
</script>

<style scoped>
.chat-page {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

/* 视觉舞台 */
.visual-stage {
  background: white;
  padding: 1.5rem;
  border-bottom: 2px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stage-content {
  text-align: center;
}

.stage-title {
  color: #1f2937;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.stage-characters {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.character-avatar {
  font-size: 4rem;
  animation: float 3s ease-in-out infinite;
}

/* 聊天容器 */
.chat-container {
  flex: 1;
  display: flex;
  gap: 1rem;
  padding: 1rem;
  overflow: hidden;
}

/* 侧边栏 */
.sidebar {
  width: 150px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rescue-btn,
.end-btn {
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.rescue-btn {
  background: #d32f2f;
  color: white;
}

.rescue-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.4);
}

.rescue-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.end-btn {
  background: white;
  color: #333;
}

.end-btn:hover:not(:disabled) {
  background: #f5f5f5;
}

.end-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 气场侧边栏 */
.aura-sidebar {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.aura-item {
  text-align: center;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 0.5rem;
}

.aura-item.pancake {
  background: #FFD700;
}

.aura-item.garlic {
  background: #9333ea;
}

.aura-icon {
  font-size: 2rem;
}

.aura-label {
  font-size: 0.875rem;
  color: white;
  font-weight: 600;
  margin-top: 0.25rem;
}

.aura-value {
  font-size: 1.5rem;
  color: white;
  font-weight: 700;
}

.round-info {
  text-align: center;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  font-weight: 600;
}

/* 主对话区 */
.chat-main {
  flex: 1;
  background: white;
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 判定反馈框 */
.critique-box {
  padding: 1rem;
  margin: 1rem 1rem 0;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: slideDown 0.3s ease;
}

.critique-box.pancake {
  background: #FFD700;
  color: white;
}

.critique-box.garlic {
  background: #9333ea;
  color: white;
}

.critique-icon {
  font-size: 2.5rem;
}

.critique-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.critique-text {
  font-size: 0.875rem;
}

/* 聊天历史 */
.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.message {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  animation: fadeIn 0.3s ease;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #d32f2f;
}

.message-content {
  max-width: 70%;
}

.message.user .message-content {
  text-align: right;
}

.message-name {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.message-text {
  background: #f3f4f6;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  line-height: 1.5;
}

.message.user .message-text {
  background: #d32f2f;
  color: white;
}

.message-judgment {
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

.message-judgment .pancake {
  color: #f59e0b;
  font-weight: 600;
}

.message-judgment .garlic {
  color: #9333ea;
  font-weight: 600;
}

/* 加载指示器 */
.typing-indicator {
  display: flex;
  gap: 0.25rem;
  padding: 0.5rem;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #999;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

/* 输入区 */
.input-area {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.mic-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: white;
  border-radius: 50%;
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.mic-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.message-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 2rem;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.message-input:focus {
  border-color: #d32f2f;
}

.send-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 2rem;
  background: #d32f2f;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 语音弹窗 */
.mic-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.mic-modal-content {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
}

/* 动画 */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}
</style>
