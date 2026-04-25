<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">公告管理</h1>
      <el-button v-if="userStore.isAdmin" type="primary" :icon="Plus" @click="openDialog()">发布公告</el-button>
    </div>

    <div class="toolbar">
      <div class="toolbar-form">
        <el-input v-model="query.keyword" clearable placeholder="公告标题" style="width: 220px" />
        <el-select v-if="userStore.isAdmin" v-model="query.status" clearable placeholder="状态" style="width: 140px">
          <el-option label="草稿" value="draft" />
          <el-option label="已发布" value="published" />
        </el-select>
        <el-button type="primary" :icon="Search" @click="loadData">查询</el-button>
        <el-button :icon="Refresh" @click="resetQuery">重置</el-button>
      </div>
    </div>

    <div class="notice-list">
      <div v-for="item in tableData" :key="item.id" class="notice-item">
        <div class="notice-head">
          <div>
            <h2>{{ item.title }}</h2>
            <div class="notice-meta">
              {{ item.publisher_name }} · {{ item.published_time || item.create_time }}
              <el-tag v-if="userStore.isAdmin" size="small" :type="tagTypeOf(item.status)">
                {{ labelOf(noticeStatusMap, item.status) }}
              </el-tag>
            </div>
          </div>
          <div v-if="userStore.isAdmin" class="table-actions">
            <el-button size="small" :icon="Edit" @click="openDialog(item)">编辑</el-button>
            <el-button size="small" type="danger" :icon="Delete" @click="remove(item)">删除</el-button>
          </div>
        </div>
        <p>{{ item.content }}</p>
      </div>
    </div>

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

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑公告' : '发布公告'" width="680px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="7" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio-button label="published">发布</el-radio-button>
            <el-radio-button label="draft">草稿</el-radio-button>
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
import { Delete, Edit, Plus, Refresh, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { onMounted, reactive, ref } from 'vue'
import { noticeApi } from '../api/notices'
import { useUserStore } from '../stores/user'
import { labelOf, noticeStatusMap, tagTypeOf } from '../utils/dicts'

const userStore = useUserStore()
const tableData = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const formRef = ref()
const query = reactive({ page: 1, page_size: 8, keyword: '', status: '' })
const form = reactive(defaultForm())
const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

function defaultForm() {
  return { id: null, title: '', content: '', status: 'published' }
}

async function loadData() {
  const data = await noticeApi.list(query)
  tableData.value = data.items
  total.value = data.total
}

function resetQuery() {
  Object.assign(query, { page: 1, page_size: 8, keyword: '', status: '' })
  loadData()
}

function openDialog(row) {
  Object.assign(form, defaultForm(), row || {})
  dialogVisible.value = true
}

async function save() {
  await formRef.value.validate()
  if (form.id) await noticeApi.update(form.id, form)
  else await noticeApi.create(form)
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadData()
}

async function remove(row) {
  await ElMessageBox.confirm(`确认删除公告 ${row.title}？`, '删除确认', { type: 'warning' })
  await noticeApi.remove(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.notice-list {
  display: grid;
  gap: 14px;
}

.notice-item {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 18px;
}

.notice-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.notice-head h2 {
  margin: 0;
  font-size: 18px;
}

.notice-meta {
  margin-top: 8px;
  color: #6b7280;
  display: flex;
  gap: 8px;
  align-items: center;
}

.notice-item p {
  margin: 14px 0 0;
  color: #374151;
  line-height: 1.8;
  white-space: pre-wrap;
}
</style>

