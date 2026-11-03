import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { getHealth } from '../api/health'
import { useHealthStore } from './health'
import type { HealthResponse } from '../types/health'

vi.mock('../api/health', () => ({ getHealth: vi.fn() }))
const response: HealthResponse = {
  status: 'ok',
  service: 'test API',
  version: '0.1.0',
  database: 'ok',
  timestamp: '2026-11-03T00:00:00Z',
}

beforeEach(() => {
  setActivePinia(createPinia())
  vi.resetAllMocks()
})

describe('backend connection state', () => {
  it('shows success after a healthy response', async () => {
    vi.mocked(getHealth).mockResolvedValue(response)
    const store = useHealthStore()
    await store.checkHealth()
    expect(store.status).toBe('online')
    expect(store.result).toEqual(response)
    expect(store.checkedAt).toBeTruthy()
  })

  it('clears stale success and permits recovery after failure', async () => {
    const store = useHealthStore()
    vi.mocked(getHealth)
      .mockResolvedValueOnce(response)
      .mockRejectedValueOnce(new Error('网络不可达'))
      .mockResolvedValueOnce(response)
    await store.checkHealth()
    await store.checkHealth()
    expect(store.status).toBe('offline')
    expect(store.result).toBeNull()
    expect(store.error).toBe('网络不可达')
    await store.checkHealth()
    expect(store.status).toBe('online')
    expect(store.error).toBe('')
  })

  it('prevents duplicate checks while a request is in flight', async () => {
    let resolve!: (value: HealthResponse) => void
    vi.mocked(getHealth).mockReturnValue(
      new Promise((done) => {
        resolve = done
      }),
    )
    const store = useHealthStore()
    const check = store.checkHealth()
    await store.checkHealth()
    expect(getHealth).toHaveBeenCalledTimes(1)
    expect(store.status).toBe('loading')
    resolve(response)
    await check
    expect(store.status).toBe('online')
  })
})
