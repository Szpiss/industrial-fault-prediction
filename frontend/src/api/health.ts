import { ApiError, http } from './http'
import type { HealthResponse } from '../types/health'

export async function getHealth(): Promise<HealthResponse> {
  const { data } = await http.get<HealthResponse>('/health')
  if (data.status !== 'ok' || data.database !== 'ok' || typeof data.timestamp !== 'string') {
    throw new ApiError('健康检查响应格式不正确，请检查 API 地址。')
  }
  return data
}
