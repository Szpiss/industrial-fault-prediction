<script setup lang="ts">
import { RouterLink } from 'vue-router'
defineProps<{ title: string; description: string; items: string[]; stage: string }>()
</script>

<template>
  <div class="page-heading">
    <div>
      <p class="eyebrow">MODULE WORKSPACE</p>
      <h1>{{ title }}</h1>
      <p>{{ description }}</p>
    </div>
    <el-tag effect="plain" type="info">规划中</el-tag>
  </div>
  <section class="panel placeholder-panel">
    <el-empty description="该模块尚未开发，当前为路由与页面占位。" :image-size="100" />
    <div class="planned-scope">
      <h2>预留功能范围</h2>
      <ul>
        <li v-for="item in items" :key="item">{{ item }}</li>
      </ul>
      <p>{{ stage }}</p>
    </div>
    <RouterLink to="/" class="text-link">返回状态总览 →</RouterLink>
  </section>
</template>
