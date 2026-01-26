<template>
  <div class="scenario-select">
    <!-- 全局加载遮罩 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner">⏳</div>
        <h2 class="loading-text">{{ loadingText }}</h2>
      </div>
    </div>

    <div class="header">
      <h1 class="title">TalkArena</h1>
      <p class="subtitle">选择你的挑战场景</p>
    </div>

    <div v-if="scenarios.length === 0 && !isLoading" class="loading-placeholder">
      <div class="loading-spinner">⏳</div>
      <p>加载场景中...</p>
    </div>

    <div v-else class="scenarios-grid">
      <div
        v-for="scenario in scenarios"
        :key="scenario.id"
        class="scenario-card"
        :class="{ 'disabled': isLoading }"
        @click="selectScenario(scenario)"
      >
        <div class="card-icon">{{ getIcon(scenario.type) }}</div>
        <h3 class="card-title">{{ scenario.name }}</h3>
        <p class="card-desc">{{ scenario.description }}</p>
      </div>
    </div>

    <div class="footer">
      <p>© 2024 TalkArena - 社交技能训练模拟器</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { useGameStore } from '@/store/game'

const router = useRouter()
const gameStore = useGameStore()
const scenarios = ref([])
const isLoading = ref(false)
const loadingText = ref('加载中...')

const iconMap = {
  shandong_dinner: '🍺',
  negotiation: '💼',
  debate: '⚖️',
  interview: '👔'
}

const getIcon = (type) => iconMap[type] || '🎯'

const selectScenario = async (scenario) => {
  if (isLoading.value) return

  gameStore.scenarioId = scenario.id
  gameStore.scenarioName = scenario.name

  // 如果是山东饭局，进入配置页；否则直接开始
  if (scenario.type === 'shandong_dinner') {
    router.push('/config')
  } else {
    isLoading.value = true
    loadingText.value = '正在创建会话...'
    try {
      await gameStore.createSession(scenario.id)
      router.push('/chat')
    } catch (error) {
      alert('创建会话失败，请重试')
    } finally {
      isLoading.value = false
    }
  }
}

onMounted(async () => {
  isLoading.value = true
  loadingText.value = '加载场景列表...'
  try {
    scenarios.value = await api.getScenarios()
  } catch (error) {
    console.error('获取场景列表失败:', error)
    alert('获取场景列表失败，请刷新重试')
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.scenario-select {
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
  animation: fadeIn 0.8s ease;
}

.title {
  font-size: 4rem;
  font-weight: 700;
  color: white;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  width: 100%;
  animation: fadeIn 1s ease 0.3s both;
}

.scenario-card {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.scenario-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.scenario-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.card-desc {
  color: #6b7280;
  font-size: 1rem;
  line-height: 1.5;
}

.footer {
  margin-top: 3rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Loading 遮罩层样式 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.loading-content {
  text-align: center;
  color: white;
}

.loading-spinner {
  font-size: 4rem;
  animation: spin 2s linear infinite;
}

.loading-text {
  margin-top: 1rem;
  font-size: 1.5rem;
  font-weight: 500;
}

.loading-placeholder {
  text-align: center;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  animation: fadeIn 0.5s ease;
}

.loading-placeholder .loading-spinner {
  font-size: 3rem;
  margin-bottom: 1rem;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
