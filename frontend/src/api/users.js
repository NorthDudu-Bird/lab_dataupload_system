import request from './request'

export const userApi = {
  list: (params) => request.get('/users', { params }),
  create: (data) => request.post('/users', data),
  update: (id, data) => request.put(`/users/${id}`, data),
  remove: (id) => request.delete(`/users/${id}`),
  changeStatus: (id, status) => request.patch(`/users/${id}/status`, { status }),
  resetPassword: (id, password = '123456') => request.patch(`/users/${id}/password/reset`, { password })
}

