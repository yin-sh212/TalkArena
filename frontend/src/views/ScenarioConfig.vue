<template>
  <div class="config-page">
    <!-- 全屏加载遮罩 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner">⏳</div>
        <h2 class="loading-text">正在准备饭局...</h2>
        <p class="loading-subtitle">AI正在生成开场白，请稍候</p>
      </div>
    </div>

    <div class="header">
      <h1 class="title">山东人的饭桌</h1>
      <p class="subtitle">选择你的饭局战场</p>
    </div>

    <div class="content">
      <!-- 场景选择区 -->
      <div class="section">
        <h2 class="section-title">选择场景</h2>
        <div class="scene-cards">
          <div
            v-for="scene in scenes"
            :key="scene.name"
            class="scene-card"
            :class="{ active: selectedScene === scene.name }"
            @click="selectScene(scene)"
          >
            {{ scene.name }}
          </div>
        </div>
        <div class="scene-desc">{{ sceneDescription }}</div>
      </div>

      <!-- 饭局成员区 -->
      <div class="section">
        <h2 class="section-title">
          选择你的对手 <span class="ai-badge">AI扮演</span>
        </h2>
        <p class="section-subtitle">这些角色由AI扮演，他们会在酒桌上向你发起挑战</p>
        <div class="roster-container">
          <div
            v-for="member in members"
            :key="member.name"
            class="roster-card"
            :class="{ selected: selectedMembers.includes(member.name) }"
            @click="toggleMemberSelection(member)"
          >
            <div class="roster-avatar">{{ member.avatar }}</div>
            <div class="roster-name">{{ member.name }}</div>
            <div class="roster-role">{{ member.role }}</div>
            <div class="roster-personality">{{ member.personality }}</div>
            <div v-if="selectedMembers.includes(member.name)" class="selected-badge">✓</div>
          </div>
        </div>

        <div class="action-buttons">
          <button class="btn btn-secondary" @click="regenerateMembers">
            🔄 随机换人
          </button>
          <button class="btn btn-secondary" @click="editMembers">
            ✏️ 手动编辑
          </button>
        </div>
      </div>

      <!-- 开始按钮 -->
      <div class="bottom-actions">
        <button class="btn btn-primary btn-large" @click="startGame" :disabled="isLoading">
          🍺 入席开整
        </button>
        <button class="btn btn-link" @click="backToScenes" :disabled="isLoading">
          ← 返回场景选择
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/store/game'

const router = useRouter()
const gameStore = useGameStore()

// 场景配置
const scenes = ref([
  {
    name: '家庭聚会',
    description: '亲戚满座，长幼尊卑分明，既要应酬长辈，又得照顾晚辈，滴水不漏才是王道。'
  },
  {
    name: '单位聚餐',
    description: '上下级层次分明，话题要谨慎，敬酒要得体，一言一行都是职场风向标。'
  },
  {
    name: '商务宴请',
    description: '高端局，主陪副陪分清，话权要巧妙抓住，让话题走在你的节奏。'
  },
  {
    name: '同学聚会',
    description: '看似随意实则暗流涌动，吹牛要有度，敬酒要真诚，别让同学看扁了。'
  },
  {
    name: '招待客户',
    description: '你是东道主，既要展现诚意，又要把控节奏，让客户满意而归才是目标。'
  }
])

const selectedScene = ref('商务宴请')
const sceneDescription = ref('高端局，主陪副陪分清，话权要巧妙抓住，让话题走在你的节奏。')

// 饭局成员选择状态
const selectedMembers = ref([])

// 加载状态
const isLoading = ref(false)

// 饭局成员
const members = ref([
  {
    avatar: '👨‍💼',
    name: '王局长',
    role: '主陪·局领导·威压全场',
    personality: '深谙官场礼仪，对座次、敬酒顺序极为讲究，用话语掌控节奏…'
  },
  {
    avatar: '👔',
    name: '李总',
    role: '副陪·商界老板·副驾驶',
    personality: '能言善辩，擅长活跃气氛，总能找到话题接茬，能左右逢源…'
  },
  {
    avatar: '👩',
    name: '小赵',
    role: '实诚晚辈·新手',
    personality: '性格耿直但缺乏饭局经验，善于"酒桌踩雷"，为了替领导撑面子…'
  }
])

// 预定义的成员库
const memberPool = [
  {
    avatar: '👨‍💼',
    name: '王局长',
    role: '主陪·局领导·威压全场',
    personality: '深谙官场礼仪，对座次、敬酒顺序极为讲究，用话语掌控节奏…'
  },
  {
    avatar: '👔',
    name: '李总',
    role: '副陪·商界老板·副驾驶',
    personality: '能言善辩，擅长活跃气氛，总能找到话题接茬，能左右逢源…'
  },
  {
    avatar: '👩',
    name: '小赵',
    role: '实诚晚辈·新手',
    personality: '性格耿直但缺乏饭局经验，善于"酒桌踩雷"，为了替领导撑面子…'
  },
  {
    avatar: '👴',
    name: '大舅',
    role: '主陪·家族长辈·德高望重',
    personality: '鲁中地区长辈，极讲规矩，擅长情感绑架和逻辑劝酒，热情但强势…'
  },
  {
    avatar: '👨‍🏫',
    name: '张教授',
    role: '文化人·斯文败类',
    personality: '表面儒雅，实则精明，用典故和文化来压人，话里有话…'
  },
  {
    avatar: '👨‍💻',
    name: '老刘',
    role: '老同学·混得好的',
    personality: '成功人士派头十足，喜欢炫耀，话题总绕到自己的成就上…'
  }
]

const selectScene = (scene) => {
  selectedScene.value = scene.name
  sceneDescription.value = scene.description
}

const toggleMemberSelection = (member) => {
  const index = selectedMembers.value.indexOf(member.name)
  if (index === -1) {
    selectedMembers.value.push(member.name)
  } else {
    selectedMembers.value.splice(index, 1)
  }
}

const regenerateMembers = () => {
  // 从成员池中随机选择3个不同的成员
  const shuffled = [...memberPool].sort(() => 0.5 - Math.random())
  members.value = shuffled.slice(0, 3)
  // 清空选择状态
  selectedMembers.value = []
}

const editMembers = () => {
  alert('手动编辑功能开发中...')
}

const startGame = async () => {
  try {
    // 检查是否有选择成员
    if (selectedMembers.value.length === 0) {
      alert('请至少选择一位饭局成员')
      return
    }

    // 设置加载状态
    isLoading.value = true

    // 获取选中的成员详细信息
    const selectedMemberDetails = members.value.filter(m =>
      selectedMembers.value.includes(m.name)
    )

    // 创建配置对象
    const config = {
      scene: selectedScene.value,
      description: sceneDescription.value,
      members: selectedMemberDetails
    }

    // 创建会话
    await gameStore.createSession('shandong_dinner', config)

    // 跳转到对话页
    router.push('/chat')
  } catch (error) {
    console.error('创建会话失败:', error)
    alert('创建会话失败，请重试')
  } finally {
    // 无论成功失败，都重置加载状态
    isLoading.value = false
  }
}

const backToScenes = () => {
  router.push('/')
}
</script>

<style scoped>
.config-page {
  width: 100%;
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem;
  padding-bottom: 4rem;
  overflow-y: auto;
  overflow-x: hidden;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
  animation: fadeIn 0.8s ease;
}

.title {
  font-size: 3rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.subtitle {
  font-size: 1.25rem;
  color: #666;
}

.content {
  max-width: 1000px;
  margin: 0 auto;
}

.section {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  margin-bottom: 2rem;
  animation: fadeIn 1s ease;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.ai-badge {
  font-size: 0.75rem;
  background: #d32f2f;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-weight: 500;
}

.section-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
  margin-top: -1rem;
  margin-bottom: 1rem;
  font-style: italic;
}

/* 场景卡片 */
.scene-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.scene-card {
  padding: 1rem;
  background: #f3f4f6;
  border: 2px solid transparent;
  border-radius: 0.75rem;
  text-align: center;
  font-weight: 500;
  color: #1f2937;
  cursor: pointer;
  transition: all 0.3s ease;
}

.scene-card:hover {
  background: #e5e7eb;
  transform: translateY(-2px);
}

.scene-card.active {
  background: #d32f2f;
  color: white;
  border-color: #d32f2f;
  transform: scale(1.05);
}

.scene-desc {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  color: #6b7280;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* 饭局成员 */
.roster-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.roster-card {
  background: #f9fafb;
  border-radius: 1rem;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
  position: relative;
}

.roster-card:hover {
  background: #f3f4f6;
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.roster-card.selected {
  background: #e0e7ff;
  border-color: #d32f2f;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.selected-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #d32f2f;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
}

.roster-avatar {
  font-size: 3rem;
  margin-bottom: 0.75rem;
}

.roster-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.roster-role {
  font-size: 0.85rem;
  color: #d32f2f;
  font-weight: 500;
  margin-bottom: 0.75rem;
}

.roster-personality {
  font-size: 0.9rem;
  color: #6b7280;
  line-height: 1.5;
}

/* 按钮 */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
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

.btn-primary {
  background: #d32f2f;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-large {
  padding: 1rem 2.5rem;
  font-size: 1.25rem;
}

.btn-link {
  background: transparent;
  color: #666;
  border: none;
  font-size: 0.95rem;
}

.btn-link:hover {
  text-decoration: underline;
}

.bottom-actions {
  text-align: center;
  animation: fadeIn 1.2s ease;
}

.bottom-actions .btn-primary {
  margin-bottom: 1rem;
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

/* 全屏加载遮罩 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
}

.loading-content {
  text-align: center;
  color: white;
}

.loading-spinner {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #fff;
}

.loading-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}
</style>
