<template>
  <div class="login-page">
    <div class="login-panel">
      <div class="login-visual">
        <div class="system-name">实验室数据上报系统</div>
        <div class="system-desc">Lab Data Reporting System</div>
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
    linear-gradient(135deg, rgba(37, 99, 235, 0.14), rgba(16, 185, 129, 0.14)),
    #eef2f7;
}

.login-panel {
  width: min(920px, 100%);
  min-height: 520px;
  display: grid;
  grid-template-columns: 1fr 380px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.14);
}

.login-visual {
  padding: 48px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  color: #ffffff;
  background:
    linear-gradient(rgba(17, 24, 39, 0.35), rgba(17, 24, 39, 0.72)),
    url("https://images.unsplash.com/photo-1581093458791-9d42cc030243?auto=format&fit=crop&w=1200&q=80") center/cover;
}

.system-name {
  font-size: 36px;
  font-weight: 800;
}

.system-desc {
  margin-top: 10px;
  font-size: 18px;
  color: #dbeafe;
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
    min-height: 220px;
  }
}
</style>

