import { createRouter, createWebHistory } from 'vue-router'
import { useLoadingStore } from '@/store/loading'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/ScenarioSelect.vue')
    },
    {
      path: '/config',
      name: 'config',
      component: () => import('@/views/ScenarioConfig.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/ChatView.vue')
    },
    {
      path: '/report',
      name: 'report',
      component: () => import('@/views/ReportView.vue')
    }
  ]
})

// 路由导航守卫 - 添加页面切换 loading
router.beforeEach((to, from, next) => {
  const loadingStore = useLoadingStore()

  // 只在路由真正发生变化时显示 loading
  if (to.path !== from.path) {
    loadingStore.show('页面加载中...')
  }

  next()
})

router.afterEach(() => {
  const loadingStore = useLoadingStore()

  // 路由加载完成后隐藏 loading
  setTimeout(() => {
    loadingStore.hide()
  }, 300) // 延迟 300ms 确保页面渲染完成
})

export default router
