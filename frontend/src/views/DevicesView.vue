<script setup lang="ts">
import ModulePlaceholder from '../components/ModulePlaceholder.vue'
const items = ['设备基本信息与分类', '设备运行状态与维护记录', '设备信息查询与编辑']
</script>

<template>
  <ModulePlaceholder
    title="设备管理"
    description="为设备台账与运行状态管理预留统一入口。"
    :items="items"
    stage="建议作为下一阶段的首个业务模块。"
  />
</template>
