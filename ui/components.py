"""
Verbal Dojo UI 组件
按照HTML原型精准复刻
"""
from typing import Optional
from ui.user import get_current_user


def render_scenario_card(name: str, desc: str, active: bool = False) -> str:
    """渲染场景选择卡片"""
    active_class = "active" if active else ""
    return f'''
    <div class="scenario-card {active_class}">
        <div class="card-header">{name}</div>
        <div class="card-desc">{desc}</div>
    </div>
    '''


def render_aura_dashboard(user_score: int, ai_score: int) -> str:
    """渲染气场仪表盘（蓝色渐变背景）"""
    return f'''
    <div class="aura-dashboard">
        <div class="aura-header">
            <span>我的气场</span>
            <span>对方气场</span>
        </div>
        <div class="aura-scores">
            <span>{user_score}</span>
            <span>{ai_score}</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar-red" style="width: {user_score}%;"></div>
        </div>
        <div class="rules-list-box">
            * 规则提示:<br>
            · 思考超过3秒开始掉气场<br>
            · 对方思考也会掉气场<br>
            · 裁判实时评判每轮交锋
        </div>
    </div>
    '''


def render_avatar_section(user_name: str, ai_name: str, user_score: int = 50, ai_score: int = 50) -> str:
    """渲染聊天区头部的头像，根据气场值动态调整大小"""
    user = get_current_user()
    
    # 根据气场值计算头像大小 (40-80px)
    user_size = 40 + int(user_score * 0.4)
    ai_size = 40 + int(ai_score * 0.4)
    user_font = user_size // 3
    ai_font = ai_size // 3
    
    return f'''
    <div class="avatar-section">
        <div class="avatar-wrapper">
            <div class="avatar-circle" style="width:{user_size}px; height:{user_size}px; font-size:{user_font}px;">
                {user.avatar_letter}
            </div>
            <div class="avatar-name">{user_name}</div>
            <div class="avatar-score">{user_score}</div>
        </div>
        <div class="avatar-wrapper">
            <div class="avatar-circle opponent" style="width:{ai_size}px; height:{ai_size}px; font-size:{ai_font}px;">
                🤖
            </div>
            <div class="avatar-name">{ai_name}</div>
            <div class="avatar-score">{ai_score}</div>
        </div>
    </div>
    '''


def render_bubble(role: str, content: str, is_user: bool = False) -> str:
    """渲染单条消息气泡"""
    user = get_current_user()
    row_class = "user" if is_user else "ai"
    avatar_content = user.avatar_letter if is_user else "🤖"
    
    return f'''
    <div class="bubble-row {row_class}">
        <div class="bubble-avatar" style="background: {'#66A6FF' if is_user else '#999'}; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">
            {avatar_content}
        </div>
        <div class="bubble-content">{content}</div>
    </div>
    '''


def render_warning_box(seconds: int) -> str:
    """渲染沉默警告框"""
    if seconds <= 0:
        return ""
    return f'''
    <div class="warning-box">
        <span>⚠️</span>
        <span>沉默警告 {seconds}s</span>
    </div>
    '''


def render_input_pill() -> str:
    """渲染底部输入药丸"""
    return '''
    <div class="input-pill-container">
        <div class="input-pill">
            <div class="icon-btn">
                <span class="icon-mic">🎤</span>
            </div>
            <span class="input-text-placeholder">按住 空格键 说话</span>
            <div class="icon-btn">⌨</div>
        </div>
    </div>
    '''


def render_sidebar_brand() -> str:
    """渲染侧边栏品牌标题"""
    return '''
    <div class="brand-title">TalkArena</div>
    <div class="brand-subtitle">选择挑战场景</div>
    '''


def render_footer_action() -> str:
    """渲染底部自定义场景链接"""
    return '''
    <div class="footer-action">自定义场景 ?</div>
    '''


# 兼容旧接口
def render_dominance_bar(user_score: int, ai_score: int) -> str:
    """兼容旧接口的气场显示"""
    return render_aura_dashboard(user_score, ai_score)


def render_user_avatar(size: int = 40, letter: str = None) -> str:
    """渲染用户头像"""
    user = get_current_user()
    avatar_letter = letter or user.avatar_letter
    return f'''
    <div style="
        width: {size}px;
        height: {size}px;
        border-radius: 50%;
        background: #66A6FF;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: {size // 2}px;
        border: 4px solid #66A6FF;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    ">{avatar_letter}</div>
    '''


def render_sidebar(scenario_name: str, scenario_desc: str,
                   role1_name: str, role1_desc: str,
                   role2_name: str, role2_desc: str,
                   user_score: int, ai_score: int) -> str:
    """渲染对话页左侧边栏（兼容旧接口）"""
    return f'''
    <div class="brand-title">TalkArena</div>
    {render_aura_dashboard(user_score, ai_score)}
    '''


def render_chat_header(user_name: str, ai_name: str) -> str:
    """渲染聊天头部（兼容旧接口）"""
    return render_avatar_section(user_name, ai_name)


def render_silence_warning(seconds: int) -> str:
    """渲染沉默警告（兼容旧接口）"""
    return render_warning_box(seconds)


def get_avatar_url(seed: str) -> str:
    """获取头像URL（保留兼容性）"""
    return f"https://api.dicebear.com/7.x/bottts/svg?seed={seed}"
