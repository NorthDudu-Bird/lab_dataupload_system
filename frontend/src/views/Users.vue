<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">用户管理</h1>
      <el-button type="primary" :icon="Plus" @click="openDialog()">新增用户</el-button>
    </div>

    <div class="toolbar">
      <div class="toolbar-form">
        <el-input v-model="query.username" clearable placeholder="用户名" style="width: 180px" />
        <el-input v-model="query.real_name" clearable placeholder="真实姓名" style="width: 180px" />
        <el-select v-model="query.role" clearable placeholder="角色" style="width: 150px">
          <el-option label="系统管理员" value="admin" />
          <el-option label="审核员" value="reviewer" />
          <el-option label="上报员" value="reporter" />
        </el-select>
        <el-button type="primary" :icon="Search" @click="loadData">查询</el-button>
        <el-button :icon="Refresh" @click="resetQuery">重置</el-button>
      </div>
    </div>

    <div class="panel">
      <el-table :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="real_name" label="真实姓名" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="email" label="邮箱" min-width="170" />
        <el-table-column label="角色" width="120">
          <template #default="{ row }">{{ labelOf(roleMap, row.role) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="tagTypeOf(row.status)">{{ labelOf(userStatusMap, row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="170" />
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <div class="table-actions">
              <el-button size="small" :icon="Edit" @click="openDialog(row)">编辑</el-button>
              <el-button size="small" :type="row.status === 'enabled' ? 'warning' : 'success'" @click="toggleStatus(row)">
                {{ row.status === 'enabled' ? '禁用' : '启用' }}
              </el-button>
              <el-button size="small" :icon="Key" @click="resetPassword(row)">重置密码</el-button>
              <el-button size="small" type="danger" :icon="Delete" @click="remove(row)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="query.page"
          v-model:page-size="query.page_size"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @current-change="loadData"
          @size-change="loadData"
        />
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑用户' : '新增用户'" width="560px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="86px">
        <el-form-item v-if="!form.id" label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item v-if="!form.id" label="初始密码" prop="password">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="form.real_name" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" style="width: 100%">
            <el-option label="系统管理员" value="admin" />
            <el-option label="审核员" value="reviewer" />
            <el-option label="上报员" value="reporter" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio-button label="enabled">启用</el-radio-button>
            <el-radio-button label="disabled">禁用</el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { Delete, Edit, Key, Plus, Refresh, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { onMounted, reactive, ref } from 'vue'
import { userApi } from '../api/users'
import { labelOf, roleMap, tagTypeOf, userStatusMap } from '../utils/dicts'

const tableData = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const formRef = ref()
const query = reactive({ page: 1, page_size: 10, username: '', real_name: '', role: '' })
const form = reactive(defaultForm())

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

function defaultForm() {
  return {
    id: null,
    username: '',
    password: '123456',
    real_name: '',
    phone: '',
    email: '',
    role: 'reporter',
    status: 'enabled'
  }
}

async function loadData() {
  const data = await userApi.list(query)
  tableData.value = data.items
  total.value = data.total
}

function resetQuery() {
  Object.assign(query, { page: 1, page_size: 10, username: '', real_name: '', role: '' })
  loadData()
}

function openDialog(row) {
  Object.assign(form, defaultForm(), row || {})
  dialogVisible.value = true
}

async function save() {
  await formRef.value.validate()
  if (form.id) {
    await userApi.update(form.id, form)
    ElMessage.success('更新成功')
  } else {
    await userApi.create(form)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

async function toggleStatus(row) {
  const status = row.status === 'enabled' ? 'disabled' : 'enabled'
  await userApi.changeStatus(row.id, status)
  ElMessage.success('状态更新成功')
  loadData()
}

async function resetPassword(row) {
  await ElMessageBox.confirm(`确认将 ${row.username} 的密码重置为 123456？`, '重置密码')
  await userApi.resetPassword(row.id)
  ElMessage.success('密码已重置')
}

async function remove(row) {
  await ElMessageBox.confirm(`确认删除用户 ${row.username}？`, '删除确认', { type: 'warning' })
  await userApi.remove(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>

