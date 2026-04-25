<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">{{ isEdit ? '编辑上报' : '新增上报' }}</h1>
      <el-button :icon="Back" @click="router.back()">返回</el-button>
    </div>

    <div class="panel">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <div class="form-grid">
          <el-form-item label="上报日期" prop="report_date">
            <el-date-picker v-model="form.report_date" value-format="YYYY-MM-DD" type="date" style="width: 100%" />
          </el-form-item>
          <el-form-item label="实验室" prop="lab_id">
            <el-select v-model="form.lab_id" filterable style="width: 100%">
              <el-option v-for="lab in labs" :key="lab.id" :label="lab.lab_name" :value="lab.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="温度" prop="temperature">
            <el-input-number v-model="form.temperature" :precision="2" :step="0.1" style="width: 100%" />
          </el-form-item>
          <el-form-item label="湿度" prop="humidity">
            <el-input-number v-model="form.humidity" :precision="2" :step="0.1" style="width: 100%" />
          </el-form-item>
          <el-form-item label="使用人数/次数" prop="usage_count">
            <el-input-number v-model="form.usage_count" :min="0" style="width: 100%" />
          </el-form-item>
          <el-form-item label="卫生状态" prop="hygiene_status">
            <el-select v-model="form.hygiene_status" style="width: 100%">
              <el-option label="正常" value="normal" />
              <el-option label="异常" value="abnormal" />
            </el-select>
          </el-form-item>
          <el-form-item label="电力状态" prop="power_status">
            <el-select v-model="form.power_status" style="width: 100%">
              <el-option label="正常" value="normal" />
              <el-option label="异常" value="abnormal" />
            </el-select>
          </el-form-item>
          <el-form-item label="网络状态" prop="network_status">
            <el-select v-model="form.network_status" style="width: 100%">
              <el-option label="正常" value="normal" />
              <el-option label="异常" value="abnormal" />
            </el-select>
          </el-form-item>
          <el-form-item label="门窗状态" prop="door_window_status">
            <el-select v-model="form.door_window_status" style="width: 100%">
              <el-option label="正常" value="normal" />
              <el-option label="异常" value="abnormal" />
            </el-select>
          </el-form-item>
          <el-form-item label="消防状态" prop="fire_status">
            <el-select v-model="form.fire_status" style="width: 100%">
              <el-option label="正常" value="normal" />
              <el-option label="异常" value="abnormal" />
            </el-select>
          </el-form-item>
          <el-form-item label="设备状态" prop="equipment_status">
            <el-select v-model="form.equipment_status" style="width: 100%">
              <el-option label="正常" value="normal" />
              <el-option label="异常" value="abnormal" />
            </el-select>
          </el-form-item>
          <el-form-item class="full-row" label="异常描述">
            <el-input v-model="form.abnormal_desc" type="textarea" :rows="4" placeholder="如无异常可留空" />
          </el-form-item>
          <el-form-item class="full-row" label="附件">
            <div class="upload-line">
              <el-upload :http-request="handleUpload" :show-file-list="false">
                <el-button :icon="Upload">上传附件</el-button>
              </el-upload>
              <el-link v-if="form.attachment_path" :href="form.attachment_path" target="_blank" type="primary">
                {{ form.attachment_path }}
              </el-link>
            </div>
          </el-form-item>
        </div>
      </el-form>
      <div class="form-footer">
        <el-button @click="router.back()">取消</el-button>
        <el-button type="primary" :loading="saving" @click="submit">提交保存</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Back, Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { labApi } from '../api/labs'
import { reportApi } from '../api/reports'

const route = useRoute()
const router = useRouter()
const formRef = ref()
const saving = ref(false)
const labs = ref([])
const isEdit = computed(() => Boolean(route.params.id))
const form = reactive(defaultForm())

const rules = {
  report_date: [{ required: true, message: '请选择上报日期', trigger: 'change' }],
  lab_id: [{ required: true, message: '请选择实验室', trigger: 'change' }],
  temperature: [{ required: true, message: '请输入温度', trigger: 'blur' }],
  humidity: [{ required: true, message: '请输入湿度', trigger: 'blur' }],
  usage_count: [{ required: true, message: '请输入使用人数或次数', trigger: 'blur' }]
}

function defaultForm() {
  const today = new Date().toISOString().slice(0, 10)
  return {
    report_date: today,
    lab_id: '',
    temperature: 23,
    humidity: 50,
    hygiene_status: 'normal',
    power_status: 'normal',
    network_status: 'normal',
    door_window_status: 'normal',
    fire_status: 'normal',
    equipment_status: 'normal',
    usage_count: 0,
    abnormal_desc: '',
    attachment_path: ''
  }
}

async function loadLabs() {
  const data = await labApi.list({ page: 1, page_size: 1000, status: 'enabled' })
  labs.value = data.items
}

async function loadDetail() {
  if (!isEdit.value) return
  const data = await reportApi.detail(route.params.id)
  if (data.review_status !== 'pending') {
    ElMessage.warning('已审核记录不能修改')
    router.replace(`/reports/detail/${route.params.id}`)
    return
  }
  Object.assign(form, data)
}

async function handleUpload(option) {
  const formData = new FormData()
  formData.append('file', option.file)
  try {
    const data = await reportApi.upload(formData)
    form.attachment_path = data.file_path
    option.onSuccess(data)
    ElMessage.success('上传成功')
  } catch (error) {
    option.onError(error)
  }
}

async function submit() {
  await formRef.value.validate()
  saving.value = true
  try {
    if (isEdit.value) {
      await reportApi.update(route.params.id, form)
      ElMessage.success('更新成功')
    } else {
      await reportApi.create(form)
      ElMessage.success('提交成功')
    }
    router.push('/reports')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadLabs()
  loadDetail()
})
</script>

<style scoped>
.upload-line {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.form-footer {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
