<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">首页统计</h1>
      <el-button :icon="Refresh" @click="loadData">刷新</el-button>
    </div>

    <div class="stat-grid">
      <StatCard label="上报总数" :value="cards.total" :icon="Files" color="#2563eb" />
      <StatCard label="待审核数量" :value="cards.pending" :icon="Clock" color="#d97706" />
      <StatCard label="已通过数量" :value="cards.approved" :icon="CircleCheck" color="#059669" />
      <StatCard label="被驳回数量" :value="cards.rejected" :icon="CircleClose" color="#dc2626" />
      <StatCard label="异常上报数量" :value="cards.abnormal" :icon="Warning" color="#7c3aed" />
    </div>

    <div class="chart-grid">
      <div class="panel">
        <h2>按日期统计上报趋势</h2>
        <EChart :option="trendOption" />
      </div>
      <div class="panel">
        <h2>设备状态分布</h2>
        <EChart :option="deviceOption" />
      </div>
    </div>

    <div class="panel">
      <h2>按实验室统计上报数</h2>
      <EChart :option="labOption" />
    </div>
  </div>
</template>

<script setup>
import { CircleCheck, CircleClose, Clock, Files, Refresh, Warning } from '@element-plus/icons-vue'
import { computed, onMounted, ref } from 'vue'
import EChart from '../components/EChart.vue'
import StatCard from '../components/StatCard.vue'
import { getDashboard } from '../api/dashboard'
import { equipmentStatusMap, labelOf } from '../utils/dicts'

const cards = ref({ total: 0, pending: 0, approved: 0, rejected: 0, abnormal: 0 })
const labStats = ref([])
const trend = ref([])
const deviceStatus = ref([])

const trendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 36, right: 20, top: 28, bottom: 34 },
  xAxis: { type: 'category', data: trend.value.map((item) => item.date) },
  yAxis: { type: 'value', minInterval: 1 },
  series: [
    {
      name: '上报数量',
      type: 'line',
      smooth: true,
      areaStyle: { opacity: 0.12 },
      data: trend.value.map((item) => item.count),
      itemStyle: { color: '#2563eb' }
    }
  ]
}))

const labOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 36, right: 20, top: 28, bottom: 30 },
  xAxis: { type: 'category', data: labStats.value.map((item) => item.name) },
  yAxis: { type: 'value', minInterval: 1 },
  series: [
    {
      name: '上报数',
      type: 'bar',
      barWidth: 34,
      data: labStats.value.map((item) => item.value),
      itemStyle: { color: '#10b981', borderRadius: [4, 4, 0, 0] }
    }
  ]
}))

const deviceOption = computed(() => ({
  tooltip: { trigger: 'item' },
  legend: { bottom: 0 },
  series: [
    {
      name: '设备状态',
      type: 'pie',
      radius: ['42%', '68%'],
      center: ['50%', '46%'],
      data: deviceStatus.value.map((item) => ({
        name: labelOf(equipmentStatusMap, item.name),
        value: item.value
      }))
    }
  ]
}))

async function loadData() {
  const data = await getDashboard()
  cards.value = data.cards
  labStats.value = data.lab_stats
  trend.value = data.trend
  deviceStatus.value = data.device_status
}

onMounted(loadData)
</script>

<style scoped>
.stat-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(150px, 1fr));
  gap: 16px;
}

.panel h2 {
  margin: 0 0 12px;
  font-size: 17px;
}

@media (max-width: 1180px) {
  .stat-grid {
    grid-template-columns: repeat(2, minmax(180px, 1fr));
  }
}
</style>

