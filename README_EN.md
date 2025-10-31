<div align="center">

# 🤖 Interview Assistant

**Input Resume + Job Description, One-Click to Generate Your Personalized Interview Preparation Guide!**

Self-introduction | Interview Outline | Question Generation | Answer Analysis | Standard Reference

![Python](https://img.shields.io/badge/Python-3.12.5-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-Agent-green)
![Node](https://img.shields.io/badge/Node.js-22.16.0-brightgreen?logo=node.js)
![pnpm](https://img.shields.io/badge/pnpm-9+-orange?logo=pnpm)

</div>

---

## 📘 Project Introduction

**Interview Assistant** is an intelligent interview preparation tool based on **Flask + LangChain + Frontend-Backend Separation Architecture**.

All you need to provide:

- 📄 A PDF resume
- 💼 A job description

The system will automatically generate personalized interview preparation materials for you, including:

| Functional Module | Description |
|-----------|------|
| 🎤 Self-introduction | Automatically generate personalized introduction based on resume and position |
| 🧭 Interview Outline | Organize core exam points and interview directions for the position |
| ❓ Interview Questions | Automatically generate high-quality question list |
| 🧠 Answer Analysis | Evaluate your answers and provide standard references |

---

## ⚙️ Environment Requirements

| Tool | Recommended Version | Description |
|------|-----------|------|
| 🐍 Python | 3.12.5 | Backend runtime environment |
| 🧩 Node.js | 22.16.0 | Frontend runtime environment |
| 🧠 LLM Provider | OpenAI Compatible Format | Used for model invocation |

---

## 🚀 Startup Instructions

### 🖥️ Backend Startup (Flask API)

```bash
# 1️⃣ Copy configuration file
cp .env.example .env

# 2️⃣ Install dependencies
pip install -r interview-myself/requirements.txt

# 3️⃣ Start the application
cd interview-myself
python app.py
```

Default access after startup:

> 🌐 [http://localhost:8910](http://localhost:8910)

---

### 💡 Frontend Startup

```bash
# 1️⃣ Install dependencies
cd interview-myself-web
pnpm install

# 2️⃣ Start local development environment
pnpm dev
```

Default access address:

> 🌐 [http://localhost:5173](http://localhost:5173)

---

## Docker Deployment

```shell 
# Copy docker-compose template and modify environment variable values
cp docker-compose.yml.template docker-compose.yml

docker-compose up -d
```
> 🚀 After successful startup, access [http://localhost:18080](http://localhost:18080)
---

## 🖼️ Page Preview

| Example | Description |
| ------- | ----------- |
| ![1](https://raw.githubusercontent.com/kuschzzp/images_repository/main/images/20251030_1.png) | Usage Example 1 |
| ![2](https://raw.githubusercontent.com/kuschzzp/images_repository/main/images/20251030_2.png) | Usage Example 2 |


## 📜 Open Source License

This project is released under the **GNU General Public License v3 (GPLv3)**. This means:

- ✅ You are free to use, copy, study and modify this project;
- ⚙️ If you modify or re-publish this project, you must continue to open source under the same **GPLv3 license**;
- 🚫 It is prohibited to embed the code of this project into commercial products in a closed-source manner;
- 🧾 You should include the original license file `LICENSE` when distributing.

---

## 💬 Author's Words

> "Every interview is a deeper self-exploration.
> Let AI become your preparation coach, not a replacement."

If you find this project helpful, please give it a ⭐ **Star** to support!

---

<div align="center">

Made with ❤️ by [Kusch](https://github.com/kuschzzp)

</div>