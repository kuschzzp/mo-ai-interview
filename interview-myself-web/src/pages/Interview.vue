<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <!-- Header -->
    <header class="backdrop-blur-md bg-white/90 shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="container mx-auto px-6 py-2 flex items-center justify-between min-h-[48px]">
        <router-link
          to="/"
          class="rounded-full px-3 py-1 bg-gradient-to-r from-gray-600 to-gray-700 text-white hover:from-gray-700 hover:to-gray-800 transition-all text-xs shadow-md hover:shadow-lg flex items-center"
        >
          <i class="fas fa-arrow-left mr-1 text-xs"></i> 返回
        </router-link>
        <div class="flex items-center gap-2">
          <i class="fas fa-robot text-indigo-600 text-lg"></i>
          <h1 class="text-base font-semibold text-gray-800 tracking-tight">AI 面试助手</h1>
          <span class="ml-2 text-xs bg-blue-100/80 text-blue-700 px-2 py-0.5 rounded-full backdrop-blur-sm font-normal">Beta</span>
        </div>
        <div class="w-14"></div>
      </div>
    </header>

    <!-- Progress Bar -->
    <div class="container mx-auto px-6 py-6">
      <div class="backdrop-blur-sm bg-white/60 rounded-2xl p-6 shadow-lg border border-white/30">
        <div class="flex justify-between relative">
          <!-- 进度条背景线 -->
          <div class="absolute top-6 left-6 right-6 h-2 bg-gray-200/60 -z-10 rounded-full"></div>
          <!-- 进度条进度线 -->
          <div
              class="absolute top-6 left-6 h-2 bg-gradient-to-r from-blue-500 to-indigo-500 -z-10 transition-all duration-500 rounded-full"
              :style="progressStyle"
          ></div>
          <!-- 步骤按钮 -->
          <div
              v-for="(step, index) in steps"
              :key="index"
              class="flex flex-col items-center relative z-10"
          >
            <div
                class="w-12 h-12 rounded-full flex items-center justify-center mb-2 transition-all duration-300 backdrop-blur-sm"
                :class="{
                                'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-lg': state.currentStep >= index,
                                'bg-white/80 border-2 border-gray-300/60 text-gray-400 shadow-sm': state.currentStep < index
                            }"
            >
              <i :class="step.icon"></i>
            </div>
            <span class="text-sm font-medium text-gray-600">{{ step.title }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主页面：四步流程 -->
    <main class="container mx-auto px-6 py-8 pb-20 space-y-8">
      <!-- Step 1: 个人信息补充（上传简历 + 岗位需求） -->
      <section v-if="state.currentStep === 0"
          class="backdrop-blur-md bg-white/70 rounded-2xl shadow-xl p-8 transition-all duration-300 border border-white/30"
      >
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <span class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white flex items-center justify-center mr-3 backdrop-blur-sm">1</span>
          个人信息补充
        </h2>

        <UploadAndGoal
            v-model:jobGoal="state.jobGoal"
            v-model:file-list="state.resumeFileList"
            :loading="state.loadingIntro"
            @file-selected="(f: File) => (state.resumePdf = f)"
        />

        <div class="mt-8 flex justify-end">
          <button
              class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
              @click="goToStep(1)"
              :disabled="!state.resumePdf || !state.jobGoal"
              :class="{ 'opacity-50 cursor-not-allowed': !state.resumePdf || !state.jobGoal }"
          >
            进入下一步
            <i class="fas fa-arrow-right ml-2"></i>
          </button>
        </div>
      </section>

      <!-- Step 2: 生成自我介绍 -->
      <section v-if="state.currentStep === 1"
          class="backdrop-blur-md bg-white/70 rounded-2xl shadow-xl p-8 transition-all duration-300 border border-white/30"
      >
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <span class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white flex items-center justify-center mr-3 backdrop-blur-sm">2</span>
          生成自我介绍
        </h2>

        <div class="flex flex-wrap gap-3 mb-6">
          <button
              class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white hover:from-gray-600 hover:to-gray-700 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
              @click="goBackToInfo()"
          >
            <i class="fas fa-arrow-left mr-2"></i>返回上一步
          </button>
          <button
              class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
              @click="onGenerateSelfIntro"
              :disabled="state.selfIntroStreaming || !state.resumePdf || !state.jobGoal"
              :class="{ 'opacity-50 cursor-not-allowed': state.selfIntroStreaming || !state.resumePdf || !state.jobGoal }"
          >
            <i v-if="state.selfIntroStreaming" class="fas fa-spinner fa-spin mr-2"></i>
            <i v-else-if="state.selfIntro" class="fas fa-sync-alt mr-2"></i>
            <i v-else class="fas fa-magic mr-2"></i>
            <span v-if="state.selfIntroStreaming">生成中...</span>
            <span v-else-if="state.selfIntro">重新生成自我介绍</span>
            <span v-else>生成自我介绍</span>
          </button>
          <button
              v-if="state.selfIntro"
              class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white hover:from-green-600 hover:to-emerald-600 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
              @click="goToStep(2)"
          >
            进入下一步<i class="fas fa-arrow-right ml-2"></i>
          </button>
        </div>

        <!-- 流动区: 生成中实时增量 -->
        <div
          v-if="state.selfIntroStreaming && state.selfIntroStreamText"
          class="p-6 mb-3 bg-blue-50 rounded-xl border border-blue-200/70 animate-pulse shadow text-blue-800 overflow-auto max-h-80"
        >
          <div class="text-xs text-blue-700 mb-2">生成中...</div>
          <div class="whitespace-pre-line font-mono text-[15px] leading-relaxed">{{ state.selfIntroStreamText }}</div>
        </div>
        <!-- 最终区 -->
        <div v-if="state.selfIntro && !state.selfIntroStreaming" class="p-6 backdrop-blur-sm bg-blue-50/80 rounded-xl border border-blue-200/50">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-semibold text-gray-800">为您生成的个性化自我介绍：</h3>
            <button
                class="!rounded-button whitespace-nowrap px-3 py-1 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 text-sm shadow-lg hover:shadow-xl backdrop-blur-sm flex items-center"
                @click="copySelfIntro"
            >
              <i class="fas fa-copy mr-1"></i>复制
            </button>
          </div>
          <p class="text-gray-700 whitespace-pre-line">{{ state.selfIntro }}</p>
        </div>
      </section>

      <!-- Step 3: 生成面试大纲（卡片式） -->
      <section v-if="state.currentStep === 2"
          class="backdrop-blur-md bg-white/70 rounded-2xl shadow-xl p-8 transition-all duration-300 border border-white/30"
      >
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <span class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white flex items-center justify-center mr-3 backdrop-blur-sm">3</span>
          生成面试大纲
        </h2>

        <div class="flex flex-wrap gap-3 mb-6">
          <button
              class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white hover:from-gray-600 hover:to-gray-700 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
              @click="goBackToIntro()"
          >
            <i class="fas fa-arrow-left mr-2"></i>返回上一步
          </button>
          <button
              class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
              @click="onGenerateOutline"
              :disabled="state.outlineStreaming || !state.jobGoal"
              :class="{ 'opacity-50 cursor-not-allowed': state.outlineStreaming || !state.jobGoal }"
          >
            <i v-if="state.outlineStreaming" class="fas fa-spinner fa-spin mr-2"></i>
            <i v-else-if="state.outline.length" class="fas fa-sync-alt mr-2"></i>
            <i v-else class="fas fa-magic mr-2"></i>
            <span v-if="state.outlineStreaming">生成中...</span>
            <span v-else-if="state.outline.length">重新生成大纲</span>
            <span v-else>生成大纲</span>
          </button>
          <button
              v-if="state.selectedOutline"
              class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white hover:from-green-600 hover:to-emerald-600 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
              @click="goToStep(3)"
          >
            进入下一步<i class="fas fa-arrow-right ml-2"></i>
          </button>
        </div>

        <div
          v-if="state.outlineStreaming && state.outlineStreamText"
          class="p-6 mb-3 bg-gradient-to-br from-blue-100 via-indigo-50 to-purple-50 rounded-xl border border-blue-200/60 animate-pulse shadow text-blue-800 overflow-auto max-h-80"
        >
          <div class="text-xs text-blue-700 mb-2">生成大纲中...</div>
          <div class="whitespace-pre-line font-mono text-[15px] leading-relaxed" v-html="renderMarkdown(state.outlineStreamText)"></div>
        </div>
        <div v-if="!state.outlineStreaming && state.outline.length === 0" class="text-gray-500">暂无大纲，请先点击生成。</div>

        <div v-else-if="!state.outlineStreaming && state.outline.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
              v-for="(item, index) in state.outline"
              :key="index"
              class="cursor-pointer relative overflow-hidden backdrop-blur-sm bg-white/80 border rounded-xl p-4 shadow-sm hover:shadow-md transition-all"
              :class="state.selectedOutline === item ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-200'"
              @click="onSelectOutline(item)"
          >
            <div class="flex items-start">
              <div class="mt-1 mr-3 h-6 w-6 rounded-md bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white text-xs">
                {{ index + 1 }}
              </div>
              <div class="flex-1">
                <div class="text-gray-800 text-sm leading-relaxed" v-html="renderMarkdown(item)"></div>
                <p class="text-xs text-gray-500 mt-2">点击选择该大纲项</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Step 4: 生成面试问题（三栏布局） -->
      <section v-if="state.currentStep === 3"
          class="backdrop-blur-md bg-white/70 rounded-2xl shadow-xl p-8 transition-all duration-300 border border-white/30"
      >
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <span class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white flex items-center justify-center mr-3 backdrop-blur-sm">4</span>
          生成面试问题
        </h2>

        <div class="flex flex-wrap gap-3 mb-6">
          <button
              class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white hover:from-gray-600 hover:to-gray-700 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
              @click="goBackToOutline()"
          >
            <i class="fas fa-arrow-left mr-2"></i>返回上一步
          </button>
          <button
              class="!rounded-button whitespace-nowrap px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 flex items-center shadow-lg hover:shadow-xl backdrop-blur-sm"
              @click="onGenerateQuestions(state.selectedOutline)"
              :disabled="state.questionsStreaming || !state.selectedOutline"
              :class="{ 'opacity-50 cursor-not-allowed': state.questionsStreaming || !state.selectedOutline }"
          >
            <i v-if="state.questionsStreaming" class="fas fa-spinner fa-spin mr-2"></i>
            <i v-else-if="state.questions.length" class="fas fa-sync-alt mr-2"></i>
            <i v-else class="fas fa-magic mr-2"></i>
            <span v-if="state.questionsStreaming">生成中...</span>
            <span v-else-if="state.questions.length">重新生成面试问题</span>
            <span v-else>生成面试问题</span>
          </button>
        </div>

        <!-- 当前选择的大纲提示（置于按钮下方，仅在已选择时展示） -->
        <div v-if="state.selectedOutline" class="mb-6 flex items-start justify-between gap-4">
          <div class="flex-1 rounded-xl border border-indigo-200/60 bg-gradient-to-r from-indigo-50 to-blue-50 p-4">
            <div class="text-xs text-indigo-700 mb-1">当前大纲</div>
            <div class="text-sm text-gray-800 whitespace-normal break-words leading-relaxed" v-html="renderMarkdown(state.selectedOutline)"></div>
          </div>
          <button
            class="rounded-full px-4 py-2 bg-gradient-to-r from-indigo-100 to-blue-100 text-indigo-700 font-semibold border border-indigo-200 shadow hover:from-blue-500 hover:to-indigo-500 hover:text-white hover:shadow-lg transition-all duration-200 text-sm"
            style="min-width:80px;letter-spacing:1px;"
            @click="goBackToOutline()"
          >重新选择</button>
        </div>

        <!-- 流动区：问题生成中 -->
        <div
          v-if="state.questionsStreaming && state.questionsStreamText"
          class="p-6 mb-3 bg-gradient-to-br from-blue-100 via-indigo-50 to-purple-50 rounded-xl border border-blue-200/60 animate-pulse shadow text-blue-800 overflow-auto max-h-80"
        >
          <div class="text-xs text-blue-700 mb-2">生成问题中...</div>
          <div class="whitespace-pre-line font-mono text-[15px] leading-relaxed">{{ state.questionsStreamText }}</div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <!-- 左：问题列表 -->
          <div class="lg:col-span-3">
            <div class="rounded-xl border border-gray-200 bg-white/70 shadow-sm">
              <div class="px-4 py-3 border-b border-gray-100 text-sm text-gray-600">问题列表(请点击选择)</div>
              <div class="divide-y divide-gray-100 overflow-auto" :style="{ maxHeight: questionListMaxHeight }">
                <button
                    v-for="q in state.questions"
                    :key="q.id"
                    class="w-full text-left px-4 py-3 hover:bg-gray-50 transition flex items-center gap-2"
                    :class="selectedQuestionId === q.id ? 'bg-indigo-50' : ''"
                    @click="selectQuestion(q.id)"
                >
                  <i class="fas fa-question text-indigo-500 flex-shrink-0"></i>
                  <span class="text-sm text-gray-800 truncate">{{ q.text }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 中：问题详情 + 作答 + 分析按钮 -->
          <div class="lg:col-span-6">
            <div class="rounded-xl border border-gray-200 bg-white/70 shadow-sm p-4">
              <div v-if="!selectedQuestion" class="text-gray-500 text-sm">请选择左侧问题</div>
              <div v-else>
                <div class="mb-3 bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-100 rounded-lg p-3">
                  <div class="text-xs text-indigo-700 mb-1 flex items-center">
                    <i class="fas fa-question-circle mr-2"></i> 当前问题
                  </div>
                  <div class="text-sm font-semibold text-gray-800 leading-relaxed">{{ selectedQuestion.text }}</div>
                </div>
                <textarea
                    v-model="answerDraft"
                    class="w-full h-48 border-2 border-gray-200/60 rounded-xl p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none transition-all duration-200 bg-white/80"
                    placeholder="请在此填写你的回答..."
                ></textarea>
                <div class="mt-2 flex items-center justify-between text-xs text-gray-500">
                  <span>已输入 {{ answerLength }} 字符</span>
                  <span v-if="selectedQuestion.analysis" class="text-green-600">已分析</span>
                </div>
                <div class="mt-3 flex justify-end">
                  <button
                      class="!rounded-button whitespace-nowrap px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-blue-600 text-white hover:from-indigo-700 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg flex items-center"
                      :disabled="!answerDraft || state.loadingAnalyzeIds.has(selectedQuestion.id)"
                      :class="{ 'opacity-50 cursor-not-allowed': !answerDraft || state.loadingAnalyzeIds.has(selectedQuestion.id) }"
                      @click="onAnalyze({ id: selectedQuestion.id, answer: answerDraft })"
                  >
                    <i v-if="state.loadingAnalyzeIds.has(selectedQuestion.id)" class="fas fa-spinner fa-spin mr-2"></i>
                    <i v-else class="fas fa-wand-magic-sparkles mr-2"></i>
                    <span v-if="state.loadingAnalyzeIds.has(selectedQuestion.id)">分析中...</span>
                    <span v-else>AI 分析</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 右：分析结果 -->
          <div class="lg:col-span-3">
            <div class="rounded-xl border border-gray-200 bg-white/70 shadow-sm">
              <div class="px-4 py-3 border-b border-gray-100 text-sm text-gray-600">分析结果</div>
              <div class="p-4">
                <div v-if="!selectedQuestion" class="text-gray-500 text-sm text-center py-8">
                  <i class="fas fa-info-circle text-2xl mb-2 block"></i>
                  分析结果将显示在这里
                </div>
                <div v-else class="space-y-4">
                  <!-- AI分析流动区 -->
                  <div v-if="state.answerAnalyzeStream[selectedQuestion.id]" class="p-4 mb-2 bg-blue-50 border border-blue-200/50 animate-pulse rounded-lg shadow text-blue-800 overflow-auto max-h-72">
                    <div class="text-xs text-blue-700 mb-1">AI分析中...</div>
                    <div class="font-mono text-[15px] leading-relaxed text-blue-800">{{ state.answerAnalyzeStream[selectedQuestion.id]! }}</div>
                  </div>
                  <!-- AI 分析卡片 -->
                  <div v-if="!state.answerAnalyzeStream[selectedQuestion.id]" class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200/50">
                    <div class="flex items-center mb-2">
                      <i class="fas fa-brain text-blue-600 mr-2"></i>
                      <h4 class="text-sm font-semibold text-blue-800">AI 分析</h4>
                    </div>
                    <div class="text-sm text-gray-700 leading-relaxed">
                      <p v-if="selectedQuestion.analysis" class="whitespace-pre-line">{{ selectedQuestion.analysis }}</p>
                      <p v-else class="text-gray-500 italic">暂无分析结果，请先点击 AI 分析</p>
                    </div>
                  </div>
                  <!-- 参考答案卡片 unchanged -->
                  <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-4 border border-green-200/50">
                    <div class="flex items-center mb-2">
                      <i class="fas fa-lightbulb text-green-600 mr-2"></i>
                      <h4 class="text-sm font-semibold text-green-800">参考答案</h4>
                    </div>
                    <div class="text-sm text-gray-700 leading-relaxed">
                      <div
                        v-if="selectedQuestion.standardAnswer"
                        class="cursor-pointer select-none"
                        @click="openFullAnswerDialog(selectedQuestion)"
                        title="点击查看完整内容"
                      >
                        {{ truncateText(selectedQuestion.standardAnswer || '', 90) }}
                        <span v-if="(selectedQuestion.standardAnswer || '').length > 90">…</span>
                        <div class="text-[11px] text-gray-500 mt-1">点击查看完整内容</div>
                      </div>
                      <p v-else class="text-gray-500 italic">暂无参考答案，请先点击 AI 分析</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <el-dialog v-model="showAnswerDialog" width="680px" :show-close="false" class="answer-dialog">
      <template #header>
        <div class="flex items-center justify-center gap-2 w-full text-center">
          <i class="fas fa-book-open text-indigo-600"></i>
          <h3 class="text-base font-semibold text-indigo-700">参考答案</h3>
        </div>
      </template>
      <div class="mt-2 space-y-5">
        <div class="rounded-lg border border-indigo-100 bg-gradient-to-r from-indigo-50 to-blue-50 p-3">
          <div class="text-xs text-indigo-700 mb-1">当前问题</div>
          <div class="text-sm font-semibold text-gray-800 leading-relaxed">{{ fullAnswerDialogQuestion }}</div>
        </div>
        <div class="rounded-lg border border-green-100 bg-gradient-to-r from-green-50 to-emerald-50 p-3">
          <div class="flex items-center justify-between mb-2">
            <div class="text-xs text-green-700">参考答案</div>
            <button
              class="rounded-full px-3 py-1 text-xs bg-white text-green-700 border border-green-200 hover:bg-green-50 transition"
              @click="copyDialogAnswer"
            >复制</button>
          </div>
          <div class="text-sm text-gray-700 leading-relaxed prose prose-sm prose-indigo max-w-full" v-html="renderMarkdown(fullAnswerDialogContent)"></div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <button
            class="!rounded-button px-4 py-2 bg-gradient-to-r from-gray-600 to-gray-700 text-white hover:from-gray-700 hover:to-gray-800 transition-all"
            @click="showAnswerDialog = false"
          >关闭</button>
        </span>
      </template>
    </el-dialog>

  </div>
  
  <!-- Footer -->
  <footer class="fixed bottom-0 left-0 right-0 backdrop-blur-md bg-white/60 border-t border-white/30 py-2 z-40">
    <div class="container mx-auto px-6">
      <div class="text-center text-gray-500 text-xs">
        <p>© 2025 AI 面试助手. 保留所有权利.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import {computed, reactive, ref, computed as vueComputed} from 'vue';
import {ElMessage} from 'element-plus';
import {
  analyzeAnswer,
  generateInterviewOutline,
  generateQuestions,
  generateSelfIntroduction,
  processResume,
  generateSelfIntroductionStream,
  generateInterviewOutlineStream,
  generateQuestionsStream,
  analyzeAnswerStream
} from '../api/client';
import UploadAndGoal from '../components/UploadAndGoal.vue';
import { marked } from 'marked';

const steps = [
  {title: '个人信息补充', icon: 'fas fa-id-card'},
  {title: '生成自我介绍', icon: 'fas fa-user-pen'},
  {title: '生成面试大纲', icon: 'fas fa-list'},
  {title: '生成面试问题', icon: 'fas fa-comments'}
];

const progressStyle = computed(() => {
  const total = steps.length - 1;
  const clamped = Math.max(0, Math.min(state.currentStep, total));
  if (clamped === 0 || total === 0) return { width: '0px' };
  const percent = (clamped / total) * 100;
  const halfCircle = 24; // w-12 => 48px, half = 24px
  const endOffsetPx = 32; // slightly larger to avoid visual overshoot with rounded ends
  if (clamped === total) {
    return { width: `calc(100% - ${endOffsetPx}px)` };
  }
  return { width: `calc(${percent}% - ${halfCircle}px)` };
});

type Question = {
  id: string;
  text: string;
  answer?: string;
  analysis?: string;
  standardAnswer?: string;
};

const state = reactive({
  resumePdf: undefined as File | undefined,
  resumeFileList: [] as any[],
  jobGoal: '',
  selfIntro: '',      // 最终卡片展示文本
  selfIntroStreaming: false, // 是否在流式中
  selfIntroStreamText: '',   // 增量片段字符串（流动区）
  outline: [] as string[],
  selectedOutline: '',
  questions: [] as Question[],
  pdfText: '',
  loadingIntro: false,
  loadingOutline: false,
  outlineStreaming: false,
  outlineStreamText: '',
  outlineStreamError: '',
  loadingQuestions: false,
  questionsStreaming: false,
  questionsStreamText: '',
  loadingAnalyzeIds: new Set<string>(),
  answerAnalyzeStream: {} as Record<string, string>,
  currentStep: 0,
});

function goToStep(stepIndex: number) {
  state.currentStep = stepIndex;
}

async function ensurePdfText() {
  if (!state.pdfText) {
    if (!state.resumePdf) throw new Error('请先上传 PDF 简历');
    const {pdf_text} = await processResume(state.resumePdf);
    state.pdfText = pdf_text || '';
  }
}

async function onGenerateSelfIntro() {
  try {
    state.selfIntroStreaming = true;
    state.selfIntroStreamText = '';
    state.selfIntro = '';
    await ensurePdfText();
    await new Promise<void>((resolve, reject) => {
      generateSelfIntroductionStream({
        job_description: state.jobGoal,
        pdf_text: state.pdfText,
      }, {
        onDelta(text: string) {
          state.selfIntroStreamText = text;
        },
        onFinal(data: any) {
          state.selfIntroStreaming = false;
          state.selfIntroStreamText = '';
          state.selfIntro = (data && data.self_introduction) || '';
          ElMessage.success('自我介绍生成成功');
          resolve();
        },
        onError(msg) {
          state.selfIntroStreaming = false;
          ElMessage.error(msg || '流式接口发生错误');
          reject(msg || '流式出错');
        },
        onEnd() {
          state.selfIntroStreaming = false;
        },
      });
    });
  } catch (e: any) {
    ElMessage.error(e?.message || '生成失败');
  } finally {
    state.selfIntroStreaming = false;
  }
}

async function onGenerateOutline() {
  try {
    state.outlineStreaming = true;
    state.outlineStreamText = '';
    state.outline = [];
    state.selectedOutline = '';
    state.questions = [];
    selectedQuestionId.value = null;
    answerDraft.value = '';
    await ensurePdfText();
    await new Promise<void>((resolve, reject) => {
      generateInterviewOutlineStream({
        job_description: state.jobGoal,
        pdf_text: state.pdfText,
      }, {
        onDelta(txt) {
          state.outlineStreamText = txt;
        },
        onFinal(data) {
          state.outlineStreaming = false;
          state.outlineStreamText = '';
          state.outline = (data && data.outline) || [];
          ElMessage.success('面试大纲生成成功');
          resolve();
        },
        onError(msg) {
          state.outlineStreaming = false;
          ElMessage.error(msg || '大纲流式接口错误');
          reject(msg || '流式出错');
        },
        onEnd() { state.outlineStreaming = false; },
      });
    });
  } catch (e) {
    state.outlineStreaming = false;
    ElMessage.error('生成大纲失败');
  }
}

function onSelectOutline(item: string) {
  state.selectedOutline = item;
  state.questions = [];
  ElMessage.success('已选择大纲条目');
}

async function onGenerateQuestions(topic: string) {
  try {
    state.questionsStreaming = true;
    state.questionsStreamText = '';
    state.questions = [];
    selectedQuestionId.value = null;
    answerDraft.value = '';
    await new Promise<void>((resolve, reject) => {
      generateQuestionsStream({ interview_outline_item: topic }, {
        onDelta(txt) {
          state.questionsStreamText = txt;
        },
        onFinal(data) {
          state.questionsStreaming = false;
          state.questionsStreamText = '';
          const now = Date.now();
          const arr = data && data.questions ? data.questions : [];
          state.questions = arr.map((text: string, i: number) => ({id: `${now}-${i+1}`, text}));
          ElMessage.success('问题列表生成成功');
          resolve();
        },
        onError(msg) {
          state.questionsStreaming = false;
          ElMessage.error(msg || '问题流式接口错误');
          reject(msg || '流式出错');
        },
        onEnd() { state.questionsStreaming = false; }
      });
    });
  } catch (e) {
    state.questionsStreaming = false;
    ElMessage.error('生成问题失败');
  }
}

async function onAnalyze(q: { id: string; answer: string }) {
  const idx = state.questions.findIndex(x => x.id === q.id);
  if (idx === -1) return;
  try {
    state.loadingAnalyzeIds.add(q.id);
    state.answerAnalyzeStream[q.id] = '';
    await new Promise<void>((resolve, reject) => {
      analyzeAnswerStream({
        question: state.questions[idx].text,
        user_answer: q.answer || '',
      }, {
        onDelta(txt) {
          state.answerAnalyzeStream[q.id] = txt;
        },
        onFinal(data) {
          state.questions[idx].answer = q.answer;
          state.questions[idx].analysis = data.answer_evaluation || '';
          state.questions[idx].standardAnswer = data.standard_answer || '';
          delete state.answerAnalyzeStream[q.id];
          ElMessage.success('分析完成');
          resolve();
        },
        onError(msg) {
          delete state.answerAnalyzeStream[q.id];
          ElMessage.error(msg || '分析流式接口错误');
          reject(msg || '流式出错');
        },
        onEnd() {
          state.loadingAnalyzeIds.delete(q.id);
        },
      });
    });
  } catch (e) {
    delete state.answerAnalyzeStream[q.id];
    state.loadingAnalyzeIds.delete(q.id);
    ElMessage.error('分析失败');
  }
}

async function copySelfIntro() {
  if (!state.selfIntro) return;
  try {
    await navigator.clipboard.writeText(state.selfIntro);
    ElMessage.success('自我介绍已复制到剪贴板');
  } catch (err) {
    const textArea = document.createElement('textarea');
    textArea.value = state.selfIntro;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    ElMessage.success('自我介绍已复制到剪贴板');
  }
}

// 第四步：本地选择与作答草稿
const selectedQuestionId = ref<string | null>(null);
const selectedQuestion = computed(() => state.questions.find(q => q.id === selectedQuestionId.value) || null);
const answerDraft = ref('');
const answerLength = computed(() => answerDraft.value.length);
const QUESTION_ROW_HEIGHT = 48;
const questionListMaxHeight = computed(() => `${Math.min(state.questions.length, 10) * QUESTION_ROW_HEIGHT}px`);
function selectQuestion(id: string) {
  selectedQuestionId.value = id;
  const q = state.questions.find(x => x.id === id);
  answerDraft.value = q?.answer || '';
}

function renderMarkdown(md: string) {
  return marked.parse(md || '');
}

// 参考答案弹窗
const showAnswerDialog = ref(false);
const fullAnswerDialogContent = ref('');
const fullAnswerDialogQuestion = ref('');
function openFullAnswerDialog(q: { text?: string; standardAnswer?: string } | null) {
  fullAnswerDialogQuestion.value = (q?.text || '').toString();
  fullAnswerDialogContent.value = (q?.standardAnswer || '').toString();
  showAnswerDialog.value = true;
}

async function copyDialogAnswer() {
  try {
    await navigator.clipboard.writeText(fullAnswerDialogContent.value || '');
    ElMessage.success('参考答案已复制到剪贴板');
  } catch (e) {
    ElMessage.warning('复制失败，请手动复制');
  }
}

function truncateText(text: string, maxLen = 90) {
  if (!text) return '';
  return text.length <= maxLen ? text : text.slice(0, maxLen);
}

function goBackToOutline() {
  state.currentStep = 2;
  state.questions = [];
  selectedQuestionId.value = null;
  answerDraft.value = '';
}

function goBackToInfo() {
  state.currentStep = 0;
}

function goBackToIntro() {
  state.currentStep = 1;
}
</script>

<style scoped>
.rounded-button {
  border-radius: 0.5rem;
}
:deep(.answer-dialog .el-dialog) {
  border-radius: 14px;
  overflow: hidden;
}
:deep(.answer-dialog .el-dialog__header) {
  background: transparent;
  border-bottom: none;
  display: flex;
  justify-content: center;
}
:deep(.answer-dialog .el-dialog__body) {
  background: #fff;
}
</style>


