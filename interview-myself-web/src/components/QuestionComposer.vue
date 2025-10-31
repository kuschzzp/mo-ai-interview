<template>
  <div class="mb-8">
    <h3 class="text-lg font-semibold text-gray-700 mb-4">问题生成器</h3>
    <p class="text-gray-600 mb-4">选择条目后填入下方，可修改后生成问题</p>

    <textarea
        v-model="topic"
        class="w-full h-32 border border-gray-300/60 rounded-2xl p-4 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none mb-4 backdrop-blur-sm bg-white/80 shadow-lg hover:shadow-xl transition-all duration-200"
        placeholder="选择某一条后会填入这里，支持自由编辑"
    ></textarea>

    <div class="flex justify-end gap-3">
      <button
          class="!rounded-button whitespace-nowrap px-4 py-2 bg-gradient-to-r from-gray-500 to-gray-600 text-white hover:from-gray-600 hover:to-gray-700 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
          @click="$emit('back-to-outline')"
      >
        <i class="fas fa-list mr-2"></i>重新选择大纲
      </button>
      <button
          class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
          @click="emitGen"
          :disabled="!topic.trim() || loading"
          :class="{ 'opacity-50 cursor-not-allowed': !topic.trim() || loading }"
      >
        <i class="fas fa-magic mr-2"></i>
        <span v-if="loading">生成中...</span>
        <span v-else>生成问题</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, watch} from 'vue';

const props = defineProps<{ selected: string; loading?: boolean }>();
const emit = defineEmits<{
  (e: 'gen-questions', topic: string): void;
  (e: 'back-to-outline'): void;
}>();

const topic = ref('');
watch(
    () => props.selected,
    (v) => {
      topic.value = v || '';
    },
    {immediate: true}
);

function emitGen() {
  emit('gen-questions', topic.value.trim());
}
</script>

<style scoped>
.rounded-button {
  border-radius: 0.5rem;
}
</style>


