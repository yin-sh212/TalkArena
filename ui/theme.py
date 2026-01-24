"""
TalkArena 主题样式 - 简化版
"""

CUSTOM_CSS = """
/* 全局根容器适配 */
#app, .gradio-app, .gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
}

/* Page 1: 场景选择页 */
.scene-select-page {
    flex: 1 !important;
    min-height: 100vh !important;
    background: #E6F0FF !important;
    display: flex !important;
    flex-direction: row !important;
}

/* 左侧场景选择区 - 60% */
.scene-select-page .column:first-child,
.scene-select-page [data-testid="column"]:first-child,
.scene-select-page > div:first-child {
    width: 60% !important;
    min-width: 60% !important;
    max-width: 60% !important;
    flex: 0 0 60% !important;
    background: #E6F0FF !important;
    padding: 30px 40px !important;
    display: flex !important;
    flex-direction: column !important;
}

/* 右侧登录区 - 40% */
.scene-select-page .column:last-child,
.scene-select-page [data-testid="column"]:last-child,
.scene-select-page > div:last-child {
    width: 40% !important;
    min-width: 40% !important;
    max-width: 40% !important;
    flex: 0 0 40% !important;
    background: white !important;
    padding: 40px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    border-left: 1px solid #E2E8F0 !important;
}

/* 登录表单容器 */
.scene-select-page > div:last-child > div {
    width: 100% !important;
    max-width: 320px !important;
}

/* Page 2: 对话页 */
.chat-page {
    flex: 1 !important;
    height: 100vh !important;
    max-height: 100vh !important;
    padding: 0 !important;
    margin: 0 !important;
    background: #F8FAFC !important;
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
    z-index: 100 !important;
}

/* 中间主内容行 */
.chat-page > .row,
.chat-page > [data-testid="row"] {
    flex: 1 !important;
    min-height: 0 !important;
    display: flex !important;
    gap: 0 !important;
    margin: 0 !important;
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

/* 聊天框容器 - 固定高度 + 滚动 */
.chat-box-container {
    flex: 1 1 auto !important;
    min-height: 200px !important;
    max-height: calc(100vh - 350px) !important;
    background: #FAFAFA !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}

/* Gradio 6.x Chatbot 内部滚动穿透 */
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
    margin-top: 10px !important;
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

/* 品牌标题 */
.brand-title {
    color: #1a237e;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 4px;
}

.brand-subtitle {
    color: #1a237e;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 24px;
    opacity: 0.8;
}

/* 场景卡片 */
.scenario-card {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin-bottom: 12px !important;
    border: 2px solid transparent !important;
    box-shadow: 0 4px 10px rgba(74, 144, 226, 0.1) !important;
    text-align: left !important;
    white-space: pre-wrap !important;
    min-height: 70px !important;
}

.scenario-card:hover {
    background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%) !important;
    border-color: #4A90E2 !important;
}

.footer-action {
    margin-top: 20px;
    text-align: center;
    color: #1a237e;
    font-weight: bold;
    font-size: 16px;
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
    padding: 5px 0;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: flex-end;
    height: 140px;
    border-radius: 12px;
    overflow: hidden;
}

.seat-wrapper {
    display: flex;
    align-items: flex-end;
    gap: 30px;
    position: relative;
    z-index: 2;
}

.avatar-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
}

.avatar-img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #ddd;
    border: 2px solid white;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}

.avatar-box.center .avatar-img {
    width: 65px;
    height: 65px;
    border-color: #5B6BF9;
    font-size: 32px;
}

.speaking-indicator {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #5B6BF9;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 10px;
    border: 2px solid white;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.8; }
    100% { transform: scale(1); opacity: 1; }
}

.role-badge {
    margin-top: -8px;
    background: #333;
    color: white;
    font-size: 10px;
    padding: 1px 8px;
    border-radius: 10px;
    z-index: 2;
}

.table-curve {
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    height: 50px;
    background: white;
    border-radius: 100% 100% 0 0 / 200% 200% 0 0;
    z-index: 1;
}

/* 左上角分数板 */
.score-board-left {
    position: absolute;
    top: 15px;
    left: 15px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(4px);
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 10px 18px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    z-index: 3;
}

.score-board-left .score-label-mini {
    font-size: 11px;
    color: #666;
    font-weight: bold;
}

.score-board-left .score-val-large {
    font-size: 32px;
    font-weight: 900;
    color: #D32F2F;
    line-height: 1.1;
}

/* 右上角煎饼大蒜 */
.score-board-right {
    position: absolute;
    top: 15px;
    right: 15px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(4px);
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    display: flex;
    align-items: center;
    padding: 8px 15px;
    gap: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    z-index: 3;
}

.score-board-right .score-item-mini {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
}

.score-board-right .score-val-mini {
    font-size: 18px;
    font-weight: 900;
}

.score-board-right .score-label-mini {
    font-size: 10px;
    color: #888;
}

.score-board-right .face { color: #D48806; }
.score-board-right .gaffe { color: #722ED1; }

/* 删除旧的浮动计分板样式引用 */
.score-board-floating {
    display: none !important;
}

.critique-box {
    width: 100%;
    background: #FFF1F0;
    border: 1px solid #FFCCC7;
    border-radius: 8px;
    padding: 8px 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    position: relative;
    margin: 0 auto 8px auto;
}

.float-tag {
    position: absolute;
    top: -12px;
    right: 10px;
    background: #1F2937;
    color: white;
    font-size: 10px;
    padding: 2px 10px;
    border-radius: 10px 10px 10px 0;
}

.critique-text {
    color: #CF1322;
    font-size: 12px;
}

#status-display {
    font-size: 11px !important;
    color: #1a237e !important;
    opacity: 0.7 !important;
    text-align: center !important;
}

.mic-container-floating {
    background: white !important;
    border-radius: 12px !important;
    box-shadow: 0 -4px 15px rgba(0,0,0,0.1) !important;
    padding: 10px !important;
    margin-bottom: 5px !important;
}
"""