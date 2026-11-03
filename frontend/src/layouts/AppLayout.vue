<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  DataBoard,
  Monitor,
  DataAnalysis,
  TrendCharts,
  Bell,
  Operation,
  Menu,
  Close,
} from '@element-plus/icons-vue'

const route = useRoute()
const menuOpen = ref(false)
const navigation = [
  { path: '/', title: '设备状态总览', icon: DataBoard, section: '工作台' },
  { path: '/devices', title: '设备管理', icon: Monitor, section: '设备中心' },
  { path: '/analysis', title: '数据分析', icon: DataAnalysis, section: '设备中心' },
  { path: '/predictions', title: '故障预测', icon: TrendCharts, section: '智能运维' },
  { path: '/alerts', title: '告警管理', icon: Bell, section: '智能运维' },
]
</script>

<template>
  <div class="app-shell">
    <a class="skip-link" href="#main-content">跳转到主要内容</a>
    <button
      v-if="menuOpen"
      class="sidebar-backdrop"
      aria-label="关闭导航"
      @click="menuOpen = false"
    />
    <aside id="main-navigation" class="sidebar" :class="{ 'is-open': menuOpen }">
      <RouterLink to="/" class="brand" @click="menuOpen = false">
        <span class="brand-mark"><Operation /></span>
        <span><strong>INDUSTRIAL AI</strong><small>工业设备故障预测系统</small></span>
      </RouterLink>
      <div class="workspace-label">运维工作空间 <span>DEV</span></div>
      <nav aria-label="主要导航">
        <template v-for="(item, index) in navigation" :key="item.path">
          <div
            v-if="index === 0 || navigation[index - 1]?.section !== item.section"
            class="nav-section"
          >
            {{ item.section }}
          </div>
          <RouterLink
            :to="item.path"
            class="nav-link"
            :class="{ active: route.path === item.path }"
            @click="menuOpen = false"
          >
            <component :is="item.icon" class="nav-icon" /><span>{{ item.title }}</span>
            <span v-if="route.path === item.path" class="nav-active-dot" />
          </RouterLink>
        </template>
      </nav>
      <div class="sidebar-footer">
        <span class="status-dot" /> 本地开发环境<small>基础框架 v0.1.0</small>
      </div>
    </aside>
    <div class="workspace">
      <header class="topbar">
        <button
          class="menu-toggle"
          :aria-expanded="menuOpen"
          aria-controls="main-navigation"
          :aria-label="menuOpen ? '关闭导航' : '打开导航'"
          @click="menuOpen = !menuOpen"
        >
          <component :is="menuOpen ? Close : Menu" />
        </button>
        <div class="breadcrumb">
          <span>{{ route.meta.section }}</span
          ><span class="separator">/</span><strong>{{ route.meta.title }}</strong>
        </div>
        <div class="topbar-meta">
          <span class="development-badge">开发预览</span><span class="avatar">研</span
          ><span class="developer-label">毕业设计工作台</span>
        </div>
      </header>
      <main id="main-content" class="main-content"><RouterView /></main>
      <footer class="page-footer">
        <span>基于 Web 与机器学习的工业设备故障预测系统</span><span>PHASE 01 · 工程初始化</span>
      </footer>
    </div>
  </div>
</template>
