# TalkArena ModelScope 部署指南

## 快速部署步骤

### 1. 准备工作

在部署前，确保已构建前端：

```bash
cd frontend
npm install
npm run build
cd ..
```

构建后会生成 `frontend/dist/` 目录，包含所有前端静态文件。

### 2. 提交代码到 Git

```bash
# 添加所有文件（包括 frontend/dist）
git add .

# 提交
git commit -m "Ready for ModelScope deployment"

# 推送到远程仓库
git push origin master
```

### 3. 在 ModelScope 创建空间

1. 访问 [ModelScope](https://modelscope.cn)
2. 点击 "创建空间"
3. 填写信息：
   - **英文名称**：例如 `talkarena`
   - **中文名称**：社交技能训练模拟器
   - **所有者**：你的账号
   - **License**：Apache License 2.0
   - **是否公开**：根据需求选择

4. **接入SDK**：选择 **Gradio** + Gradio 6.2.0
5. **镜像版本**：ubuntu22.04-py311-torch2.3.1-modelscope1.31.0
6. **天联云资源**：按需选择（推荐至少 2v CPU / 16G内存）

### 4. 上传代码

方式一：通过 Git 推送
```bash
git remote add modelscope <你的ModelScope仓库地址>
git push modelscope master
```

方式二：通过网页直接上传文件

### 5. 等待启动

ModelScope 会自动：
- 安装 `requirements.txt` 中的依赖
- 运行 `app.py` 启动服务
- 在端口 7860 提供服务

## 项目结构说明

```
TalkArena/
├── app.py                 # ModelScope 入口文件（自动运行）
├── requirements.txt       # Python 依赖
├── backend/              # FastAPI 后端
│   ├── main.py          # FastAPI 应用
│   └── api/             # API 路由
├── frontend/dist/        # 前端静态文件（必须提交）
├── config/              # 配置文件
└── models/              # AI 模型
```

## 访问应用

部署成功后：
- **应用首页**：`https://你的空间名.modelscope.cn/`
- **API 文档**：`https://你的空间名.modelscope.cn/docs`
- **健康检查**：`https://你的空间名.modelscope.cn/health`

## 注意事项

### 1. 前端静态文件

⚠️ **重要**：`frontend/dist/` 目录必须提交到 Git！

已修改 `.gitignore` 以允许提交此目录。

### 2. 依赖安装

首次启动可能需要 5-10 分钟安装依赖，包括：
- PyTorch（约 2GB）
- ModelScope SDK
- Transformers
- FastAPI 等

### 3. 模型文件

如果项目使用大型 AI 模型：
- 考虑从 ModelScope Hub 动态下载
- 或使用 Git LFS 管理大文件
- 避免直接提交大模型文件

### 4. CORS 配置

生产环境建议修改 `backend/main.py` 中的 CORS 设置：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://你的空间名.modelscope.cn"],  # 指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 本地测试

部署前建议本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

访问 `http://localhost:7860` 验证功能。

## 常见问题

### 前端页面空白

检查：
- `frontend/dist/` 是否已构建并提交
- 浏览器控制台是否有错误
- API 路径是否正确

### 依赖安装失败

- 检查 `requirements.txt` 版本兼容性
- 查看 ModelScope 构建日志
- 尝试降低依赖版本号

### 启动超时

- 首次启动需要时间安装依赖，耐心等待
- 检查代码是否有语法错误
- 查看 ModelScope 日志

## 技术架构

- **前端**：Vue 3 + Vite（打包为静态文件）
- **后端**：FastAPI + uvicorn
- **AI**：ModelScope + PyTorch + Transformers
- **部署**：ModelScope Gradio SDK

## 更新部署

修改代码后：

```bash
# 如果修改了前端，重新构建
cd frontend && npm run build && cd ..

# 提交更新
git add .
git commit -m "Update: 描述"
git push modelscope master
```

ModelScope 会自动重新部署。

---

**祝部署成功！🚀**
