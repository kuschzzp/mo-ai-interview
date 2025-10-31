# ===== 阶段1：构建前端 =====
FROM node:22-bullseye AS frontend-build
WORKDIR /frontend

# 设置 npm 使用阿里云镜像，并启用 pnpm
RUN npm config set registry https://registry.npmmirror.com \
    && corepack enable

# 先复制依赖文件以利用缓存
COPY interview-myself-web/package.json interview-myself-web/pnpm-lock.yaml ./

# 安装依赖
RUN pnpm install

# 复制其余前端代码并构建
COPY interview-myself-web/ .
RUN pnpm build

# ===== 阶段2：最终运行镜像（包含后端 + 前端 + 服务) =====
FROM python:3.12-slim-bookworm AS backend-build
WORKDIR /app

# 设置 pip 使用清华镜像
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 设置镜像，安装依赖
RUN rm -f /etc/apt/sources.list.d/debian.sources \
    && echo "deb https://mirrors.ustc.edu.cn/debian/ bookworm main contrib non-free" > /etc/apt/sources.list \
    && echo "deb https://mirrors.ustc.edu.cn/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.ustc.edu.cn/debian-security/ bookworm-security main contrib non-free" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends nginx supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY interview-myself/requirements.txt .

RUN pip install gunicorn==23.0.0
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY interview-myself/ .

# 复制前端构建产物
COPY --from=frontend-build /frontend/dist ./frontend_dist

# 复制配置
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]