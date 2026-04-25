<template>
  <el-container class="app-shell">
    <el-aside width="236px" class="sidebar">
      <div class="brand">
        <div class="brand-mark">LAB</div>
        <div>
          <div class="brand-title">实验室数据上报系统</div>
          <div class="brand-subtitle">{{ roleMap[userStore.role] }}</div>
        </div>
      </div>
      <el-menu :default-active="route.path" router class="side-menu">
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="topbar">
        <div class="top-title">{{ route.meta.title }}</div>
        <div class="top-user">
          <span>{{ userStore.user?.real_name }}</span>
          <el-tag size="small">{{ roleMap[userStore.role] }}</el-tag>
          <el-button :icon="SwitchButton" @click="handleLogout">退出</el-button>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import {
  Bell,
  DataAnalysis,
  DocumentChecked,
  Files,
  House,
  Monitor,
  SwitchButton,
  User
} from '@element-plus/icons-vue'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { roleMap } from '../utils/dicts'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const allMenus = [
  { path: '/dashboard', title: '首页统计', roles: ['admin', 'reviewer', 'reporter'], icon: DataAnalysis },
  { path: '/users', title: '用户管理', roles: ['admin'], icon: User },
  { path: '/labs', title: '实验室管理', roles: ['admin', 'reviewer'], icon: House },
  { path: '/equipments', title: '设备管理', roles: ['admin', 'reviewer'], icon: Monitor },
  { path: '/reports', title: '上报记录', roles: ['admin', 'reviewer', 'reporter'], icon: Files },
  { path: '/reviews', title: '审核管理', roles: ['admin', 'reviewer'], icon: DocumentChecked },
  { path: '/notices', title: '公告管理', roles: ['admin', 'reviewer', 'reporter'], icon: Bell }
]

const menus = computed(() => allMenus.filter((item) => item.roles.includes(userStore.role)))

function handleLogout() {
  userStore.logout()
  router.replace('/login')
}
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.sidebar {
  background: #111827;
  color: #ffffff;
}

.brand {
  height: 76px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 8px;
  display: grid;
  place-items: center;
  color: #ffffff;
  font-weight: 800;
  background: #2563eb;
}

.brand-title {
  font-size: 15px;
  font-weight: 700;
}

.brand-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #a7f3d0;
}

.side-menu {
  border-right: 0;
  background: transparent;
}

.side-menu :deep(.el-menu-item) {
  color: #d1d5db;
}

.side-menu :deep(.el-menu-item.is-active) {
  color: #ffffff;
  background: #1d4ed8;
}

.topbar {
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.top-title {
  font-size: 18px;
  font-weight: 700;
}

.top-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.main-content {
  min-height: calc(100vh - 64px);
  background: #f5f7fb;
  padding: 20px;
}

@media (max-width: 760px) {
  .sidebar {
    width: 72px !important;
  }

  .brand {
    justify-content: center;
    padding: 12px;
  }

  .brand > div:not(.brand-mark),
  .side-menu :deep(.el-menu-item span) {
    display: none;
  }

  .side-menu :deep(.el-menu-item) {
    justify-content: center;
    padding: 0 !important;
  }

  .side-menu :deep(.el-icon) {
    margin-right: 0;
  }

  .topbar {
    padding: 0 12px;
  }

  .top-title {
    font-size: 16px;
  }

  .top-user > span {
    display: none;
  }

  .main-content {
    padding: 14px;
  }
}
</style>
