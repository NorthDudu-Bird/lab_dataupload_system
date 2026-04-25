import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'
import MainLayout from '../layout/MainLayout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '首页统计', roles: ['admin', 'reviewer', 'reporter'] }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/Users.vue'),
        meta: { title: '用户管理', roles: ['admin'] }
      },
      {
        path: 'labs',
        name: 'Labs',
        component: () => import('../views/Labs.vue'),
        meta: { title: '实验室管理', roles: ['admin', 'reviewer'] }
      },
      {
        path: 'equipments',
        name: 'Equipments',
        component: () => import('../views/Equipments.vue'),
        meta: { title: '设备管理', roles: ['admin', 'reviewer'] }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('../views/Reports.vue'),
        meta: { title: '上报记录', roles: ['admin', 'reviewer', 'reporter'] }
      },
      {
        path: 'reports/create',
        name: 'ReportCreate',
        component: () => import('../views/ReportForm.vue'),
        meta: { title: '新增上报', roles: ['admin', 'reporter'] }
      },
      {
        path: 'reports/edit/:id',
        name: 'ReportEdit',
        component: () => import('../views/ReportForm.vue'),
        meta: { title: '编辑上报', roles: ['admin', 'reporter'] }
      },
      {
        path: 'reports/detail/:id',
        name: 'ReportDetail',
        component: () => import('../views/ReportDetail.vue'),
        meta: { title: '上报详情', roles: ['admin', 'reviewer', 'reporter'] }
      },
      {
        path: 'reviews',
        name: 'Reviews',
        component: () => import('../views/Reviews.vue'),
        meta: { title: '审核管理', roles: ['admin', 'reviewer'] }
      },
      {
        path: 'notices',
        name: 'Notices',
        component: () => import('../views/Notices.vue'),
        meta: { title: '公告管理', roles: ['admin', 'reviewer', 'reporter'] }
      }
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/dashboard' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.public) {
    if (userStore.token && to.path === '/login') return next('/dashboard')
    return next()
  }

  if (!userStore.token) {
    return next(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }

  if (!userStore.user) {
    try {
      await userStore.fetchProfile()
    } catch {
      userStore.logout()
      return next('/login')
    }
  }

  const roles = to.meta.roles || []
  if (roles.length && !roles.includes(userStore.role)) {
    return next('/dashboard')
  }
  return next()
})

export default router

