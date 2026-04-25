<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">上报记录</h1>
      <el-button v-if="canCreate" type="primary" :icon="Plus" @click="router.push('/reports/create')">新增上报</el-button>
    </div>

    <div class="toolbar">
      <div class="toolbar-form">
        <el-input v-model="query.keyword" clearable placeholder="上报编号" style="width: 180px" />
        <el-select v-model="query.lab_id" clearable placeholder="实验室" style="width: 210px">
          <el-option v-for="lab in labs" :key="lab.id" :label="lab.lab_name" :value="lab.id" />
        </el-select>
        <el-select v-model="query.review_status" clearable placeholder="审核状态" style="width: 150px">
          <el-option label="待审核" value="pending" />
          <el-option label="已通过" value="approved" />
          <el-option label="已驳回" value="rejected" />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          style="width: 260px"
        />
        <el-select v-model="query.abnormal" clearable placeholder="异常筛选" style="width: 130px">
          <el-option label="异常记录" value="1" />
        </el-select>
        <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
        <el-button :icon="Refresh" @click="resetQuery">重置</el-button>
      </div>
    </div>

    <div class="panel">
      <el-table :data="tableData" border stripe>
        <el-table-column prop="report_no" label="上报编号" width="180" />
        <el-table-column prop="report_date" label="上报日期" width="120" />
        <el-table-column prop="lab_name" label="实验室" min-width="160" />
        <el-table-column prop="reporter_name" label="上报员" width="120" />
        <el-table-column prop="temperature" label="温度" width="90" />
        <el-table-column prop="humidity" label="湿度" width="90" />
        <el-table-column label="设备" width="90">
          <template #default="{ row }">
            <el-tag :type="tagTypeOf(row.equipment_status)">{{ labelOf(normalStatusMap, row.equipment_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="审核状态" width="110">
          <template #default="{ row }">
            <el-tag :type="tagTypeOf(row.review_status)">{{ labelOf(reportStatusMap, row.review_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="abnormal_desc" label="异常描述" min-width="180" show-overflow-tooltip />
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <div class="table-actions">
              <el-button size="small" :icon="View" @click="router.push(`/reports/detail/${row.id}`)">详情</el-button>
              <el-button v-if="canEdit(row)" size="small" :icon="Edit" @click="router.push(`/reports/edit/${row.id}`)">编辑</el-button>
              <el-button v-if="canDelete(row)" size="small" type="danger" :icon="Delete" @click="remove(row)">删除</el-button>
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
  </div>
</template>

<script setup>
import { Delete, Edit, Plus, Refresh, Search, View } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { labApi } from '../api/labs'
import { reportApi } from '../api/reports'
import { useUserStore } from '../stores/user'
import { labelOf, normalStatusMap, reportStatusMap, tagTypeOf } from '../utils/dicts'

const router = useRouter()
const userStore = useUserStore()
const labs = ref([])
const tableData = ref([])
const total = ref(0)
const dateRange = ref([])
const query = reactive({
  page: 1,
  page_size: 10,
  keyword: '',
  lab_id: '',
  review_status: '',
  start_date: '',
  end_date: '',
  abnormal: ''
})

const canCreate = computed(() => ['admin', 'reporter'].includes(userStore.role))

async function loadLabs() {
  const data = await labApi.list({ page: 1, page_size: 1000, status: 'enabled' })
  labs.value = data.items
}

async function loadData() {
  const data = await reportApi.list(query)
  tableData.value = data.items
  total.value = data.total
}

function handleSearch() {
  query.page = 1
  query.start_date = dateRange.value?.[0] || ''
  query.end_date = dateRange.value?.[1] || ''
  loadData()
}

function resetQuery() {
  dateRange.value = []
  Object.assign(query, { page: 1, page_size: 10, keyword: '', lab_id: '', review_status: '', start_date: '', end_date: '', abnormal: '' })
  loadData()
}

function canEdit(row) {
  if (row.review_status !== 'pending') return false
  return userStore.role === 'admin' || row.reporter_id === userStore.user?.id
}

function canDelete(row) {
  if (userStore.role === 'admin') return true
  return row.review_status === 'pending' && row.reporter_id === userStore.user?.id
}

async function remove(row) {
  await ElMessageBox.confirm(`确认删除上报记录 ${row.report_no}？`, '删除确认', { type: 'warning' })
  await reportApi.remove(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(() => {
  loadLabs()
  loadData()
})
</script>

