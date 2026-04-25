import request from './request'

export const noticeApi = {
  list: (params) => request.get('/notices', { params }),
  create: (data) => request.post('/notices', data),
  update: (id, data) => request.put(`/notices/${id}`, data),
  remove: (id) => request.delete(`/notices/${id}`)
}

