"""
游戏服务 - 连接原有的 Orchestrator 和游戏逻辑
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from orchestrator import Orchestrator
from typing import Dict, Any, Optional


class GameService:
    """游戏服务 - 管理会话和调用核心逻辑"""

    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.orchestrator = None

    def _get_orchestrator(self):
        """懒加载 Orchestrator（避免启动时就加载模型）"""
        if self.orchestrator is None:
            self.orchestrator = Orchestrator(enable_tts=True)
        return self.orchestrator

    def init_session(self, session_id: str, scenario_id: str, config: Optional[dict] = None):
        """初始化会话"""
        self.sessions[session_id] = {
            "scenario_id": scenario_id,
            "config": config,
            "conversation_history": [],
            "pancake_score": 0,
            "garlic_score": 0,
            "round": 0
        }

    async def process_message(self, session_id: str, user_message: str, message_type: str = "text") -> Dict[str, Any]:
        """
        处理用户消息

        Args:
            session_id: 会话 ID
            user_message: 用户输入
            message_type: 消息类型 ("text" 或 "voice")

        Returns:
            包含 AI 响应和游戏状态的字典
        """
        if session_id not in self.sessions:
            raise ValueError("会话不存在")

        session = self.sessions[session_id]

        # 调用 Orchestrator 处理消息
        orchestrator = self._get_orchestrator()

        # 将内部session_id映射到orchestrator的session
        orch_session_id = session.get("orch_session_id")
        if not orch_session_id:
            # 首次使用，需要在orchestrator中创建session
            orch_session = orchestrator.start_session(session["scenario_id"])
            orch_session_id = orch_session.session_id
            session["orch_session_id"] = orch_session_id

        # 使用流式处理
        ai_text = None
        audio_path = None
        judgment = "处理中"
        dominance_shift = 0

        for event in orchestrator.process_turn_streaming(orch_session_id, user_message):
            if event["stage"] == "complete":
                ai_text = event.get("ai_text", "")
                audio_path = event.get("audio_path")
                judgment = event.get("judgment", "")
                dominance_shift = event.get("dominance_shift", 0)

                # 更新气场分数
                orch_session = orchestrator.sessions[orch_session_id]
                session["pancake_score"] = orch_session.user_dominance
                session["garlic_score"] = orch_session.ai_dominance
                session["round"] = orch_session.turn_count

        # 构建响应
        response = {
            "session_id": session_id,
            "npc_name": orchestrator.sessions[orch_session_id].ai_name,
            "message": ai_text or "AI暂无回应",
            "audio_url": audio_path,
            "judgment": {
                "score": abs(dominance_shift),
                "comment": judgment,
                "type": "pancake" if dominance_shift > 0 else "garlic"
            },
            "game_state": {
                "round": session["round"],
                "pancake_score": session["pancake_score"],
                "garlic_score": session["garlic_score"]
            }
        }

        return response

    async def get_rescue(self, session_id: str) -> Dict[str, str]:
        """获取救场建议"""
        if session_id not in self.sessions:
            raise ValueError("会话不存在")

        session = self.sessions[session_id]
        orchestrator = self._get_orchestrator()

        # 获取orchestrator session
        orch_session_id = session.get("orch_session_id")
        if not orch_session_id:
            return {
                "suggestion": "请先开始对话",
                "explanation": "还没有对话历史"
            }

        # 调用 Orchestrator 生成救场答案
        suggestion = orchestrator.get_rescue_suggestion(orch_session_id)

        return {
            "suggestion": suggestion,
            "explanation": "这是基于当前对话情境生成的高情商回复建议"
        }
