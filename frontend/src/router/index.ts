import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'

declare module 'vue-router' {
  interface RouteMeta {
    title: string
    section?: string
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: AppLayout,
      meta: { title: '工作台' },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('../views/DashboardView.vue'),
          meta: { title: '设备状态总览', section: '工作台' },
        },
        {
          path: 'devices',
          name: 'devices',
          component: () => import('../views/DevicesView.vue'),
          meta: { title: '设备管理', section: '设备中心' },
        },
        {
          path: 'analysis',
          name: 'analysis',
          component: () => import('../views/AnalysisView.vue'),
          meta: { title: '数据分析', section: '设备中心' },
        },
        {
          path: 'predictions',
          name: 'predictions',
          component: () => import('../views/PredictionsView.vue'),
          meta: { title: '故障预测', section: '智能运维' },
        },
        {
          path: 'alerts',
          name: 'alerts',
          component: () => import('../views/AlertsView.vue'),
          meta: { title: '告警管理', section: '智能运维' },
        },
        {
          path: ':pathMatch(.*)*',
          name: 'not-found',
          component: () => import('../views/NotFoundView.vue'),
          meta: { title: '页面不存在', section: '工作台' },
        },
      ],
    },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

router.afterEach((to) => {
  document.title = `${to.meta.title} · 工业设备故障预测系统`
})
export default router
