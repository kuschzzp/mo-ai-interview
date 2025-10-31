<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <!-- Resume Upload -->
    <div
        class="backdrop-blur-sm bg-white/60 border-2 border-dashed border-gray-300/60 rounded-2xl p-8 text-center transition-all duration-200 hover:border-blue-400/80 hover:bg-blue-50/40 shadow-lg hover:shadow-xl">
      <div class="flex justify-center mb-4">
        <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center">
          <i class="fas fa-file-pdf text-blue-600 text-2xl"></i>
        </div>
      </div>
      <h3 class="text-lg font-semibold text-gray-700 mb-2">上传 PDF 简历</h3>
      <p class="text-gray-500 mb-4">拖拽文件到此处或点击选择文件</p>

      <el-upload
          class="uploader"
          :auto-upload="false"
          :show-file-list="true"
          v-model:file-list="fileList"
          accept="application/pdf"
          :on-change="onElFile"
      >
        <button
            class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 mb-4 shadow-lg hover:shadow-xl backdrop-blur-sm">
          <i class="fas fa-upload mr-2"></i>选择文件
        </button>
      </el-upload>

      <p class="text-sm text-gray-400">
        <i class="fas fa-info-circle mr-1"></i>
        支持 PDF 格式，文件大小不超过 10MB
      </p>
    </div>

    <!-- Job Description -->
    <div>
      <h3 class="text-lg font-semibold text-gray-700 mb-4 flex items-center">
        <i class="fas fa-briefcase text-blue-600 mr-2"></i>
        目标岗位描述
      </h3>
      <div class="relative">
				<textarea
            v-model="jobGoal"
            class="w-full h-64 border-2 border-gray-200/60 rounded-2xl p-4 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none transition-all duration-200 shadow-lg hover:shadow-xl backdrop-blur-sm bg-white/80"
            placeholder="请详细描述您申请的目标岗位要求，包括：&#10;&#10;📋 岗位职责&#10;💼 所需技能&#10;🎯 工作经验要求&#10;🎓 学历背景&#10;🏢 公司行业特点&#10;&#10;越详细越好，AI会根据这些信息为您生成更精准的面试准备内容..."
        ></textarea>
        <div class="absolute bottom-3 right-3 text-xs text-gray-400 bg-white/80 backdrop-blur-sm px-2 py-1 rounded">
          {{ jobGoal.length }}/1000
        </div>
      </div>
      <div class="mt-3 text-sm text-gray-500">
        <i class="fas fa-lightbulb text-yellow-500 mr-1"></i>
        <strong>小贴士：</strong>详细描述岗位要求有助于AI生成更精准的面试大纲和问题
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, ref, watch} from 'vue';
import type {UploadFile} from 'element-plus';

const props = defineProps<{ loading?: boolean; jobGoal?: string; fileList?: any[] }>();
const emit = defineEmits<{
  (e: 'request-generate', payload: { resume?: File; jobGoal: string }): void;
  (e: 'update:jobGoal', value: string): void;
  (e: 'update:file-list', value: any[]): void;
  (e: 'file-selected', file: File): void;
}>();

const resume = ref<File>();
const jobGoal = ref(props.jobGoal || '');
const fileList = ref<any[]>(props.fileList || []);

const canGen = computed(() => !!jobGoal.value && !!resume.value);

// 双向绑定 jobGoal
watch(jobGoal, (v) => emit('update:jobGoal', v));
watch(fileList, (v) => emit('update:file-list', v), {deep: true});

function onFile(e: Event) {
  const input = e.target as HTMLInputElement;
  if (input && input.files && input.files.length > 0) {
    const f = input.files[0];
    if (f.type === 'application/pdf') {
      resume.value = f;
    }
  }
}

function onElFile(file: UploadFile) {
  // el-upload on-change 回调
  if (file && file.raw && file.raw.type === 'application/pdf') {
    resume.value = file.raw;
    emit('file-selected', file.raw);
  }
}

function emitRequest() {
  const g = jobGoal.value.trim();
  emit('request-generate', {resume: resume.value, jobGoal: g});
}
</script>

<style scoped>
.rounded-button {
  border-radius: 0.5rem;
}

.uploader :deep(.el-upload) {
  display: block;
}

.uploader :deep(.el-upload-list) {
  margin-top: 8px;
}
</style>


