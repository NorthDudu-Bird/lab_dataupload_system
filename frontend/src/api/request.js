import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000
})

service.interceptors.request.use((config) => {
  const token = localStorage.getItem('lab_report_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

service.interceptors.response.use(
  (response) => {
    const body = response.data
    if (body.code !== 200) {
      ElMessage.error(body.message || '请求失败')
      return Promise.reject(body)
    }
    return body.data
  },
  (error) => {
    const response = error.response
    if (response?.status === 401) {
      localStorage.removeItem('lab_report_token')
      localStorage.removeItem('lab_report_user')
      router.replace('/login')
    }
    ElMessage.error(response?.data?.message || '网络或服务器异常')
    return Promise.reject(error)
  }
)

export default service

