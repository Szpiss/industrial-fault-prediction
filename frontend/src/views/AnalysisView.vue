<script setup lang="ts">
import ModulePlaceholder from '../components/ModulePlaceholder.vue'
const items = ['CSV / 时序数据导入', '缺失值处理与数据质量校验', '特征工程与数据可视化']
</script>

<template>
  <ModulePlaceholder
    title="数据分析"
    description="为传感器数据导入与分析预留工作空间。"
    :items="items"
    stage="待设备数据结构确定后逐步开发。"
  />
</template>
