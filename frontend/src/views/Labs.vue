<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">实验室管理</h1>
      <el-button v-if="userStore.isAdmin" type="primary" :icon="Plus" @click="openDialog()">新增实验室</el-button>
    </div>

    <div class="toolbar">
      <div class="toolbar-form">
        <el-input v-model="query.keyword" clearable placeholder="编号或名称" style="width: 220px" />
        <el-select v-model="query.status" clearable placeholder="状态" style="width: 140px">
          <el-option label="启用" value="enabled" />
          <el-option label="禁用" value="disabled" />
        </el-select>
        <el-button type="primary" :icon="Search" @click="loadData">查询</el-button>
        <el-button :icon="Refresh" @click="resetQuery">重置</el-button>
      </div>
    </div>

    <div class="panel">
      <el-table :data="tableData" border stripe>
        <el-table-column prop="lab_code" label="实验室编号" width="150" />
        <el-table-column prop="lab_name" label="实验室名称" min-width="180" />
        <el-table-column prop="building" label="楼宇" />
        <el-table-column prop="room_no" label="房间号" />
        <el-table-column prop="manager_name" label="负责人" />
        <el-table-column prop="capacity" label="容量" width="90" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="tagTypeOf(row.status)">{{ labelOf(labStatusMap, row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="180" show-overflow-tooltip />
        <el-table-column v-if="userStore.isAdmin" label="操作" width="170" fixed="right">
          <template #default="{ row }">
            <div class="table-actions">
              <el-button size="small" :icon="Edit" @click="openDialog(row)">编辑</el-button>
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

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑实验室' : '新增实验室'" width="640px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <div class="form-grid">
          <el-form-item label="实验室编号" prop="lab_code">
            <el-input v-model="form.lab_code" />
          </el-form-item>
          <el-form-item label="实验室名称" prop="lab_name">
            <el-input v-model="form.lab_name" />
          </el-form-item>
          <el-form-item label="楼宇" prop="building">
            <el-input v-model="form.building" />
          </el-form-item>
          <el-form-item label="房间号" prop="room_no">
            <el-input v-model="form.room_no" />
          </el-form-item>
          <el-form-item label="负责人">
            <el-input v-model="form.manager_name" />
          </el-form-item>
          <el-form-item label="容量">
            <el-input-number v-model="form.capacity" :min="0" style="width: 100%" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-radio-group v-model="form.status">
              <el-radio-button label="enabled">启用</el-radio-button>
              <el-radio-button label="disabled">禁用</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item class="full-row" label="备注">
            <el-input v-model="form.remark" type="textarea" />
          </el-form-item>
        </div>
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
import { labApi } from '../api/labs'
import { useUserStore } from '../stores/user'
import { labStatusMap, labelOf, tagTypeOf } from '../utils/dicts'

const userStore = useUserStore()
const tableData = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const formRef = ref()
const query = reactive({ page: 1, page_size: 10, keyword: '', status: '' })
const form = reactive(defaultForm())
const rules = {
  lab_code: [{ required: true, message: '请输入实验室编号', trigger: 'blur' }],
  lab_name: [{ required: true, message: '请输入实验室名称', trigger: 'blur' }],
  building: [{ required: true, message: '请输入楼宇', trigger: 'blur' }],
  room_no: [{ required: true, message: '请输入房间号', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

function defaultForm() {
  return { id: null, lab_code: '', lab_name: '', building: '', room_no: '', manager_name: '', capacity: 0, status: 'enabled', remark: '' }
}

async function loadData() {
  const data = await labApi.list(query)
  tableData.value = data.items
  total.value = data.total
}

function resetQuery() {
  Object.assign(query, { page: 1, page_size: 10, keyword: '', status: '' })
  loadData()
}

function openDialog(row) {
  Object.assign(form, defaultForm(), row || {})
  dialogVisible.value = true
}

async function save() {
  await formRef.value.validate()
  if (form.id) await labApi.update(form.id, form)
  else await labApi.create(form)
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadData()
}

async function remove(row) {
  await ElMessageBox.confirm(`确认删除实验室 ${row.lab_name}？`, '删除确认', { type: 'warning' })
  await labApi.remove(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>

