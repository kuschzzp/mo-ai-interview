<template>
  <div>
    <main class="container mx-auto px-6 py-8">
      <!-- Question Generation & Analysis -->
      <section class="backdrop-blur-md bg-white/70 rounded-2xl shadow-xl p-8 border border-white/30">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <span
              class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white flex items-center justify-center mr-3 backdrop-blur-sm">3</span>
          问题生成与回答分析
        </h2>

        <div class="mb-6 p-4 backdrop-blur-sm bg-blue-50/80 rounded-xl border border-blue-100/60">
          <h3 class="font-semibold text-gray-800 mb-2">当前大纲：</h3>
          <p class="text-gray-700">{{ selectedOutline }}</p>
        </div>

        <QuestionComposer
            :selected="selectedOutline"
            :loading="loadingQuestions"
            @gen-questions="onGenerateQuestions"
            @back-to-outline="$emit('back-to-outline')"
        />

        <QuestionList
            :questions="questions"
            :analyzing-ids="Array.from(loadingAnalyzeIds)"
            @analyze="onAnalyze"
        />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import QuestionComposer from './QuestionComposer.vue';
import QuestionList from './QuestionList.vue';

type Question = {
  id: string;
  text: string;
  answer?: string;
  analysis?: string;
  standardAnswer?: string;
};

const props = defineProps<{
  selectedOutline: string;
  questions: Question[];
  loadingQuestions: boolean;
  loadingAnalyzeIds: Set<string>;
}>();

const emit = defineEmits<{
  (e: 'back-to-outline'): void;
  (e: 'generate-questions', topic: string): void;
  (e: 'analyze', payload: { id: string; answer: string }): void;
}>();

async function onGenerateQuestions(topic: string) {
  emit('generate-questions', topic);
}

async function onAnalyze(q: { id: string; answer: string }) {
  emit('analyze', q);
}
</script>

<style scoped>
.rounded-button {
  border-radius: 0.5rem;
}
</style>
