"""
会话管理 API
"""
from fastapi import APIRouter, HTTPException
from typing import Dict
import uuid
from datetime import datetime
from backend.models import SessionCreate, SessionResponse
from backend.services import game_service

router = APIRouter()

# 全局会话存储（生产环境应该用数据库）
sessions: Dict[str, dict] = {}


@router.post("/", response_model=SessionResponse)
async def create_session(request: SessionCreate):
    """创建新会话"""
    session_id = str(uuid.uuid4())

    # 调用游戏服务初始化,获取开场白
    config_dict = request.config.dict() if request.config else None
    opening_messages = game_service.init_session(session_id, request.scenario_id, config_dict)

    # 初始化游戏会话
    session_data = {
        "session_id": session_id,
        "scenario_id": request.scenario_id,
        "status": "active",
        "created_at": datetime.now(),
        "pancake_score": 0,
        "garlic_score": 0,
        "config": request.config.dict() if request.config else None,
        "conversation_history": opening_messages,  # 包含开场白
        "round": 0
    }

    sessions[session_id] = session_data

    return SessionResponse(**session_data)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """获取会话信息"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="会话不存在")

    return SessionResponse(**sessions[session_id])


@router.post("/{session_id}/end")
async def end_session(session_id: str):
    """结束会话"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="会话不存在")

    sessions[session_id]["status"] = "ended"

    return {"message": "会话已结束", "session_id": session_id}


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="会话不存在")

    del sessions[session_id]

    return {"message": "会话已删除"}
