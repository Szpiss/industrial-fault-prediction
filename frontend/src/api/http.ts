import axios from 'axios'

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status?: number,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 8000,
  headers: { Accept: 'application/json' },
})

http.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status
      const message =
        status === 503
          ? '后端可访问，但数据库检查未通过。请检查数据库连接配置。'
          : '无法连接后端服务，请确认 FastAPI 已启动，并检查代理地址与网络连接。'
      return Promise.reject(new ApiError(message, status))
    }
    return Promise.reject(new ApiError('请求发生异常，请稍后重试。'))
  },
)
