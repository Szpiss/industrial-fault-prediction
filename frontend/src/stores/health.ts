import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getHealth } from '../api/health'
import type { ConnectionStatus, HealthResponse } from '../types/health'

export const useHealthStore = defineStore('health', () => {
  const status = ref<ConnectionStatus>('idle')
  const result = ref<HealthResponse | null>(null)
  const error = ref('')
  const checkedAt = ref<string | null>(null)

  async function checkHealth() {
    if (status.value === 'loading') return
    status.value = 'loading'
    error.value = ''
    result.value = null
    try {
      result.value = await getHealth()
      status.value = 'online'
    } catch (cause) {
      status.value = 'offline'
      error.value = cause instanceof Error ? cause.message : '服务连接失败，请稍后重试。'
    } finally {
      checkedAt.value = new Date().toISOString()
    }
  }

  return { status, result, error, checkedAt, checkHealth }
})
