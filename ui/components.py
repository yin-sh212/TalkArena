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


def render_aura_dashboard(user_score: int, ai_score: int, theme_color: str = "#4A90E2") -> str:
    """渲染顶栏气场和评分 (新版：左气场，右评分)"""
    return f'''
    <div class="top-header-bar">
        <div class="aura-mini-display">
            <div class="aura-label">气场</div>
            <div class="aura-bar-container">
                <div class="aura-bar-fill user" style="width: {user_score}%; background: {theme_color};"></div>
                <div class="aura-bar-fill ai" style="width: {ai_score}%; background: #C62828;"></div>
            </div>
            <div class="aura-values">{user_score} : {ai_score}</div>
        </div>
        <div class="performance-score">
            <div class="score-label">当前表现</div>
            <div class="score-value">{user_score}</div>
        </div>
    </div>
    '''


def render_avatar_section(user_name: str, ai_name: str, user_score: int = 50, ai_score: int = 50, theme_color: str = "#4A90E2", characters: list = None) -> str:
    """渲染聊天区头部的头像，支持多角色显示"""
    user = get_current_user()
    
    # 根据气场值计算头像大小 (40-80px)
    user_size = 40 + int(user_score * 0.4)
    ai_size = 40 + int(ai_score * 0.4)
    user_font = user_size // 3
    ai_font = ai_size // 3
    
    # 构建多角色显示
    ai_avatars_html = ""
    if characters:
        # 如果是多角色，横向排列
        for char in characters:
            ai_avatars_html += f'''
            <div class="avatar-wrapper multi-char">
                <div class="avatar-circle opponent small" style="border: 2px solid {theme_color};">
                    {char.get('avatar', '🤖')}
                </div>
                <div class="avatar-name">{char['name']}</div>
            </div>
            '''
    else:
        # 单角色
        ai_avatars_html = f'''
        <div class="avatar-wrapper">
            <div class="avatar-circle opponent" style="width:{ai_size}px; height:{ai_size}px; font-size:{ai_font}px; border: 3px solid {theme_color};">
                🤖
            </div>
            <div class="avatar-name">{ai_name}</div>
            <div class="avatar-score">{ai_score}</div>
        </div>
        '''

    return f'''
    <div class="avatar-section">
        <div class="avatar-wrapper">
            <div class="avatar-circle" style="width:{user_size}px; height:{user_size}px; font-size:{user_font}px; border: 3px solid white;">
                {user.avatar_letter}
            </div>
            <div class="avatar-name">{user_name}</div>
            <div class="avatar-score">{user_score}</div>
        </div>
        <div class="vs-badge" style="background: {theme_color};">VS</div>
        <div class="ai-group-wrapper">
            {ai_avatars_html}
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


def render_visual_stage(characters: list = None, current_speaker: str = None, user_score: int = 50, ai_score: int = 50) -> str:
    """渲染视觉舞台区 (山东饭局特色)
    左上角：当前表现分数
    右上角：煎饼大蒜
    """
    if not characters:
        return ""
    
    try:
        u_score = int(user_score)
        a_score = int(ai_score)
    except (ValueError, TypeError):
        print(f"[DEBUG] render_visual_stage got invalid types: user_score={type(user_score)}, ai_score={type(ai_score)}")
        u_score = 50
        a_score = 50
    
    pancakes = u_score // 10
    garlic = (100 - u_score) // 20
    
    ai_seats_html = ""
    for i, char in enumerate(characters):
        is_speaking = char['name'] == current_speaker
        speaking_indicator = '<div class="speaking-indicator">💬</div>' if is_speaking else ""

        ai_seats_html += f'''
        <div class="avatar-box">
            <div class="avatar-img" style="background: #FCD34D;">
                {char.get('avatar', '🤖')}
                {speaking_indicator}
            </div>
            <div class="role-badge">{char['name']}</div>
            <div class="role-desc">{char.get('bio', '')[:20]}...</div>
        </div>
        '''

    return f'''
    <div class="stage-container">
        <!-- 左上角：当前表现分数 -->
        <div class="score-board-left">
            <div class="score-label-mini">当前表现</div>
            <div class="score-val-large">{u_score}</div>
        </div>
        
        <!-- 右上角：煎饼大蒜 -->
        <div class="score-board-right">
            <div class="score-item-mini face">
                <span class="score-val-mini">🥞 {pancakes}</span>
                <span class="score-label-mini">煎饼(面子)</span>
            </div>
            <div class="score-item-mini gaffe">
                <span class="score-val-mini">🧄 {garlic}</span>
                <span class="score-label-mini">大蒜(失礼)</span>
            </div>
        </div>

        <div class="seat-wrapper">
            {ai_seats_html}
        </div>

        <div class="table-curve"></div>
    </div>
    '''


def render_aura_sidebar(user_score: int, ai_score: int) -> str:
    """渲染侧边栏垂直气场条"""
    return f'''
    <div class="aura-side-panel">
        <div class="aura-vertical-label">对峙气场</div>
        <div class="aura-vertical-bar">
            <div class="aura-vertical-fill ai" style="height: {ai_score}%;"></div>
            <div class="aura-vertical-fill user" style="height: {user_score}%;"></div>
        </div>
        <div class="aura-vertical-values">
            <div class="val-ai">AI: {ai_score}</div>
            <div class="val-user">YOU: {user_score}</div>
        </div>
    </div>
    '''


def render_critique_box(judgment: str = "势均力敌", show_rescue: bool = True) -> str:
    """渲染判定反馈框"""
    if not judgment:
        return ""
        
    rescue_btn_html = ""
    # 注意：这里的按钮点击事件需要在 app.py 中绑定，这里只提供样式占位或简单的HTML按钮
    # 但 Gradio 最好还是用组件。这里我们返回 HTML，并在 app.py 里用一个真正的按钮覆盖或配合使用。
    # 为了保持精修前端的感觉，我们返回带样式的容器。
    
    return f'''
    <div class="critique-box">
        <div class="float-tag">局面判定</div>
        <div class="critique-text">
            <span class="thumb-icon">{'👍' if '优' in judgment or '好' in judgment else '🧐'}</span>
            {judgment}
        </div>
    </div>
    '''
