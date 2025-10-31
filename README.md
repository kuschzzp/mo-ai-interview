<div align="center">

# 🤖 面试助手 · Interview Assistant

**输入简历 + 岗位需求，一键生成你的专属面试准备指南！**

自我介绍 ｜ 面试大纲 ｜ 题目生成 ｜ 回答分析 ｜ 标准参考

![Python](https://img.shields.io/badge/Python-3.12.5-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-Agent-green)
![Node](https://img.shields.io/badge/Node.js-22.16.0-brightgreen?logo=node.js)
![pnpm](https://img.shields.io/badge/pnpm-9+-orange?logo=pnpm)

</div>

---

## 📘 项目简介

**面试助手 (Interview Assistant)** 是一个基于 **Flask + LangChain + 前后端分离架构** 的智能面试准备工具。

你只需提供：

- 📄 一份 PDF 简历  
- 💼 一份岗位需求  

系统将自动为你生成个性化的面试准备资料，包括：

| 功能模块 | 说明 |
|-----------|------|
| 🎤 自我介绍 | 根据简历与岗位自动生成个性化介绍 |
| 🧭 面试大纲 | 梳理岗位核心考点与面试方向 |
| ❓ 面试问题 | 自动生成高质量问题清单 |
| 🧠 答案分析 | 评价你的回答并提供标准参考 |

---

## ⚙️ 环境要求

| 工具 | 推荐版本 | 说明 |
|------|-----------|------|
| 🐍 Python | 3.12.5 | 后端运行环境 |
| 🧩 Node.js | 22.16.0 | 前端运行环境 |
| 🧠 LLM Provider | OpenAI 格式兼容 | 用于模型调用 |

---

## 🚀 启动方式

### 🖥️ 后端启动（Flask API）

```bash
# 1️⃣ 拷贝配置文件
cp .env.example .env

# 2️⃣ 安装依赖
pip install -r interview-myself/requirements.txt

# 3️⃣ 启动应用
cd interview-myself
python app.py
````

默认启动后访问：

> 🌐 [http://localhost:8910](http://localhost:8910)

---

### 💡 前端启动

```bash
# 1️⃣ 安装依赖
cd interview-myself-web
pnpm install

# 2️⃣ 启动本地开发环境
pnpm dev
```

默认访问地址：

> 🌐 [http://localhost:5173](http://localhost:5173)

---

## docker 部署

```shell 
# 复制 docker-compose 模板,修改其中环境变量的值
cp docker-compose.yml.template docker-compose.yml

docker-compose up -d
```
> 🚀 启动成功后访问 [http://localhost:18080](http://localhost:18080)
---

## 🖼️ 页面预览

| 示例                                                                                            | 说明     |
| --------------------------------------------------------------------------------------------- | ------ |
| ![1](https://raw.githubusercontent.com/kuschzzp/images_repository/main/images/20251030_1.png) | 使用示例 1 |
| ![2](https://raw.githubusercontent.com/kuschzzp/images_repository/main/images/20251030_2.png) | 使用示例 2 |


## 📜 开源协议说明

本项目基于 **GNU General Public License v3 (GPLv3)** 开源发布。  
这意味着：

- ✅ 你可以自由使用、复制、学习和修改本项目；
- ⚙️ 如果你修改或二次发布本项目，必须在相同的 **GPLv3 协议** 下继续开源；
- 🚫 禁止将本项目的代码闭源地嵌入到商业产品中；
- 🧾 你应在分发时附带原始协议文件 `LICENSE`。

---

## 💬 作者的话

> “每一场面试，都是一次更深的自我探索。
> 让 AI 成为你的准备教练，而不是替代者。”

如果你觉得这个项目有帮助，请点个 ⭐ **Star** 支持一下！

---

<div align="center">

Made with ❤️ by [Kusch](https://github.com/kuschzzp)

</div>