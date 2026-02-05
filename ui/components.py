"""
Verbal Dojo UI 组件
按照HTML原型精准复刻
"""


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
