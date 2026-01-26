"""
TalkArena - FastAPI 后端主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys
import os

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from backend.api import scenarios, sessions, chat

app = FastAPI(
    title="TalkArena API",
    description="社交技能训练模拟器 API",
    version="2.0.0"
)

# CORS 配置 - 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite 和其他前端开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(scenarios.router, prefix="/api/scenarios", tags=["场景管理"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["会话管理"])
app.include_router(chat.router, prefix="/api/chat", tags=["对话"])

@app.get("/")
async def root():
    return {
        "message": "TalkArena API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 开发模式自动重载
    )
