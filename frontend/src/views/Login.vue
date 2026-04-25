<template>
  <div class="login-page">
    <div class="login-panel">
      <div class="login-visual">
        <div class="visual-copy">
          <div class="visual-badge">LAB REPORT SYSTEM</div>
          <div class="system-name">实验室数据上报系统</div>
          <div class="system-desc">Lab Data Reporting System</div>
        </div>
        <div class="mock-screen">
          <div class="mock-header">
            <span></span>
            <span></span>
            <span></span>
            <strong>系统功能概览</strong>
          </div>
          <div class="mock-grid">
            <div class="mock-card">
              <small>数据上报</small>
              <b>填报</b>
            </div>
            <div class="mock-card warning">
              <small>审核管理</small>
              <b>流转</b>
            </div>
            <div class="mock-card success">
              <small>统计分析</small>
              <b>图表</b>
            </div>
          </div>
          <div class="mock-chart">
            <i style="height: 38%"></i>
            <i style="height: 54%"></i>
            <i style="height: 72%"></i>
            <i style="height: 45%"></i>
            <i style="height: 84%"></i>
            <i style="height: 62%"></i>
          </div>
          <div class="mock-status">
            <span>实验室信息</span>
            <span>设备台账</span>
            <span>公告通知</span>
          </div>
        </div>
      </div>
      <div class="login-form-wrap">
        <h1>用户登录</h1>
        <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @keyup.enter="handleLogin">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" size="large" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="form.password" size="large" type="password" show-password placeholder="请输入密码" />
          </el-form-item>
          <el-button type="primary" size="large" class="login-button" :loading="loading" @click="handleLogin">
            登录
          </el-button>
        </el-form>
        <div class="account-line">默认账号：admin / admin123，reviewer / 123456，reporter1 / 123456</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const formRef = ref()
const loading = ref(false)
const form = reactive({
  username: 'admin',
  password: 'admin123'
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

async function handleLogin() {
  await formRef.value.validate()
  loading.value = true
  try {
    await userStore.loginAction(form)
    ElMessage.success('登录成功')
    router.replace(route.query.redirect ? decodeURIComponent(route.query.redirect) : '/dashboard')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 28px;
  background:
    linear-gradient(120deg, rgba(37, 99, 235, 0.18), transparent 34%),
    linear-gradient(300deg, rgba(20, 184, 166, 0.18), transparent 38%),
    linear-gradient(180deg, #edf5ff 0%, #f7fafc 44%, #eef7f4 100%);
}

.login-panel {
  width: min(1040px, 100%);
  min-height: 580px;
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) 390px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.14);
}

.login-visual {
  position: relative;
  min-height: 580px;
  padding: 48px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 30px;
  color: #ffffff;
  background:
    linear-gradient(135deg, rgba(10, 31, 68, 0.96), rgba(13, 92, 105, 0.92)),
    repeating-linear-gradient(0deg, rgba(255, 255, 255, 0.06) 0 1px, transparent 1px 34px),
    repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.05) 0 1px, transparent 1px 34px);
  overflow: hidden;
}

.login-visual::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(115deg, transparent 0 44%, rgba(96, 165, 250, 0.14) 44% 45%, transparent 45% 100%),
    linear-gradient(155deg, transparent 0 62%, rgba(45, 212, 191, 0.16) 62% 63%, transparent 63% 100%);
  pointer-events: none;
}

.visual-copy,
.mock-screen {
  position: relative;
  z-index: 1;
}

.visual-badge {
  width: fit-content;
  padding: 7px 12px;
  border: 1px solid rgba(191, 219, 254, 0.5);
  border-radius: 999px;
  color: #bfdbfe;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 1.2px;
}

.system-name {
  margin-top: 22px;
  font-size: 36px;
  font-weight: 800;
  line-height: 1.18;
}

.system-desc {
  margin-top: 10px;
  font-size: 18px;
  color: #dbeafe;
}

.mock-screen {
  width: min(520px, 100%);
  border: 1px solid rgba(191, 219, 254, 0.22);
  border-radius: 8px;
  background: rgba(15, 23, 42, 0.46);
  box-shadow: 0 24px 56px rgba(0, 0, 0, 0.28);
  backdrop-filter: blur(10px);
  padding: 18px;
}

.mock-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e5f2ff;
  font-size: 14px;
}

.mock-header span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #38bdf8;
}

.mock-header span:nth-child(2) {
  background: #22c55e;
}

.mock-header span:nth-child(3) {
  background: #f59e0b;
}

.mock-header strong {
  margin-left: 8px;
}

.mock-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 18px;
}

.mock-card {
  min-height: 76px;
  padding: 12px;
  border-radius: 8px;
  background: rgba(37, 99, 235, 0.18);
  border: 1px solid rgba(147, 197, 253, 0.22);
}

.mock-card small {
  display: block;
  color: #bfdbfe;
  font-size: 12px;
}

.mock-card b {
  display: block;
  margin-top: 8px;
  font-size: 26px;
  line-height: 1;
}

.mock-card.warning {
  background: rgba(217, 119, 6, 0.18);
}

.mock-card.success {
  background: rgba(5, 150, 105, 0.2);
}

.mock-chart {
  height: 120px;
  display: flex;
  align-items: flex-end;
  gap: 12px;
  margin-top: 18px;
  padding: 16px 12px 0;
  border-radius: 8px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02)),
    repeating-linear-gradient(0deg, transparent 0 29px, rgba(255, 255, 255, 0.08) 30px);
}

.mock-chart i {
  flex: 1;
  border-radius: 6px 6px 0 0;
  background: linear-gradient(180deg, #60a5fa, #2dd4bf);
}

.mock-status {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 16px;
}

.mock-status span {
  padding: 6px 10px;
  border-radius: 999px;
  color: #dbeafe;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.14);
  font-size: 12px;
}

.login-form-wrap {
  padding: 54px 34px;
}

.login-form-wrap h1 {
  margin: 0 0 28px;
  font-size: 26px;
}

.login-button {
  width: 100%;
  margin-top: 8px;
}

.account-line {
  margin-top: 18px;
  color: #6b7280;
  font-size: 13px;
  line-height: 1.7;
}

@media (max-width: 760px) {
  .login-panel {
    grid-template-columns: 1fr;
  }

  .login-visual {
    min-height: 360px;
    padding: 34px;
  }

  .mock-screen {
    display: none;
  }
}
</style>
