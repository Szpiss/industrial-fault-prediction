<script setup lang="ts">
import ModulePlaceholder from '../components/ModulePlaceholder.vue'
const items = ['故障风险阈值配置', '告警事件与处理状态', '告警历史查询']
</script>

<template>
  <ModulePlaceholder
    title="告警管理"
    description="为设备风险阈值与告警处理预留入口。"
    :items="items"
    stage="待预测结果接口稳定后开发。"
  />
</template>
