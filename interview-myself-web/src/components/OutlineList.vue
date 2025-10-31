<template>
  <div>

    <div v-if="!outline.length"
         class="text-center py-12 backdrop-blur-sm bg-white/40 rounded-2xl border border-white/30">
      <div
          class="w-16 h-16 rounded-full bg-gradient-to-r from-gray-100 to-gray-200 flex items-center justify-center mx-auto mb-4 backdrop-blur-sm">
        <i class="fas fa-list text-gray-400 text-2xl"></i>
      </div>
      <p class="text-gray-500 mb-4">暂无面试大纲</p>
      <button
          class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 flex items-center mx-auto shadow-lg hover:shadow-xl backdrop-blur-sm"
          @click="$emit('gen-outline')"
          :disabled="loading"
          :class="{ 'opacity-50 cursor-not-allowed': loading }"
      >
        <i class="fas fa-magic mr-2"></i>
        <span v-if="loading">生成中...</span>
        <span v-else>生成面试大纲</span>
      </button>
    </div>

    <div v-else class="space-y-4">
      <!-- 重新生成按钮 -->
      <div class="flex justify-end mb-4">
        <button
            class="!rounded-button whitespace-nowrap px-4 py-2 bg-gradient-to-r from-gray-500 to-gray-600 text-white hover:from-gray-600 hover:to-gray-700 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
            @click="$emit('gen-outline')"
            :disabled="loading"
            :class="{ 'opacity-50 cursor-not-allowed': loading }"
        >
          <i class="fas fa-sync-alt mr-2"></i>
          <span v-if="loading">重新生成中...</span>
          <span v-else>重新生成大纲</span>
        </button>
      </div>

      <div
          v-for="(item, index) in outline"
          :key="index"
          class="outline-item backdrop-blur-sm bg-white/60 border border-gray-200/60 rounded-2xl p-5 hover:shadow-xl transition-all duration-200 cursor-pointer"
          :class="{ 'border-blue-500/80 bg-blue-50/60 shadow-lg': selectedOutline === index }"
          @click="selectOutline(index)"
      >
        <div class="flex items-start">
          <input
              type="radio"
              class="mt-1 mr-4 h-5 w-5 text-blue-600 focus:ring-blue-500"
              :name="'outline-selection'"
              :checked="selectedOutline === index"
              @click.stop
          >
          <div class="flex-1">
            <h3 class="font-semibold text-gray-800 mb-2">{{ item }}</h3>
            <p class="text-gray-600 text-sm">{{ item }}</p>
          </div>
          <div class="ml-4">
            <button
                class="!rounded-button whitespace-nowrap px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 text-sm shadow-lg hover:shadow-xl backdrop-blur-sm"
                @click.stop="$emit('select-outline', item)"
            >
              <i class="fas fa-check mr-1"></i>选择
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, watch} from 'vue';

const props = defineProps<{ outline: string[]; loading?: boolean; selectedOutline?: string }>();
const emit = defineEmits<{
  (e: 'select-outline', item: string): void;
  (e: 'gen-outline'): void;
}>();

const selectedOutline = ref<number | null>(null);

// 监听selectedOutline prop的变化，更新本地选中状态
watch(() => props.selectedOutline, (newSelected) => {
  if (newSelected && props.outline.length > 0) {
    const index = props.outline.findIndex(item => item === newSelected);
    selectedOutline.value = index >= 0 ? index : null;
  } else {
    selectedOutline.value = null;
  }
}, {immediate: true});

const selectOutline = (index: number) => {
  selectedOutline.value = index;
  // 立即触发选择事件并跳转
  emit('select-outline', props.outline[index]);
};
</script>

<style scoped>
.rounded-button {
  border-radius: 0.5rem;
}
</style>


