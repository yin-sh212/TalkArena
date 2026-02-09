"""
TalkArena 主题样式 - 优化版
"""

CUSTOM_CSS = """
/* ====================================
   基础重置（必须使用 !important 覆盖 Gradio）
   ==================================== */
* {
    box-sizing: border-box;
}

body, html {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

/* Gradio 根容器重置 */
#root, #app, .gradio-app {
    width: 100% !important;
    height: 100vh !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}

.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    height: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
    border: none !important;
}

.gradio-container > div,
[data-testid="column"] {
    border: none !important;
}

/* ====================================
   页面布局系统
   ==================================== */
.scene-select-page,
.config-page,
.chat-page,
.report-page {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 1;
    border: none;
    display: flex;
    flex-direction: column;
}

/* 处理Gradio的hidden attribute */
.scene-select-page[hidden],
.config-page[hidden],
.chat-page[hidden],
.report-page[hidden] {
    display: none !important;
}

/* ====================================
   场景选择页
   ==================================== */
.scene-select-page {
    flex-direction: column;
    background: #E6F0FF;
    overflow: hidden;
    justify-content: center;
    align-items: center;
    padding: 2vh 2vw;
    gap: 2vh;
}

.scenario-grid {
    width: 100%;
    max-width: 1200px;
    margin: 20px 0;
    gap: 20px;
}

/* ====================================
   配置页
   ==================================== */
.config-page {
    flex-direction: column;
    background: #E6F0FF;
    padding: 2vh 3vw;
    overflow: hidden;
}

.config-page > * {
    border: none;
}

.config-page-title {
    font-size: 28px;
    font-weight: 900;
    color: #C8102E;
    text-align: center;
    margin-bottom: 0.5vh;
}

.config-page-subtitle {
    font-size: 15px;
    color: #8B0000;
    text-align: center;
    margin-bottom: 2vh;
}

.section-title {
    font-size: 17px;
    font-weight: bold;
    color: #333;
    margin: 1.5vh 0 1vh;
}

.ai-badge {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 12px;
    margin-left: 10px;
    font-weight: normal;
}

/* 场景卡片行 */
.scenario-cards-row {
    gap: 1vw;
    margin-bottom: 1.5vh;
}

/* 场景卡片 */
.scene-card {
    flex: 1;
    min-width: 150px;
    padding: 1.5vh 1vw;
    background: white;
    border: 2px solid #E5E7EB;
    border-radius: 1vh;
    font-size: 15px;
    font-weight: 600;
    color: #333;
    cursor: pointer;
    transition: all 0.3s ease;
}

.scene-card:hover {
    border-color: #C8102E;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(200, 16, 46, 0.15);
}

.scene-card-selected {
    border-color: #C8102E;
    border-width: 2px;
    background: #FFE6E6;
    box-shadow: 0 4px 12px rgba(200, 16, 46, 0.2);
}

/* 场景描述 */
.scene-desc-container {
    margin: 1.5vh 0 2vh 0;
    padding: 0;
}

.scene-desc-container textarea {
    min-height: 6vh;
    background: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-radius: 1vh;
    padding: 1vh;
    font-size: 13px;
    line-height: 1.6;
    color: #555;
}

.scene-desc-container label {
    font-weight: 600;
    color: #555;
    margin-bottom: 0.5vh;
}

/* 成员卡片行 */
.roster-row {
    gap: 1.5vw;
    margin-bottom: 1.5vh;
}

/* 成员卡片 */
.roster-card {
    flex: 1;
    min-width: 200px;
    padding: 2vh 1vw;
    background: white;
    border: 2px solid #E5E7EB;
    border-radius: 1vh;
    font-size: 13px;
    line-height: 1.8;
    color: #555;
    cursor: pointer;
    transition: all 0.3s ease;
    white-space: pre-line;
    text-align: center;
}

.roster-card:hover {
    border-color: #C8102E;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.roster-card-selected {
    border-color: #C8102E;
    border-width: 2px;
    background: #FFE6E6;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* 按钮 */
.secondary-btn {
    padding: 1vh 1.5vw;
    background: white;
    border: 2px solid #E5E7EB;
    border-radius: 1vh;
    color: #666;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.secondary-btn:hover {
    border-color: #999;
    color: #333;
}

.start-game-btn {
    width: 100%;
    padding: 2vh;
    background: #C8102E;
    border: none;
    border-radius: 1vh;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 1.5vh 0;
}

.start-game-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(200, 16, 46, 0.4);
    background: #D32F2F;
}

.back-link-btn {
    background: transparent;
    border: none;
    color: #999;
    font-size: 14px;
    cursor: pointer;
    text-decoration: underline;
}

/* ====================================
   对话页
   ==================================== */
.chat-page {
    flex-direction: column !important;
    background: #F8FAFC !important;
    overflow: hidden !important;
}

.chat-page-inner {
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}

/* 舞台区 - 固定高度 */
#visual-stage {
    height: 140px !important;
    min-height: 140px !important;
    flex-shrink: 0 !important;
    background: white !important;
    border-bottom: 1px solid #E2E8F0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}

/* 中间主内容行 */
.chat-page > .row,
.chat-page > [data-testid="row"],
.chat-page-inner > .row,
.chat-page-inner > [data-testid="row"] {
    flex: 1 !important;
    display: flex !important;
    height: 100% !important;
    overflow: hidden !important;
}

/* 侧边栏 */
.side-controls {
    width: 100px !important;
    min-width: 100px !important;
    max-width: 100px !important;
    flex-shrink: 0 !important;
    height: 100% !important;
    background: #F8FAFC !important;
    border-right: 1px solid #E2E8F0 !important;
    padding: 10px 5px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 15px !important;
    overflow-y: auto !important;
}

/* 侧边栏按钮 */
.side-controls button {
    width: 80px !important;
    height: 36px !important;
    min-width: 80px !important;
    padding: 5px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 12px !important;
    border-radius: 8px !important;
}

/* ========== 右侧主对话区 - 关键布局 ========== */
.main-chat-col {
    flex: 1 !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 10px 15px !important;
    background: white !important;
    min-height: 0 !important;
    overflow: hidden !important;
}

/* 聊天框容器 - 自适应高度 */
.chat-box-container {
    flex: 1 !important;
    min-height: 0 !important;
    background: #FAFAFA !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}

/* AI消息气泡样式 - 山东饭局主题，靠左显示 */
.chat-box-container .message.bot,
.chat-box-container [data-testid="bot"] {
    background: linear-gradient(135deg, #FFF9F0 0%, #FFEFD5 100%) !important;
    border-left: 4px solid #F5A623 !important;
    padding: 14px 18px !important;
    margin: 10px 0 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(245, 166, 35, 0.1) !important;
    max-width: 80% !important;
    width: auto !important;
    align-self: flex-start !important;
    text-align: left !important;
}

/* 去掉AI消息内部嵌套元素的样式 */
.chat-box-container .message.bot *,
.chat-box-container [data-testid="bot"] * {
    background: none !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
}

/* 用户消息保持简洁，靠右显示 */
.chat-box-container .message.user,
.chat-box-container [data-testid="user"] {
    background: #E3F2FD !important;
    border-left: 4px solid #2196F3 !important;
    padding: 14px 18px !important;
    margin: 10px 0 !important;
    border-radius: 12px !important;
    max-width: 80% !important;
    width: auto !important;
    align-self: flex-end !important;
    text-align: left !important;
}

/* 去掉用户消息内部嵌套元素的样式 */
.chat-box-container .message.user *,
.chat-box-container [data-testid="user"] * {
    background: none !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
}

/* 角色名称（emoji + 粗体名字）突出显示 */
.chat-box-container .message strong,
.chat-box-container [data-testid="bot"] strong {
    color: #D48806 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    display: inline-block !important;
    margin-bottom: 8px !important;
}

/* 去掉Gradio 6.2的嵌套wrapper样式 */
.chat-box-container .message-wrap,
.chat-box-container .message-row,
.chat-box-container .message > div,
.chat-box-container [data-testid="user"] > div,
.chat-box-container [data-testid="bot"] > div {
    all: unset !important;
    display: contents !important;
}

/* Gradio 6.x Chatbot 内部滚动穿透，支持左右对齐 */
.chat-box-container > div,
.chat-box-container [role="log"],
.chat-box-container .chatbot {
    flex: 1 !important;
    min-height: 0 !important;
    height: 100% !important;
    max-height: 100% !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
}

/* 输入行 - 固定在底部 */
.input-row {
    flex: 0 0 auto !important;
    height: 56px !important;
    min-height: 56px !important;
    background: #6495ED !important;
    border-radius: 28px !important;
    padding: 0 20px !important;
    display: flex !important;
    align-items: center !important;
    margin-top: 20px !important;
    margin-bottom: 10px !important;
    box-shadow: 0 4px 15px rgba(100, 149, 237, 0.4) !important;
}

.input-row > .form {
    background: transparent !important;
    border: none !important;
}

.input-row input {
    background: transparent !important;
    border: none !important;
    color: white !important;
    flex: 1 !important;
    font-size: 16px !important;
}

.input-row input::placeholder {
    color: rgba(255,255,255,0.7) !important;
}

.input-row button {
    background: rgba(255,255,255,0.9) !important;
    color: #4A90E2 !important;
    border: none !important;
    border-radius: 16px !important;
    min-width: 60px !important;
    height: 36px !important;
    padding: 0 15px !important;
    font-weight: bold !important;
    font-size: 14px !important;
    margin-left: 10px !important;
}

/* 气场侧边栏 */
.aura-sidebar {
    width: 200px !important;
    min-width: 200px !important;
    max-width: 200px !important;
    flex-shrink: 0 !important;
    height: 100% !important;
    background: white !important;
    padding: 15px !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 15px !important;
}

/* 气场条 */
.aura-side-panel {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 10px 5px;
    background: white;
    border-radius: 10px;
    border: 1px solid #E5E7EB;
}

.aura-vertical-label {
    font-size: 11px;
    font-weight: bold;
    color: #1a237e;
    text-align: center;
}

.aura-vertical-bar {
    width: 14px;
    height: 120px;
    background: #E5E7EB;
    border-radius: 7px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.aura-vertical-fill {
    width: 100%;
    transition: height 0.5s ease;
}

.aura-vertical-fill.ai { background: #C62828; }
.aura-vertical-fill.user { background: #4A90E2; }

.aura-vertical-values {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    font-weight: bold;
}

.aura-vertical-values .val-ai { color: #C62828; }
.aura-vertical-values .val-user { color: #4A90E2; }

/* 按钮样式 */
.end-btn {
    background: #D32F2F !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
}

.back-btn {
    background: #4A90E2 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
}

.summon-btn-styled {
    background: #5B6BF9 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
}

.mic-toggle-btn {
    font-size: 18px !important;
    background: transparent !important;
    color: white !important;
}

/* 总结区域 */
.summary-box {
    background: #f0f8ff !important;
    border: 2px solid #66A6FF !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin: 10px 0 !important;
    max-height: 350px !important;
    overflow-y: auto !important;
}

/* 舞台容器 */
.stage-container {
    background: linear-gradient(180deg, #E6F0FF 0%, #FFFFFF 100%);
    padding: 10px 20px;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

/* 座位包装器 */
.seat-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    z-index: 2;
}

/* 角色头像卡片 */
.avatar-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    transition: transform 0.3s ease;
}

.avatar-box:hover {
    transform: translateY(-5px);
}

/* 中间主角色放大 */
.avatar-box.center .avatar-img {
    width: 70px;
    height: 70px;
    font-size: 36px;
}

.avatar-box.center .role-badge {
    font-size: 15px;
    padding: 6px 14px;
}

.avatar-box:hover {
    transform: translateY(-5px);
}

/* 头像图片 */
.avatar-img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    position: relative;
    transition: all 0.3s ease;
    border: 3px solid white;
}

/* 说话指示器 */
.speaking-indicator {
    position: absolute;
    top: -5px;
    right: -5px;
    font-size: 16px;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.8; }
}

/* 角色名称徽章 */
.role-badge {
    background: #333;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: bold;
    white-space: nowrap;
}

/* 角色描述 */
.role-desc {
    font-size: 11px;
    color: #666;
    text-align: center;
    max-width: 100px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 分数面板 - 左上角 */
.score-board-left {
    position: absolute;
    top: 10px;
    left: 15px;
    background: white;
    padding: 8px 15px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}

.score-label-mini {
    font-size: 11px;
    color: #666;
    font-weight: 600;
}

.score-val-large {
    font-size: 24px;
    font-weight: bold;
    color: #4A90E2;
}

/* 分数面板 - 右上角 */
.score-board-right {
    position: absolute;
    top: 10px;
    right: 15px;
    display: flex;
    gap: 10px;
}

.score-item-mini {
    background: white;
    padding: 6px 12px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}

.score-val-mini {
    font-size: 14px;
    font-weight: bold;
}

/* 桌子曲线装饰 */
.table-curve {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 20px;
    background: rgba(139, 69, 19, 0.2);
    border-radius: 50% 50% 0 0;
    z-index: 1;
}

/* 品评框 */
.critique-box {
    padding: 20px;
    background: #F8FAFC;
    border-radius: 12px;
    margin-bottom: 15px;
}

.critique-title {
    font-size: 16px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
}

.critique-content {
    font-size: 14px;
    color: #666;
    line-height: 1.6;
}

/* ====================================
   通用组件
   ==================================== */
.brand-title {
    font-size: 56px;
    font-weight: 900;
    color: #2C3E50;
    text-align: center;
    margin-bottom: 10px;
    letter-spacing: 2px;
}

.brand-subtitle {
    font-size: 20px;
    color: #7F8C8D;
    text-align: center;
    margin-bottom: 50px;
}

/* 场景卡片（选择页）*/
.scenario-card {
    background: white;
    border: 2px solid #E5E7EB;
    border-radius: 16px;
    padding: 30px;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 180px;
}

.scenario-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    border-color: #4A90E2;
}

/* 主场景卡片按钮 - 更醒目的样式 */
.scenario-card-main {
    background: #C8102E !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 40px 60px !important;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
    min-height: 120px !important;
    width: 100% !important;
    max-width: 600px !important;
    margin: 20px auto !important;
    box-shadow: 0 8px 30px rgba(200, 16, 46, 0.3) !important;
    font-size: 32px !important;
    font-weight: 900 !important;
    color: white !important;
    letter-spacing: 2px !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2) !important;
}

.scenario-card-main:hover {
    transform: translateY(-8px) scale(1.02) !important;
    box-shadow: 0 15px 40px rgba(200, 16, 46, 0.5) !important;
    background: #D32F2F !important;
}

/* 页脚 */
.footer-action {
    text-align: center;
    color: #999;
    font-size: 14px;
    margin-top: 40px;
    cursor: pointer;
}

/* 麦克风容器 */
.mic-container-floating {
    position: fixed;
    bottom: 90px;
    right: 30px;
    z-index: 100;
}

/* 复盘报告页 */
.report-page {
    flex-direction: column;
    background: #2c313c;
    padding: 0;
    overflow: hidden;
}

.report-buttons {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 15px;
    z-index: 100;
    justify-content: center;
}

/* 按钮样式统一 */
.btn-light {
    background: white;
    color: #333;
    padding: 10px 20px;
    border: 2px solid #E5E7EB;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    height: 40px;
    min-width: 120px;
    max-width: 160px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.btn-light:hover {
    border-color: #999;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-purple {
    background: linear-gradient(135deg, #8E7CC3 0%, #6C5B7B 100%);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    height: 40px;
    min-width: 120px;
    max-width: 160px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.btn-purple:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(142, 124, 195, 0.4);
    filter: brightness(1.1);
}

/* ====================================
   响应式
   ==================================== */
@media (max-width: 768px) {
    .config-page {
        padding: 20px;
    }

    .scenario-cards-row,
    .roster-row {
        flex-direction: column;
    }

    .aura-sidebar {
        display: none;
    }
}
"""

