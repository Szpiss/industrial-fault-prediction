export interface HealthResponse {
  status: 'ok'
  service: string
  version: string
  database: 'ok'
  timestamp: string
}

export type ConnectionStatus = 'idle' | 'loading' | 'online' | 'offline'
