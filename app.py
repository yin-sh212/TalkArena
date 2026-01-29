"""
TalkArena - ModelScope 部署入口文件
社交技能训练模拟器
"""
import os
import sys
import uvicorn

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入 FastAPI 应用
from backend.main import app

if __name__ == "__main__":
    # 获取端口配置（ModelScope 默认使用 7860）
    port = int(os.environ.get("PORT", 7860))

    print(f"""
    ╔══════════════════════════════════════════════╗
    ║        TalkArena 社交技能训练模拟器          ║
    ║              正在启动服务...                 ║
    ╚══════════════════════════════════════════════╝

    🚀 服务端口: {port}
    📚 API 文档: http://0.0.0.0:{port}/docs
    🏥 健康检查: http://0.0.0.0:{port}/health
    🎯 应用首页: http://0.0.0.0:{port}/
    """)

    # 启动 uvicorn 服务器
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
