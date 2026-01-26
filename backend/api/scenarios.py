"""
场景管理 API
"""
from fastapi import APIRouter, HTTPException
from typing import List
from backend.models import Scenario

router = APIRouter()

# 场景配置（从原 app.py 迁移）
SCENARIOS = {
    "shandong_dinner": {
        "id": "shandong_dinner",
        "name": "山东人的饭桌",
        "description": "挑战大舅的劝酒功力和酒桌规矩",
        "type": "shandong_dinner"
    },
    "negotiation": {
        "id": "negotiation",
        "name": "商务谈判",
        "description": "与王总进行一场商务价格谈判",
        "type": "negotiation"
    },
    "debate": {
        "id": "debate",
        "name": "辩论赛",
        "description": "与反方辩手进行一场激烈辩论",
        "type": "debate"
    },
    "interview": {
        "id": "interview",
        "name": "压力面试",
        "description": "挑战刷人的HR总监压力面试",
        "type": "interview"
    }
}


@router.get("/", response_model=List[Scenario])
async def get_scenarios():
    """获取所有场景列表"""
    return [
        Scenario(**scenario)
        for scenario in SCENARIOS.values()
    ]


@router.get("/{scenario_id}", response_model=Scenario)
async def get_scenario(scenario_id: str):
    """获取单个场景详情"""
    if scenario_id not in SCENARIOS:
        raise HTTPException(status_code=404, detail="场景不存在")

    return Scenario(**SCENARIOS[scenario_id])
