import { createRouter, createWebHistory } from 'vue-router'

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

export default router
