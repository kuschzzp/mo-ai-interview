<template>
  <div class="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-50 via-white to-indigo-50">
    <!-- 背景装饰 -->
    <span class="pointer-events-none absolute -top-24 -left-24 h-72 w-72 rounded-full bg-blue-200/30 blur-3xl"></span>
    <span class="pointer-events-none absolute -bottom-24 -right-24 h-72 w-72 rounded-full bg-purple-200/30 blur-3xl"></span>

    <!-- 顶部导航/标题 -->
    <header class="backdrop-blur-md bg-white/90 shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="container mx-auto px-6 py-2 flex items-center justify-between min-h-[48px]">
        <div class="flex items-center gap-2">
          <i class="fas fa-toolbox text-indigo-600 text-lg"></i>
          <h1 class="text-lg font-semibold text-gray-800 tracking-tight">我的工具仓库</h1>
        </div>
        <nav class="text-gray-400 text-xs">共 {{ tools.length }} 个工具</nav>
      </div>
    </header>

    

    <!-- 卡片列表 -->
    <main id="tool-list" class="container mx-auto px-6 py-10">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <router-link
          v-for="tool in tools"
          :key="tool.path"
          :to="tool.path"
          class="group block relative overflow-hidden backdrop-blur-sm bg-white/80 border border-gray-200/70 rounded-2xl p-5 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
        >
          <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-gradient-to-br from-indigo-500/5 to-blue-500/5"></div>
          <div class="relative flex items-start justify-between mb-3">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center ring-4 ring-white/70 shadow-sm"
                 :class="tool.iconBg">
              <i :class="tool.icon" class="text-white text-xl"></i>
            </div>
            <span class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">{{ tool.badge }}</span>
          </div>
          <h3 class="relative text-lg font-semibold text-gray-800 mb-1">{{ tool.title }}</h3>
          <p class="relative text-gray-600 text-sm leading-relaxed line-clamp-2">{{ tool.desc }}</p>
          <div class="relative mt-3 flex flex-wrap gap-2">
            <span
              v-for="tag in tool.tags"
              :key="tag"
              class="text-[11px] px-2 py-0.5 rounded-full bg-gray-100 text-gray-600"
            >{{ tag }}</span>
          </div>
          <div class="relative mt-4 flex items-center text-indigo-600 group-hover:text-indigo-700">
            <span class="text-sm font-medium">进入</span>
            <i class="fas fa-arrow-right ml-2"></i>
          </div>
        </router-link>
      </div>
    </main>

  </div>
  
  <!-- 页脚 -->
  <footer class="fixed bottom-0 left-0 right-0 backdrop-blur-md bg-white/60 border-t border-white/30 py-3 z-40">
    <div class="container mx-auto px-6 text-center text-xs text-gray-400">
      <span>© 2025 我的工具仓库</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref } from 'vue';

type ToolCard = {
  title: string;
  desc: string;
  path: string;
  icon: string;
  iconBg: string;
  badge: string;
  tags: string[];
}

const tools = ref<ToolCard[]>([
  {
    title: 'AI 面试助手',
    desc: '上传简历与岗位，自动生成自我介绍、面试大纲与问题分析。',
    path: '/interview',
    icon: 'fas fa-robot',
    iconBg: 'bg-gradient-to-br from-blue-500 to-indigo-500',
    badge: 'AI',
    tags: ['AI', '求职']
  },
]);
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>


