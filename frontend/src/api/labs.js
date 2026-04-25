import request from './request'

export const labApi = {
  list: (params) => request.get('/labs', { params }),
  create: (data) => request.post('/labs', data),
  update: (id, data) => request.put(`/labs/${id}`, data),
  remove: (id) => request.delete(`/labs/${id}`)
}

