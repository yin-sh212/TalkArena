<template>
  <div class="report-page">
    <div class="report-container">
      <div class="report-card">
        <!-- 左侧面板 -->
        <div class="left-panel">
          <div class="header-section">
            <h1 class="main-title">局后复盘</h1>
            <p class="scene-info">在"{{ sceneName }}"中的表现</p>
          </div>

          <div class="medal-badge" :style="{ background: medalColor }">
            {{ medal }}
          </div>

          <div class="radar-chart">
            <canvas ref="radarCanvas"></canvas>
          </div>

          <div class="scores-grid">
            <div class="score-box">
              <span class="score-label">圆滑度</span>
              <b class="score-value">{{ scores.oily }}</b>
            </div>
            <div class="score-box">
              <span class="score-label">亲和力</span>
              <b class="score-value">{{ scores.friendliness }}</b>
            </div>
            <div class="score-box">
              <span class="score-label">逻辑性</span>
              <b class="score-value">{{ scores.logic }}</b>
            </div>
            <div class="score-box">
              <span class="score-label">幽默感</span>
              <b class="score-value">{{ scores.humor }}</b>
            </div>
            <div class="score-box">
              <span class="score-label">懂规矩</span>
              <b class="score-value">{{ scores.respect }}</b>
            </div>
          </div>
        </div>

        <!-- 右侧面板 -->
        <div class="right-panel">
          <div class="content-section">
            <h3 class="section-title">
              <span>💬</span> 综合点评
            </h3>
            <p class="section-text">{{ summary }}</p>
          </div>

          <div class="content-section">
            <h3 class="section-title">
              <span>🎭</span> NPC 内心 OS
            </h3>
            <div class="npc-os-list">
              <div v-for="npc in npcOsList" :key="npc.name" class="os-row">
                <div class="npc-avatar">{{ npc.avatar }}</div>
                <div class="os-bubble">
                  <b>{{ npc.name }}</b>
                  {{ npc.os }}
                </div>
              </div>
            </div>
          </div>

          <div class="suggestion-box">
            <b class="suggestion-title">💡 改进建议</b>
            <p class="suggestion-text">{{ suggestion }}</p>
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <button class="btn btn-primary" @click="playAgain">
          🔄 再来一局
        </button>
        <button class="btn btn-secondary" @click="backToHome">
          🏠 返回首页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useGameStore } from '@/store/game'
import { Chart, RadarController, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js'

// 注册Chart.js组件
Chart.register(RadarController, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

const router = useRouter()
const route = useRoute()
const gameStore = useGameStore()
const radarCanvas = ref(null)

// 从路由参数或store获取配置
const getSessionConfig = () => {
  // 优先从路由参数读取
  if (route.query.config) {
    try {
      return JSON.parse(route.query.config)
    } catch (e) {
      console.error('[ReportView] 解析路由配置失败:', e)
    }
  }
  // 回退到store
  return gameStore.sessionConfig || {}
}

const sessionConfig = ref(getSessionConfig())

// 使用computed动态获取配置数据
const sceneName = computed(() => {
  return sessionConfig.value?.scene || '商务宴请'
})

// 获取真实的NPC列表（从配置中），使用computed确保响应式
const realNpcList = computed(() => {
  if (sessionConfig.value?.members && sessionConfig.value.members.length > 0) {
    return sessionConfig.value.members
  }
  // 默认值
  return [
    { name: '王总', avatar: '👔' },
    { name: '李总', avatar: '👨‍💼' },
    { name: '小赵', avatar: '👩' }
  ]
})

// 模拟数据（实际应该从API获取）
const medal = ref('饭局操盘手')
const scores = ref({
  oily: 75,
  friendliness: 68,
  logic: 82,
  humor: 55,
  respect: 70
})
const summary = ref('表现中规中矩，在商务场合展现出了基本的职场素养。逻辑性表现突出，能够有条理地陈述观点，但幽默感略显不足，建议在适当时机加入轻松话题活跃气氛。整体气场稳定，没有明显失误，但也缺乏出彩表现，属于安全型选手。')

// 使用真实的NPC信息，但OS还是模拟的
const npcOsList = computed(() => {
  return realNpcList.value.map((npc, index) => ({
    name: npc.name,
    avatar: npc.avatar || '👤',
    os: index === 0 ? '这小子说话还算靠谱，就是太正经了点，没啥意思。' :
        index === 1 ? '逻辑清楚，但缺少人情味，不太好深交。' :
        '比我强多了，至少不会踩雷...'
  }))
})

const suggestion = ref('建议在保持专业的同时，适当增加一些轻松话题。可以在敬酒环节加入一些得体的玩笑，拉近与对方的距离。记住：商务宴请不仅是谈生意，更是建立信任的过程。')

onMounted(() => {
  setTimeout(() => {
    initRadarChart()
  }, 100)
})

const medalColor = computed(() => {
  const avg = (scores.value.oily + scores.value.friendliness + scores.value.logic + scores.value.humor + scores.value.respect) / 5
  if (avg >= 85) return '#e74c3c'
  if (avg >= 70) return '#f39c12'
  if (avg >= 50) return '#3498db'
  return '#95a5a6'
})

let chartInstance = null

const initRadarChart = () => {
  if (!radarCanvas.value) return

  const ctx = radarCanvas.value.getContext('2d')

  if (chartInstance) {
    chartInstance.destroy()
  }

  chartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['圆滑度', '亲和力', '逻辑性', '幽默感', '懂规矩'],
      datasets: [{
        label: '你的表现',
        data: [
          scores.value.oily,
          scores.value.friendliness,
          scores.value.logic,
          scores.value.humor,
          scores.value.respect
        ],
        backgroundColor: 'rgba(74, 93, 202, 0.2)',
        borderColor: 'rgba(74, 93, 202, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(74, 93, 202, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(74, 93, 202, 1)'
      }]
    },
    options: {
      scales: {
        r: {
          angleLines: { display: true },
          suggestedMin: 0,
          suggestedMax: 100
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  })
}

const playAgain = () => {
  router.push('/')
}

const backToHome = () => {
  router.push('/')
}
</script>

<style scoped>
.report-page {
  width: 100%;
  min-height: 100vh;
  background: #2c313c;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.report-container {
  max-width: 1000px;
  width: 100%;
}

.report-card {
  background: white;
  border-radius: 24px;
  display: flex;
  overflow: hidden;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
  animation: fadeIn 0.8s ease;
}

/* 左侧面板 */
.left-panel {
  flex: 1;
  padding: 40px;
  border-right: 1px dashed #eee;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header-section {
  text-align: left;
  width: 100%;
  margin-bottom: 20px;
}

.main-title {
  margin: 0;
  font-size: 26px;
  color: #1a1a1a;
  font-weight: 700;
}

.scene-info {
  color: #666;
  font-size: 13px;
  margin-top: 4px;
}

.medal-badge {
  color: white;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 800;
  font-size: 18px;
  transform: rotate(-3deg);
  box-shadow: 4px 8px 15px rgba(231, 76, 60, 0.3);
  margin: 20px 0;
  cursor: default;
  transition: all 0.3s;
}

.medal-badge:hover {
  transform: rotate(-3deg) scale(1.05);
}

.radar-chart {
  width: 280px;
  height: 280px;
  margin: 10px 0;
}

.scores-grid {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 20px;
  gap: 10px;
}

.score-box {
  flex: 1;
  background: #f8f9fa;
  padding: 10px 5px;
  border-radius: 10px;
  text-align: center;
  border: 1px solid #eee;
  transition: all 0.3s;
}

.score-box:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.score-label {
  display: block;
  font-size: 11px;
  color: #666;
  margin-bottom: 4px;
}

.score-value {
  font-size: 15px;
  color: #4a5dca;
}

/* 右侧面板 */
.right-panel {
  flex: 1.3;
  padding: 40px;
  background: #fafafa;
  display: flex;
  flex-direction: column;
  gap: 15px;
  overflow-y: auto;
  max-height: 90vh;
}

.content-section {
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  animation: slideIn 0.5s ease;
}

.section-title {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #4a5dca;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-text {
  margin: 0;
  font-size: 13px;
  line-height: 1.6;
  color: #333;
}

.npc-os-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.os-row {
  display: flex;
  gap: 10px;
  align-items: flex-start;
}

.npc-avatar {
  font-size: 24px;
  flex-shrink: 0;
}

.os-bubble {
  background: #f3f4f6;
  padding: 10px;
  border-radius: 8px;
  font-size: 13px;
  line-height: 1.5;
  color: #333;
  flex: 1;
}

.os-bubble b {
  display: block;
  margin-bottom: 4px;
  color: #4a5dca;
}

.suggestion-box {
  background: #fffbe6;
  border: 1px solid #ffe58f;
  padding: 15px;
  border-radius: 14px;
  transition: all 0.3s;
  animation: slideIn 0.7s ease;
}

.suggestion-box:hover {
  background: #fff9db;
}

.suggestion-title {
  display: block;
  font-size: 14px;
  margin-bottom: 8px;
  color: #856404;
  border-bottom: 1px solid rgba(133, 100, 4, 0.1);
  padding-bottom: 3px;
}

.suggestion-text {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
  color: #666;
}

/* 底部按钮 */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #d32f2f;
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.4);
}

.btn-secondary {
  background: white;
  color: #d32f2f;
  border: 2px solid #d32f2f;
}

.btn-secondary:hover {
  background: #d32f2f;
  color: white;
}

/* 动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .report-card {
    flex-direction: column;
  }

  .left-panel {
    border-right: none;
    border-bottom: 1px dashed #eee;
  }

  .right-panel {
    max-height: none;
  }
}
</style>
