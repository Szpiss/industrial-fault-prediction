<script setup lang="ts">
import { computed, onMounted } from 'vue'
import {
  Connection,
  RefreshRight,
  Right,
  Monitor,
  DataAnalysis,
  TrendCharts,
  Bell,
} from '@element-plus/icons-vue'
import { useHealthStore } from '../stores/health'

const health = useHealthStore()
const statusLabel = computed(
  () =>
    ({
      idle: '等待检查',
      loading: '正在检查连接',
      online: '后端服务运行正常',
      offline: '后端连接异常',
    })[health.status],
)
const checkedTime = computed(() =>
  health.checkedAt
    ? new Date(health.checkedAt).toLocaleString('zh-CN', { hour12: false })
    : '尚未检查',
)
const modules = [
  {
    title: '设备管理',
    text: '建立设备台账，记录设备运行状态',
    icon: Monitor,
    path: '/devices',
    number: '01',
  },
  {
    title: '数据分析',
    text: '导入传感器数据，进行清洗与特征分析',
    icon: DataAnalysis,
    path: '/analysis',
    number: '02',
  },
  {
    title: '故障预测',
    text: '接入机器学习模型，评估设备故障风险',
    icon: TrendCharts,
    path: '/predictions',
    number: '03',
  },
  {
    title: '告警管理',
    text: '设置风险阈值，跟进设备告警事件',
    icon: Bell,
    path: '/alerts',
    number: '04',
  },
]
onMounted(() => {
  void health.checkHealth()
})
</script>

<template>
  <div class="page-heading">
    <div>
      <p class="eyebrow">OVERVIEW / 系统工作台</p>
      <h1>设备状态总览</h1>
      <p>从数据连接开始，构建设备的智能运维工作流。</p>
    </div>
    <el-tag effect="plain" type="info">第一阶段 · 基础框架</el-tag>
  </div>

  <section
    class="connection-panel panel"
    :class="{ 'connection-error': health.status === 'offline' }"
    aria-live="polite"
    aria-atomic="true"
    data-testid="connection-panel"
  >
    <div class="connection-main">
      <div class="connection-symbol"><Connection /></div>
      <div>
        <p class="eyebrow">BACKEND CONNECTION</p>
        <h2 data-testid="connection-status">{{ statusLabel }}</h2>
        <p>
          {{
            health.status === 'offline'
              ? health.error
              : 'Vue → Axios → FastAPI → 数据库 · 开发链路健康检查'
          }}
        </p>
      </div>
    </div>
    <el-button
      :icon="RefreshRight"
      :loading="health.status === 'loading'"
      @click="health.checkHealth()"
      >重新检查</el-button
    >
    <div class="connection-details">
      <div><span>接口地址</span><code>GET /api/v1/health</code></div>
      <div>
        <span>数据库连接</span
        ><strong>{{ health.result?.database === 'ok' ? '检查通过' : '尚未确认' }}</strong>
      </div>
      <div>
        <span>API 版本</span
        ><strong>{{ health.result ? `v${health.result.version}` : '—' }}</strong>
      </div>
      <div>
        <span>最近检查</span><strong>{{ checkedTime }}</strong>
      </div>
    </div>
  </section>

  <div class="section-heading">
    <h2>运维功能模块</h2>
    <span>框架已就绪，业务功能待接入</span>
  </div>
  <div class="module-grid">
    <RouterLink v-for="item in modules" :key="item.path" :to="item.path" class="module-card panel"
      ><div class="module-top">
        <span class="module-icon"><component :is="item.icon" /></span
        ><span class="module-number">{{ item.number }}</span>
      </div>
      <h3>{{ item.title }}</h3>
      <p>{{ item.text }}</p>
      <div class="module-bottom"><span>规划中</span><Right /></div
    ></RouterLink>
  </div>

  <div class="overview-bottom">
    <section class="panel roadmap-panel">
      <div class="section-heading">
        <h2>开发路线</h2>
        <span>循序构建 · 逐步验证</span>
      </div>
      <ol class="roadmap">
        <li class="current">
          <span class="step-number">01</span>
          <div>
            <h3>工程基础框架 <el-tag size="small" effect="light">当前阶段</el-tag></h3>
            <p>项目结构、服务连通、数据库迁移与开发规范</p>
          </div>
        </li>
        <li>
          <span class="step-number">02</span>
          <div>
            <h3>设备与数据接入</h3>
            <p>设备台账、运行状态与 CSV 数据导入</p>
          </div>
        </li>
        <li>
          <span class="step-number">03</span>
          <div>
            <h3>模型评估与风险预测</h3>
            <p>特征工程、基线模型、预测结果与告警</p>
          </div>
        </li>
      </ol>
    </section>
    <section class="panel scope-panel">
      <p class="eyebrow">DEVELOPMENT NOTE</p>
      <h2>先连接，再预测。</h2>
      <p>本阶段提供可运行的工程基础。设备数据、模型训练和风险评分将在后续阶段逐步接入。</p>
      <el-alert title="当前页面未接入工业设备与预测模型" type="info" :closable="false" show-icon />
      <div class="tech-tags"><span>Vue 3</span><span>FastAPI</span><span>SQLAlchemy 2</span></div>
    </section>
  </div>
</template>
