<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">审核管理</h1>
    </div>

    <div class="toolbar">
      <div class="toolbar-form">
        <el-select v-model="query.review_status" placeholder="审核状态" style="width: 150px">
          <el-option label="待审核" value="pending" />
          <el-option label="已通过" value="approved" />
          <el-option label="已驳回" value="rejected" />
        </el-select>
        <el-button type="primary" :icon="Search" @click="loadData">查询</el-button>
        <el-button :icon="Refresh" @click="resetQuery">重置</el-button>
      </div>
    </div>

    <div class="panel">
      <el-table :data="tableData" border stripe>
        <el-table-column prop="report_no" label="上报编号" width="180" />
        <el-table-column prop="report_date" label="上报日期" width="120" />
        <el-table-column prop="lab_name" label="实验室" min-width="160" />
        <el-table-column prop="reporter_name" label="上报员" width="120" />
        <el-table-column label="审核状态" width="110">
          <template #default="{ row }">
            <el-tag :type="tagTypeOf(row.review_status)">{{ labelOf(reportStatusMap, row.review_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="abnormal_desc" label="异常描述" min-width="220" show-overflow-tooltip />
        <el-table-column label="操作" width="230" fixed="right">
          <template #default="{ row }">
            <div class="table-actions">
              <el-button size="small" :icon="View" @click="router.push(`/reports/detail/${row.id}`)">详情</el-button>
              <el-button v-if="row.review_status === 'pending'" size="small" type="primary" :icon="Checked" @click="openAudit(row)">审核</el-button>
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

    <el-dialog v-model="dialogVisible" title="审核上报记录" width="560px">
      <el-form ref="formRef" :model="auditForm" :rules="rules" label-width="90px">
        <el-form-item label="审核结果" prop="review_status">
          <el-radio-group v-model="auditForm.review_status">
            <el-radio-button label="approved">通过</el-radio-button>
            <el-radio-button label="rejected">驳回</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="审核意见" prop="review_comment">
          <el-input v-model="auditForm.review_comment" type="textarea" :rows="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitAudit">提交审核</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { Checked, Refresh, Search, View } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { reviewApi } from '../api/reviews'
import { labelOf, reportStatusMap, tagTypeOf } from '../utils/dicts'

const router = useRouter()
const tableData = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const currentRow = ref(null)
const formRef = ref()
const query = reactive({ page: 1, page_size: 10, review_status: 'pending' })
const auditForm = reactive({ review_status: 'approved', review_comment: '审核通过。' })
const rules = {
  review_status: [{ required: true, message: '请选择审核结果', trigger: 'change' }],
  review_comment: [{ required: true, message: '请输入审核意见', trigger: 'blur' }]
}

async function loadData() {
  const data = await reviewApi.list(query)
  tableData.value = data.items
  total.value = data.total
}

function resetQuery() {
  Object.assign(query, { page: 1, page_size: 10, review_status: 'pending' })
  loadData()
}

function openAudit(row) {
  currentRow.value = row
  Object.assign(auditForm, { review_status: 'approved', review_comment: '审核通过。' })
  dialogVisible.value = true
}

async function submitAudit() {
  await formRef.value.validate()
  await reviewApi.audit(currentRow.value.id, auditForm)
  ElMessage.success('审核完成')
  dialogVisible.value = false
  loadData()
}

onMounted(loadData)
</script>

