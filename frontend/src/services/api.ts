import axios from 'axios'
import { useToken } from '@/stores/auth'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
api.interceptors.request.use(
  (config) => {
    const token = useToken.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// API helper functions
export const authApi = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  
  register: (data: { username: string; email: string; password: string }) =>
    api.post('/auth/register', data),
  
  me: () => api.get('/auth/me'),
}

export const alertsApi = {
  list: (params?: { page?: number; pageSize?: number; severity?: string; status?: string }) =>
    api.get('/alerts', { params }),
  
  get: (id: string) => api.get(`/alerts/${id}`),
  
  update: (id: string, data: { status?: string; notes?: string }) =>
    api.put(`/alerts/${id}`, data),
  
  delete: (id: string) => api.delete(`/alerts/${id}`),
}

export const casesApi = {
  list: (params?: { page?: number; status?: string; severity?: string }) =>
    api.get('/cases', { params }),
  
  get: (id: string) => api.get(`/cases/${id}`),
  
  create: (data: { title: string; description?: string; severity?: string }) =>
    api.post('/cases', data),
  
  update: (id: string, data: any) => api.put(`/cases/${id}`, data),
  
  close: (id: string, resolution?: string) =>
    api.post(`/cases/${id}/close`, { resolution }),
}

export const assetsApi = {
  list: (params?: { page?: number; search?: string }) =>
    api.get('/assets', { params }),
  
  get: (id: string) => api.get(`/assets/${id}`),
  
  create: (data: any) => api.post('/assets', data),
  
  update: (id: string, data: any) => api.put(`/assets/${id}`, data),
}

export const sensorsApi = {
  list: (params?: { page?: number; type?: string }) =>
    api.get('/sensors', { params }),
  
  get: (id: string) => api.get(`/sensors/${id}`),
  
  create: (data: any) => api.post('/sensors', data),
  
  update: (id: string, data: any) => api.put(`/sensors/${id}`, data),
}

export const collectApi = {
  sendEvent: (data: { source_type: string; raw: string }) =>
    api.post('/collect/event', data),
  
  listConnectors: () => api.get('/collect/connectors'),
  
  testConnector: (id: string) => api.post(`/collect/connectors/${id}/test`),
}
