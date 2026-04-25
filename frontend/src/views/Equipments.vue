<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">设备管理</h1>
      <el-button v-if="userStore.isAdmin" type="primary" :icon="Plus" @click="openDialog()">新增设备</el-button>
    </div>

    <div class="toolbar">
      <div class="toolbar-form">
        <el-input v-model="query.keyword" clearable placeholder="编号或名称" style="width: 210px" />
        <el-select v-model="query.lab_id" clearable placeholder="实验室" style="width: 210px">
          <el-option v-for="lab in labs" :key="lab.id" :label="lab.lab_name" :value="lab.id" />
        </el-select>
        <el-select v-model="query.status" clearable placeholder="设备状态" style="width: 150px">
          <el-option label="正常" value="normal" />
          <el-option label="故障" value="faulty" />
          <el-option label="维护中" value="maintenance" />
          <el-option label="已报废" value="scrapped" />
        </el-select>
        <el-button type="primary" :icon="Search" @click="loadData">查询</el-button>
        <el-button :icon="Refresh" @click="resetQuery">重置</el-button>
      </div>
    </div>

    <div class="panel">
      <el-table :data="tableData" border stripe>
        <el-table-column prop="equipment_code" label="设备编号" width="150" />
        <el-table-column prop="equipment_name" label="设备名称" min-width="160" />
        <el-table-column prop="category" label="类别" />
        <el-table-column prop="brand" label="品牌" />
        <el-table-column prop="model" label="型号" />
        <el-table-column prop="lab_name" label="所属实验室" min-width="160" />
        <el-table-column prop="purchase_date" label="采购日期" width="120" />
        <el-table-column label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="tagTypeOf(row.status)">{{ labelOf(equipmentStatusMap, row.status) }}</el-tag>
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

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑设备' : '新增设备'" width="720px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <div class="form-grid">
          <el-form-item label="设备编号" prop="equipment_code">
            <el-input v-model="form.equipment_code" />
          </el-form-item>
          <el-form-item label="设备名称" prop="equipment_name">
            <el-input v-model="form.equipment_name" />
          </el-form-item>
          <el-form-item label="类别" prop="category">
            <el-input v-model="form.category" />
          </el-form-item>
          <el-form-item label="品牌">
            <el-input v-model="form.brand" />
          </el-form-item>
          <el-form-item label="型号">
            <el-input v-model="form.model" />
          </el-form-item>
          <el-form-item label="实验室" prop="lab_id">
            <el-select v-model="form.lab_id" style="width: 100%">
              <el-option v-for="lab in labs" :key="lab.id" :label="lab.lab_name" :value="lab.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="采购日期">
            <el-date-picker v-model="form.purchase_date" value-format="YYYY-MM-DD" type="date" style="width: 100%" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="form.status" style="width: 100%">
              <el-option label="正常" value="normal" />
              <el-option label="故障" value="faulty" />
              <el-option label="维护中" value="maintenance" />
              <el-option label="已报废" value="scrapped" />
            </el-select>
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
import { equipmentApi } from '../api/equipments'
import { labApi } from '../api/labs'
import { useUserStore } from '../stores/user'
import { equipmentStatusMap, labelOf, tagTypeOf } from '../utils/dicts'

const userStore = useUserStore()
const tableData = ref([])
const labs = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const formRef = ref()
const query = reactive({ page: 1, page_size: 10, keyword: '', lab_id: '', status: '' })
const form = reactive(defaultForm())
const rules = {
  equipment_code: [{ required: true, message: '请输入设备编号', trigger: 'blur' }],
  equipment_name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  category: [{ required: true, message: '请输入类别', trigger: 'blur' }],
  lab_id: [{ required: true, message: '请选择实验室', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

function defaultForm() {
  return { id: null, equipment_code: '', equipment_name: '', category: '', brand: '', model: '', lab_id: '', purchase_date: '', status: 'normal', remark: '' }
}

async function loadLabs() {
  const data = await labApi.list({ page: 1, page_size: 1000, status: 'enabled' })
  labs.value = data.items
}

async function loadData() {
  const data = await equipmentApi.list(query)
  tableData.value = data.items
  total.value = data.total
}

function resetQuery() {
  Object.assign(query, { page: 1, page_size: 10, keyword: '', lab_id: '', status: '' })
  loadData()
}

function openDialog(row) {
  Object.assign(form, defaultForm(), row || {})
  dialogVisible.value = true
}

async function save() {
  await formRef.value.validate()
  if (form.id) await equipmentApi.update(form.id, form)
  else await equipmentApi.create(form)
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadData()
}

async function remove(row) {
  await ElMessageBox.confirm(`确认删除设备 ${row.equipment_name}？`, '删除确认', { type: 'warning' })
  await equipmentApi.remove(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(() => {
  loadLabs()
  loadData()
})
</script>

