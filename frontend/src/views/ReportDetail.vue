<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">上报详情</h1>
      <el-button :icon="Back" @click="router.back()">返回</el-button>
    </div>

    <div class="panel" v-if="detail">
      <el-descriptions title="基础信息" :column="2" border>
        <el-descriptions-item label="上报编号">{{ detail.report_no }}</el-descriptions-item>
        <el-descriptions-item label="上报日期">{{ detail.report_date }}</el-descriptions-item>
        <el-descriptions-item label="实验室">{{ detail.lab_name }}</el-descriptions-item>
        <el-descriptions-item label="上报员">{{ detail.reporter_name }}</el-descriptions-item>
        <el-descriptions-item label="温度">{{ detail.temperature }}</el-descriptions-item>
        <el-descriptions-item label="湿度">{{ detail.humidity }}</el-descriptions-item>
        <el-descriptions-item label="使用人数/次数">{{ detail.usage_count }}</el-descriptions-item>
        <el-descriptions-item label="审核状态">
          <el-tag :type="tagTypeOf(detail.review_status)">{{ labelOf(reportStatusMap, detail.review_status) }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <el-descriptions title="状态检查" :column="3" border class="detail-block">
        <el-descriptions-item label="卫生">{{ labelOf(normalStatusMap, detail.hygiene_status) }}</el-descriptions-item>
        <el-descriptions-item label="电力">{{ labelOf(normalStatusMap, detail.power_status) }}</el-descriptions-item>
        <el-descriptions-item label="网络">{{ labelOf(normalStatusMap, detail.network_status) }}</el-descriptions-item>
        <el-descriptions-item label="门窗">{{ labelOf(normalStatusMap, detail.door_window_status) }}</el-descriptions-item>
        <el-descriptions-item label="消防">{{ labelOf(normalStatusMap, detail.fire_status) }}</el-descriptions-item>
        <el-descriptions-item label="设备">{{ labelOf(normalStatusMap, detail.equipment_status) }}</el-descriptions-item>
      </el-descriptions>

      <el-descriptions title="异常与审核" :column="1" border class="detail-block">
        <el-descriptions-item label="异常描述">{{ detail.abnormal_desc || '无' }}</el-descriptions-item>
        <el-descriptions-item label="附件">
          <el-link v-if="detail.attachment_path" :href="detail.attachment_path" type="primary" target="_blank">查看附件</el-link>
          <span v-else>无</span>
        </el-descriptions-item>
        <el-descriptions-item label="审核人">{{ detail.reviewer_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ detail.review_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审核意见">{{ detail.review_comment || '-' }}</el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<script setup>
import { Back } from '@element-plus/icons-vue'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { reportApi } from '../api/reports'
import { labelOf, normalStatusMap, reportStatusMap, tagTypeOf } from '../utils/dicts'

const route = useRoute()
const router = useRouter()
const detail = ref(null)

async function loadDetail() {
  detail.value = await reportApi.detail(route.params.id)
}

onMounted(loadDetail)
</script>

<style scoped>
.detail-block {
  margin-top: 18px;
}
</style>

