<template>
  <div class="stat-card">
    <div class="stat-icon" :style="{ background: color }">
      <component :is="icon" />
    </div>
    <div>
      <div class="stat-label">{{ label }}</div>
      <div class="stat-value">{{ value }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: Number, default: 0 },
  icon: { type: Object, required: true },
  color: { type: String, default: '#2563eb' }
})
</script>

<style scoped>
.stat-card {
  min-height: 96px;
  display: flex;
  align-items: center;
  gap: 14px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 18px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  color: #ffffff;
  border-radius: 8px;
  display: grid;
  place-items: center;
  flex: 0 0 48px;
}

.stat-icon :deep(svg) {
  width: 24px;
  height: 24px;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
}

.stat-value {
  margin-top: 6px;
  font-size: 28px;
  line-height: 1;
  font-weight: 800;
  color: #111827;
}
</style>

