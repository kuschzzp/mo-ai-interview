<template>
  <div class="space-y-8">
    <div v-if="questions.length === 0"
         class="text-center py-12 backdrop-blur-sm bg-white/40 rounded-2xl border border-white/30">
      <div
          class="w-16 h-16 rounded-full bg-gradient-to-r from-gray-100 to-gray-200 flex items-center justify-center mx-auto mb-4 backdrop-blur-sm">
        <i class="fas fa-question-circle text-gray-400 text-2xl"></i>
      </div>
      <p class="text-gray-500">请先生成问题</p>
    </div>

    <div
        v-for="(q, index) in questions"
        :key="q.id"
        class="backdrop-blur-sm bg-white/60 border border-gray-200/60 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-200"
    >
      <h3 class="font-semibold text-gray-800 mb-4 flex items-start">
				<span
            class="inline-block w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mr-3 mt-1 flex-shrink-0">
					{{ index + 1 }}
				</span>
        {{ q.text }}
      </h3>

      <div class="mb-4">
        <label class="block text-gray-700 mb-2">您的回答：</label>
        <textarea
            class="w-full h-32 border border-gray-300/60 rounded-2xl p-4 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none backdrop-blur-sm bg-white/80 shadow-sm hover:shadow-md transition-all duration-200"
            placeholder="请在此输入您的回答..."
            v-model="answers[q.id]"
        ></textarea>
      </div>

      <div v-if="q.analysis || q.standardAnswer" class="mt-6 pt-6 border-t border-gray-100">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
              class="backdrop-blur-sm bg-gradient-to-br from-purple-50/80 to-indigo-50/80 border border-purple-100/60 rounded-2xl p-6 shadow-lg">
            <h4 class="font-semibold text-gray-800 mb-4 flex items-center">
              <i class="fas fa-robot text-purple-600 mr-2"></i>AI 回答分析
            </h4>
            <div class="space-y-4">
              <div class="flex items-start">
                <i class="fas fa-check-circle text-green-500 mt-1 mr-3"></i>
                <div>
                  <h5 class="font-medium text-gray-800 mb-1">回答评价</h5>
                  <div class="text-gray-700 text-sm" v-html="renderMd(q.analysis)"></div>
                </div>
              </div>
            </div>
          </div>

          <div
              class="backdrop-blur-sm bg-gradient-to-br from-blue-50/80 to-cyan-50/80 border border-blue-100/60 rounded-2xl p-6 shadow-lg">
            <h4 class="font-semibold text-gray-800 mb-4 flex items-center">
              <i class="fas fa-book-open text-blue-600 mr-2"></i>标准参考答案
            </h4>
            <div class="backdrop-blur-sm bg-white/80 border border-blue-200/60 rounded-xl p-4 shadow-sm">
              <div class="text-gray-700 text-sm leading-relaxed" v-html="renderMd(q.standardAnswer)"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-4 flex justify-end">
        <button
            v-if="!q.analysis && !q.standardAnswer"
            class="!rounded-button whitespace-nowrap px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 shadow-lg hover:shadow-xl backdrop-blur-sm"
            @click="analyze(q)"
            :disabled="isAnalyzing(q.id)"
            :class="{ 'opacity-50 cursor-not-allowed': isAnalyzing(q.id) }"
        >
          <i class="fas fa-search mr-2"></i>
          <span v-if="isAnalyzing(q.id)">分析中...</span>
          <span v-else>分析回答</span>
        </button>
        <button
            v-else
            class="!rounded-button whitespace-nowrap px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white hover:from-green-600 hover:to-emerald-600 transition-all duration-200 shadow-lg hover:shadow-xl backdrop-blur-sm"
            @click="analyze(q)"
            :disabled="isAnalyzing(q.id)"
            :class="{ 'opacity-50 cursor-not-allowed': isAnalyzing(q.id) }"
        >
          <i class="fas fa-sync-alt mr-2"></i>
          <span v-if="isAnalyzing(q.id)">重新分析中...</span>
          <span v-else>重新分析</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {reactive, ref, watch} from 'vue';
import {marked} from 'marked';

type Question = { id: string; text: string; answer?: string; analysis?: string; standardAnswer?: string };
const props = defineProps<{ questions: Question[]; analyzingIds?: string[] }>();
const emit = defineEmits<{ (e: 'analyze', payload: { id: string; answer: string }): void }>();

const answers = reactive<Record<string, string>>({});
const active = ref<string | undefined>(undefined);

watch(
    () => props.questions,
    (list) => {
      for (const q of list) {
        answers[q.id] = q.answer || '';
      }
    },
    {immediate: true}
);

function analyze(q: Question) {
  emit('analyze', {id: q.id, answer: answers[q.id] || ''});
}

function isAnalyzing(id: string): boolean {
  return (props.analyzingIds || []).includes(id);
}

function renderMd(src?: string) {
  return marked.parse(src || '');
}

function hasAnswer(q: Question): boolean {
  const val = answers[q.id] ?? q.answer ?? '';
  return !!String(val).trim();
}

function truncate(text: string, max = 40): string {
  if (!text) return '';
  return text.length > max ? text.slice(0, max) + '…' : text;
}
</script>

<style scoped>
.rounded-button {
  border-radius: 0.5rem;
}

/* Markdown 样式 */
:deep(.md) code {
  background: #f6f8fa;
  padding: 2px 6px;
  border-radius: 4px;
}

:deep(.md) pre {
  background: #0b1021;
  color: #e6edf5;
  padding: 12px;
  border-radius: 6px;
  overflow: auto;
}
</style>


