<template>
  <div v-if="intro" class="mt-8 p-6 bg-blue-50 rounded-lg border border-blue-100">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-lg font-semibold text-gray-800">为您生成的个性化自我介绍：</h3>
      <button
          class="!rounded-button whitespace-nowrap px-3 py-1 bg-blue-600 text-white hover:bg-blue-700 transition-colors text-sm"
          @click="copy"
      >
        <i class="fas fa-copy mr-1"></i>复制
      </button>
    </div>
    <p class="text-gray-700 whitespace-pre-line">{{ intro }}</p>
  </div>
  <div v-else class="mt-8 p-6 bg-gray-50 rounded-lg border border-gray-200 text-center">
    <div class="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-3">
      <i class="fas fa-user text-gray-400 text-xl"></i>
    </div>
    <p class="text-gray-500">请先在上方生成自我介绍</p>
  </div>
</template>

<script setup lang="ts">
import {ElMessage} from 'element-plus';

const props = defineProps<{ intro: string }>();

async function copy() {
  try {
    await navigator.clipboard.writeText(props.intro || '');
    ElMessage.success('已复制到剪贴板');
  } catch {
    ElMessage.error('复制失败');
  }
}
</script>

<style scoped>
.rounded-button {
  border-radius: 0.5rem;
}
</style>


