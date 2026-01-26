<template>
  <div id="app">
    <!-- 全局 Loading 组件 -->
    <div v-if="loadingStore.global" class="global-loading">
      <div class="loading-content">
        <div class="loading-spinner">⏳</div>
        <h2 class="loading-text">{{ loadingStore.message }}</h2>
      </div>
    </div>

    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { useLoadingStore } from '@/store/loading'

const loadingStore = useLoadingStore()
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body, html {
  width: 100%;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

#app {
  width: 100vw;
  height: 100vh;
  overflow: auto;
}

/* 全局 Loading 样式 */
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
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
  font-size: 5rem;
  animation: spin 2s linear infinite;
}

.loading-text {
  margin-top: 1rem;
  font-size: 1.5rem;
  font-weight: 500;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
