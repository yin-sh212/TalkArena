"""
对话 API
"""
from fastapi import APIRouter, HTTPException
from backend.models import ChatMessage, ChatResponse, RescueRequest, RescueResponse
from backend.services import game_service

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    """发送消息并获取 AI 响应"""
    try:
        # 调用游戏服务处理消息
        response = await game_service.process_message(
            session_id=message.session_id,
            user_message=message.message,
            message_type=message.message_type
        )

        return ChatResponse(**response)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理消息失败: {str(e)}")


@router.post("/rescue", response_model=RescueResponse)
async def request_rescue(request: RescueRequest):
    """求救 - 获取高情商答案"""
    try:
        rescue_data = await game_service.get_rescue(request.session_id)

        return RescueResponse(**rescue_data)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"救场失败: {str(e)}")


@router.post("/voice")
async def process_voice(session_id: str):
    """处理语音输入（TODO: 实现文件上传）"""
    # TODO: 接收音频文件，使用 STT 转文字
    raise HTTPException(status_code=501, detail="语音功能开发中")
