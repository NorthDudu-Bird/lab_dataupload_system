<template>
  <div ref="chartRef" class="echart"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { nextTick, onBeforeUnmount, onMounted, watch, ref } from 'vue'

const props = defineProps({
  option: {
    type: Object,
    required: true
  }
})

const chartRef = ref()
let chart = null

function renderChart() {
  if (!chartRef.value) return
  if (!chart) {
    chart = echarts.init(chartRef.value)
  }
  chart.setOption(props.option, true)
}

function resizeChart() {
  chart?.resize()
}

onMounted(async () => {
  await nextTick()
  renderChart()
  window.addEventListener('resize', resizeChart)
})

watch(
  () => props.option,
  () => nextTick(renderChart),
  { deep: true }
)

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  chart?.dispose()
})
</script>

<style scoped>
.echart {
  width: 100%;
  height: 340px;
}
</style>

