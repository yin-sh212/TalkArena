"""
数据模型定义
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========== 场景相关 ==========
class Scenario(BaseModel):
    """场景信息"""
    id: str
    name: str
    description: str
    type: str  # "shandong_dinner", "negotiation", etc.


class ScenarioConfig(BaseModel):
    """山东饭局场景配置"""
    scene: str  # "商务宴请", "家庭聚会" etc.
    members: List[Dict[str, str]]  # 饭局成员信息


# ========== 会话相关 ==========
class SessionCreate(BaseModel):
    """创建会话请求"""
    scenario_id: str
    config: Optional[ScenarioConfig] = None


class SessionResponse(BaseModel):
    """会话响应"""
    session_id: str
    scenario_id: str
    status: str  # "active", "ended"
    created_at: datetime
    pancake_score: int = 0
    garlic_score: int = 0
    conversation_history: List[Dict[str, Any]] = []  # 对话历史（包含开场白）
    round: int = 0


# ========== 对话相关 ==========
class ChatMessage(BaseModel):
    """用户消息"""
    session_id: str
    message: str
    message_type: str = "text"  # "text" or "voice"


class ChatResponse(BaseModel):
    """AI 响应"""
    session_id: str
    npc_name: str
    message: str
    audio_url: Optional[str] = None  # TTS 音频地址
    judgment: Optional[Dict[str, Any]] = None  # 判分结果
    game_state: Dict[str, Any]  # 游戏状态（分数、轮次等）


class RescueRequest(BaseModel):
    """求救请求"""
    session_id: str


class RescueResponse(BaseModel):
    """救场答案"""
    suggestion: str
    explanation: str


# ========== 报告相关 ==========
class GameReport(BaseModel):
    """游戏复盘报告"""
    session_id: str
    total_rounds: int
    pancake_score: int
    garlic_score: int
    title: str
    evaluation: str
    highlights: List[Dict[str, str]]
    radar_data: Dict[str, int]
    conversation_history: List[Dict[str, Any]]
