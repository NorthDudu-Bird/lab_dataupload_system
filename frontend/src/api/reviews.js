import request from './request'

export const reviewApi = {
  list: (params) => request.get('/reviews', { params }),
  audit: (id, data) => request.post(`/reviews/${id}/audit`, data)
}

