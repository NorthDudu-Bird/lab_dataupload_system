import { defineStore } from 'pinia'
import { getProfile, login } from '../api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('lab_report_token') || '',
    user: JSON.parse(localStorage.getItem('lab_report_user') || 'null')
  }),
  getters: {
    role: (state) => state.user?.role || '',
    isAdmin: (state) => state.user?.role === 'admin'
  },
  actions: {
    async loginAction(payload) {
      const data = await login(payload)
      this.token = data.token
      this.user = data.user
      localStorage.setItem('lab_report_token', data.token)
      localStorage.setItem('lab_report_user', JSON.stringify(data.user))
    },
    async fetchProfile() {
      const user = await getProfile()
      this.user = user
      localStorage.setItem('lab_report_user', JSON.stringify(user))
      return user
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('lab_report_token')
      localStorage.removeItem('lab_report_user')
    }
  }
})

