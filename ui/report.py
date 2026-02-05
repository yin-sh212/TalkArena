"""
游戏结束后的复盘报告生成
"""
from typing import Dict, List, Tuple
import json
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

def get_medal_by_scores(scores: Dict[str, int]) -> str:
    """根据五维分数自动判定勋章称号"""
    oily = scores.get("oily", 0)
    friendliness = scores.get("friendliness", 0)
    logic = scores.get("logic", 0)
    humor = scores.get("humor", 0)
    respect = scores.get("respect", 0)
    
    score_list = [oily, friendliness, logic, humor, respect]
    avg = sum(score_list) / 5
    
    # 1. 极端/隐藏判定 (优先级最高)
    if oily < 15 and respect < 15:
        return "社交拆迁队"
    if logic > 80 and friendliness < 20:
        return "职场大炸弹"
    if friendliness > 85 and respect < 20:
        return "气氛终结者"
    if avg < 20:
        return "饭局背景板"
    
    # 2. 特色高分判定
    if respect > 85 and logic < 40:
        return "倒酒工具人"
    if logic > 85 and friendliness > 70:
        return "接话小天才"
    if oily > 85 and friendliness > 80:
        return "圆场大师"
    
    # 3. 常规等级判定 (兜底)
    if avg >= 85:
        return "酒桌老狐狸"
    if avg >= 70:
        return "饭局操盘手"
    if avg >= 50:
        return "点头专业户"
    if avg >= 30:
        return "饭桌木头人"
    
    return "初出茅庐"


def generate_radar_chart_base64(scores: Dict[str, int]) -> str:
    """生成雷达图并返回base64编码的图片"""
    try:
        import matplotlib
        matplotlib.use('Agg')  # 使用非交互式后端

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

        # 五维数据
        labels = ['圆滑度', '亲和力', '逻辑性', '幽默感', '懂规矩']
        values = [
            scores.get("oily", 0),
            scores.get("friendliness", 0),
            scores.get("logic", 0),
            scores.get("humor", 0),
            scores.get("respect", 0)
        ]

        # 为了闭合雷达图，需要将第一个值追加到末尾
        values_closed = values + [values[0]]

        # 角度计算
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles_closed = angles + [angles[0]]

        # 创建图形
        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(projection='polar'), facecolor='none')

        # 绘制雷达图
        ax.plot(angles_closed, values_closed, 'o-', linewidth=2, color='#4a5dca', label='你的表现')
        ax.fill(angles_closed, values_closed, alpha=0.25, color='#4a5dca')

        # 设置标签
        ax.set_xticks(angles)
        ax.set_xticklabels(labels, fontsize=10)

        # 设置刻度范围
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=8, color='#666')

        # 网格样式
        ax.grid(True, linestyle='--', alpha=0.3)

        # 背景透明
        ax.set_facecolor('none')
        fig.patch.set_alpha(0.0)

        # 保存为base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', transparent=True, bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)

        return f"data:image/png;base64,{image_base64}"
    except Exception as e:
        import logging
        logging.error(f"[雷达图生成失败] {e}")
        # 返回一个占位符SVG
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGV4dCB4PSIxNTAiIHk9IjE1MCIgZm9udC1zaXplPSIxOCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+6Zuv6L6+5Zu+5pqW5oiQ5aSx6LSlPC90ZXh0Pjwvc3ZnPg=="


def render_report_card(
    scene_name: str,
    medal: str,
    scores: Dict[str, int],
    summary: str,
    npc_os_list: List[Dict],
    suggestion: str
) -> str:
    """渲染复盘报告卡片HTML"""

    # 五维分数
    oily = scores.get("oily", 0)
    friendliness = scores.get("friendliness", 0)
    logic = scores.get("logic", 0)
    humor = scores.get("humor", 0)
    respect = scores.get("respect", 0)

    # 生成雷达图base64图片
    radar_chart_img = generate_radar_chart_base64(scores)
    
    # 构建NPC OS HTML
    npc_os_html = ""
    for npc in npc_os_list[:3]:  # 最多显示3个
        name = npc.get("name", "NPC")
        os_text = npc.get("os", "")
        avatar = npc.get("avatar", "👤")
        
        npc_os_html += f'''
        <div class="os-row">
            <div class="npc-avatar">{avatar}</div>
            <div class="os-bubble">
                <b>{name}</b>
                {os_text}
            </div>
        </div>
        '''
    
    html = f'''
    <div id="report-container" style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; background: #2c313c;">
        <div id="report-card" style="background: white; width: 940px; max-height: 90vh; border-radius: 24px; display: flex; overflow: hidden; box-shadow: 0 30px 60px rgba(0,0,0,0.4);">
            
            <!-- 左侧面板 -->
            <div style="flex: 1; padding: 40px; border-right: 1px dashed #eee; display: flex; flex-direction: column; align-items: center;">
                <div style="text-align: left; width: 100%;">
                    <h1 style="margin: 0; font-size: 26px; color: #1a1a1a;">局后复盘</h1>
                    <p style="color: #666; font-size: 13px; margin-top: 4px;">在"{scene_name}"中的表现</p>
                </div>
                
                <div style="background: #e74c3c; color: white; padding: 10px 20px; border-radius: 12px; font-weight: 800; font-size: 18px; transform: rotate(-3deg); box-shadow: 4px 8px 15px rgba(231, 76, 60, 0.3); margin: 20px 0; cursor: default; transition: all 0.3s;">
                    {medal}
                </div>

                <div style="width: 300px; height: 300px; margin: 10px 0; display: flex; align-items: center; justify-content: center;">
                    <img src="{radar_chart_img}" alt="能力雷达图" style="width: 100%; height: 100%; object-fit: contain;" />
                </div>
                
                <div style="display: flex; justify-content: space-between; width: 100%; margin-top: 20px; gap: 10px;">
                    <div style="flex: 1; background: #f8f9fa; padding: 10px 5px; border-radius: 10px; text-align: center; border: 1px solid #eee; transition: all 0.3s;">
                        <span style="display: block; font-size: 11px; color: #666; margin-bottom: 4px;">圆滑度</span>
                        <b style="font-size: 15px; color: #4a5dca;">{oily}</b>
                    </div>
                    <div style="flex: 1; background: #f8f9fa; padding: 10px 5px; border-radius: 10px; text-align: center; border: 1px solid #eee; transition: all 0.3s;">
                        <span style="display: block; font-size: 11px; color: #666; margin-bottom: 4px;">亲和力</span>
                        <b style="font-size: 15px; color: #4a5dca;">{friendliness}</b>
                    </div>
                    <div style="flex: 1; background: #f8f9fa; padding: 10px 5px; border-radius: 10px; text-align: center; border: 1px solid #eee; transition: all 0.3s;">
                        <span style="display: block; font-size: 11px; color: #666; margin-bottom: 4px;">逻辑性</span>
                        <b style="font-size: 15px; color: #4a5dca;">{logic}</b>
                    </div>
                    <div style="flex: 1; background: #f8f9fa; padding: 10px 5px; border-radius: 10px; text-align: center; border: 1px solid #eee; transition: all 0.3s;">
                        <span style="display: block; font-size: 11px; color: #666; margin-bottom: 4px;">幽默感</span>
                        <b style="font-size: 15px; color: #4a5dca;">{humor}</b>
                    </div>
                    <div style="flex: 1; background: #f8f9fa; padding: 10px 5px; border-radius: 10px; text-align: center; border: 1px solid #eee; transition: all 0.3s;">
                        <span style="display: block; font-size: 11px; color: #666; margin-bottom: 4px;">懂规矩</span>
                        <b style="font-size: 15px; color: #4a5dca;">{respect}</b>
                    </div>
                </div>
            </div>
            
            <!-- 右侧面板 -->
            <div style="flex: 1.3; padding: 40px; background: #fafafa; display: flex; flex-direction: column; gap: 15px; overflow-y: auto;">
                <div style="background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <h3 style="margin: 0 0 10px 0; font-size: 14px; color: #4a5dca; display: flex; align-items: center;">
                        <span style="margin-right: 8px;">💬</span> 综合点评
                    </h3>
                    <p style="margin: 0; font-size: 13px; line-height: 1.6; color: #333;">{summary}</p>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <h3 style="margin: 0 0 10px 0; font-size: 14px; color: #4a5dca; display: flex; align-items: center;">
                        <span style="margin-right: 8px;">🎭</span> NPC 内心 OS
                    </h3>
                    <div style="display: flex; flex-direction: column; gap: 10px;">
                        {npc_os_html}
                    </div>
                </div>
                
                <div style="background: #fffbe6; border: 1px solid #ffe58f; padding: 15px; border-radius: 14px; transition: all 0.3s;">
                    <b style="display: block; font-size: 14px; margin-bottom: 5px; color: #856404; border-bottom: 1px solid rgba(133, 100, 4, 0.1); padding-bottom: 3px;">
                        💡 改进建议
                    </b>
                    <p style="margin: 0; font-size: 13px; line-height: 1.5; color: #666;">{suggestion}</p>
                </div>
            </div>
        </div>
    </div>
    '''

    return html
