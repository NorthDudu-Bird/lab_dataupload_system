import request from './request'

export const equipmentApi = {
  list: (params) => request.get('/equipments', { params }),
  create: (data) => request.post('/equipments', data),
  update: (id, data) => request.put(`/equipments/${id}`, data),
  remove: (id) => request.delete(`/equipments/${id}`)
}

