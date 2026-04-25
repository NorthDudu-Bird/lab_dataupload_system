import request from './request'

export const reportApi = {
  list: (params) => request.get('/reports', { params }),
  detail: (id) => request.get(`/reports/${id}`),
  create: (data) => request.post('/reports', data),
  update: (id, data) => request.put(`/reports/${id}`, data),
  remove: (id) => request.delete(`/reports/${id}`),
  upload: (formData) =>
    request.post('/reports/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
}

