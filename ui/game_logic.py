"""
游戏核心逻辑模块
处理回合判定、评分、剧情生成
"""
from typing import Dict, List, Tuple, Optional
import json
from orchestrator import logger

class GameJudge:
    """游戏裁判系统"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def evaluate_turn(self, scene_desc: str, npc_list: List[Dict], history: List[Tuple[str, str]]) -> Dict:
        """回合评估"""
        
        history_text = "\n".join([f"{name}: {text}" for name, text in history])
        npc_text = "\n".join([f"{i+1}. {npc['name']} - {npc['role']} - {npc['personality']}" 
                              for i, npc in enumerate(npc_list)])
        
        prompt = f"""# Role
你是"山东人饭局情商大挑战"的裁判和评论员，精通中国人的酒局潜规则，负责对**玩家最新发言**做评判。

# Background
中国人的饭局社交文化讲究：尊卑有序、言语得体、敬酒时机、场面话的艺术。
得体（Pancake）：幽默、周全、高情绪价值、尊重长辈/领导、符合规矩。
失礼（Garlic）：冷场、顶撞、不懂座次、言语冒犯、不识抬举。

# Input
- 场景描述：{scene_desc}
- NPC设定列表：
{npc_text}
- 历史对话：
{history_text}

# Task Instructions
1. 裁判： 评估玩家最新发言（`history_log`中最后一条）。若非常得体，pancake为true；若表现失礼，garlic为true；其余情况均为false。
2. 评价： 给出一段20-45字的评价，得体时给予夸奖，失礼时给予尖锐嘲讽。需简明扼要、一语中的，语言风格口语化、有顿挫感、有人情味。

# Output Format (Strict JSON)
{{
"pancake": boolean,
"garlic": boolean,
"feedback": string
}}

# Constraints
- 只输出 JSON格式，不得输出任何额外解释文字
- pancake 和 garlic 不能同时为 true。如果用户最新发言表现平平，两者皆为 false。

请输出JSON："""
        
        result = self.llm.generate(prompt, max_new_tokens=200)
        
        try:
            result_json = json.loads(result)
            return result_json
        except:
            logger.warning(f"[裁判] JSON解析失败: {result}")
            return {"pancake": False, "garlic": False, "feedback": "评判中..."}
    
    def generate_next_turn(self, scene_desc: str, npc_list: List[Dict], history: List[Tuple[str, str]]) -> Dict:
        """生成下一回合对话"""
        
        history_text = "\n".join([f"{name}: {text}" for name, text in history])
        npc_text = "\n".join([f"{i+1}. {npc['name']} - {npc['role']} - {npc['personality']}" 
                              for i, npc in enumerate(npc_list)])
        
        prompt = f"""# Role
你是"山东人饭局情商大挑战"的剧情导演。你需要根据当前的氛围，选出一个最适合继续发言的角色，续写对话。

# Input
- 场景描述：{scene_desc}
- NPC设定列表：
{npc_text}
- 历史对话：
{history_text}

# Task
1.选人：从 NPC 列表中选出此时此刻最适合接话的人，输出其编号（1-{len(npc_list)}）。
2.接话：根据该 NPC 的性格和场景设定，针对最后一位发言人的发言进行回应。回复必须口语化，贴合上下文。

# Output Format (Strict JSON)
{{
"speakerIndex": int,
"response": string
}}

# Constraints
- 只输出 JSON格式，不得输出任何额外解释文字

请输出JSON："""
        
        result = self.llm.generate(prompt, max_new_tokens=300)
        
        try:
            result_json = json.loads(result)
            return result_json
        except:
            logger.warning(f"[剧情] JSON解析失败: {result}")
            return {"speakerIndex": 1, "response": "（沉默了一会儿）"}
    
    def get_rescue_suggestion(self, scene_desc: str, npc_list: List[Dict], history: List[Tuple[str, str]]) -> str:
        """获取救场建议"""
        
        history_text = "\n".join([f"{name}: {text}" for name, text in history])
        npc_text = "\n".join([f"{i+1}. {npc['name']} - {npc['role']} - {npc['personality']}" 
                              for i, npc in enumerate(npc_list)])
        
        prompt = f"""# Role
你是一位混迹山东官场与商场三十年的"饭局天花板"——山东饭局高人，深谙说话的艺术。

# Context
在"山东人饭局情商大挑战"游戏中，玩家在最近一轮对话中表现拙劣，需要你传授一句"标准答案"。
中国人的饭局社交文化讲究：尊卑有序、言语得体、敬酒时机、场面话的艺术。

# Input
- 场景描述：{scene_desc}
- NPC设定列表：
{npc_text}
- 历史对话：
{history_text}

# Task
根据当前的场景和之前的对话历史，提供一句得体、热情且周全的发言，替代玩家最新的一次发言。要求：
- 有身份感： 要符合玩家的身份（通常是晚辈或下属）
- 幽默感： 可以适当自黑或通过捧高对方来化解矛盾
- 地道、口语化，但不过分油腻。
- 真诚、热情，能提供高情绪价值。

# Output
(直接输出建议的发言内容，无需任何前缀、引号等多余内容)

建议发言："""
        
        suggestion = self.llm.generate(prompt, max_new_tokens=200)
        return suggestion.strip()
