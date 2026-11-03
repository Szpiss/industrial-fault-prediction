<script setup lang="ts">
import ModulePlaceholder from '../components/ModulePlaceholder.vue'
const items = [
  'Logistic Regression、SVM、XGBoost 基线对比',
  '模型版本与评估指标',
  'LSTM 时序预测与风险评分',
]
</script>

<template>
  <ModulePlaceholder
    title="故障预测"
    description="为模型评估、故障风险评分与预测结果预留入口。"
    :items="items"
    stage="未安装重量级机器学习依赖，尚未训练或接入模型。"
  />
</template>
