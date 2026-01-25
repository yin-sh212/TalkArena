"""
TalkArena 主题样式 - 简化版
"""

CUSTOM_CSS = """
/* Gradio 6.2 适配 - 完全重置 */
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

#root, #app, .gradio-app {
    width: 100% !important;
    height: 100vh !important;
    overflow: hidden !important;
    position: relative !important;
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
}

/* 所有页面容器默认隐藏 */
.scene-select-page,
.config-page,
.chat-page,
.report-page {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    display: none !important;
    z-index: 1 !important;
}

/* 只显示 visible的页面 */
.scene-select-page:not([style*="display: none"]),
.config-page:not([style*="display: none"]),
.chat-page:not([style*="display: none"]),
.report-page:not([style*="display: none"]) {
    display: flex !important;
}

/* Page 1: 场景选择页 */
.scene-select-page {
    flex-direction: column !important;
    background: #E6F0FF !important;
    overflow-y: auto !important;
    justify-content: flex-start !important;
    align-items: center !important;
    padding: 60px 40px !important;
}

.scenario-grid {
    width: 100% !important;
    max-width: 1200px !important;
    margin: 20px 0 !important;
    gap: 20px !important;
}



/* Page 3: 对话页 */
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
    min-height: 120px !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}

.scenario-card:hover {
    transform: translateY(-4px) !important;
    background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%) !important;
    border-color: #4A90E2 !important;
    box-shadow: 0 8px 24px rgba(74, 144, 226, 0.2) !important;
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
    width: 100%;
    height: 100%;
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

/* Page 2: 配置页 */
.config-page {
    flex-direction: column !important;
    background: linear-gradient(135deg, #FFF9F0 0%, #FFE8CC 100%) !important;
    padding: 40px 60px !important;
    overflow-y: auto !important;
    box-sizing: border-box !important;
}

/* Page 4: 复盘报告页 */
.report-page {
    flex-direction: column !important;
    background: #2c313c !important;
    padding: 0 !important;
    overflow: hidden !important;
}

.report-buttons {
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    display: flex !important;
    gap: 12px !important;
    z-index: 1000 !important;
}

.btn-dark {
    background: #1a1a1a !important;
    color: white !important;
    padding: 14px 24px !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: bold !important;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}

.btn-dark:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
    filter: brightness(1.1) !important;
}

.btn-light {
    background: white !important;
    color: #333 !important;
    padding: 14px 24px !important;
    border-radius: 12px !important;
    border: 1px solid #ddd !important;
    font-weight: bold !important;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}

.btn-light:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}

.btn-purple {
    background: #8e7cc3 !important;
    color: white !important;
    padding: 14px 24px !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: bold !important;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}

.btn-purple:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 20px rgba(142, 124, 195, 0.4) !important;
    filter: brightness(1.1) !important;
}

.config-page-title {
    font-size: 36px;
    font-weight: 900;
    color: #D48806;
    text-align: center;
    margin-bottom: 10px;
}

.config-page-subtitle {
    font-size: 18px;
    color: #8C6D3D;
    text-align: center;
    margin-bottom: 40px;
}

.section-title {
    font-size: 20px;
    font-weight: bold;
    color: #333;
    margin: 30px 0 15px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.ai-badge {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-size: 12px;
    padding: 3px 10px;
    border-radius: 12px;
    font-weight: normal;
}

.scenario-cards-row {
    display: flex !important;
    gap: 15px !important;
    margin-bottom: 20px !important;
}

.scene-card {
    flex: 1 !important;
    padding: 20px !important;
    background: white !important;
    border: 2px solid #E5E7EB !important;
    border-radius: 12px !important;
    transition: all 0.3s !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

.scene-card:hover {
    border-color: #F5A623 !important;
    box-shadow: 0 4px 12px rgba(245, 166, 35, 0.2) !important;
    transform: translateY(-2px) !important;
}

.roster-container {
    display: flex;
    gap: 20px;
    margin: 20px 0;
}

.roster-card {
    flex: 1;
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: all 0.3s;
}

.roster-card:hover {
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    transform: translateY(-4px);
}

.roster-avatar {
    font-size: 48px;
    text-align: center;
    margin-bottom: 10px;
}

.roster-name {
    font-size: 20px;
    font-weight: bold;
    color: #1a237e;
    text-align: center;
    margin-bottom: 8px;
}

.roster-role {
    font-size: 14px;
    color: #5B6BF9;
    text-align: center;
    font-weight: 600;
    margin-bottom: 10px;
}

.roster-personality {
    font-size: 13px;
    color: #666;
    line-height: 1.6;
    text-align: center;
}

.secondary-btn {
    background: white !important;
    border: 2px solid #E5E7EB !important;
    color: #333 !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-size: 14px !important;
    margin: 10px 5px !important;
}

.secondary-btn:hover {
    border-color: #F5A623 !important;
    background: #FFF9F0 !important;
}

.start-game-btn {
    width: 100% !important;
    height: 60px !important;
    font-size: 20px !important;
    font-weight: bold !important;
    background: linear-gradient(135deg, #F5A623 0%, #D48806 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    margin-top: 30px !important;
    box-shadow: 0 6px 20px rgba(245, 166, 35, 0.4) !important;
}

.start-game-btn:hover {
    box-shadow: 0 8px 25px rgba(245, 166, 35, 0.5) !important;
    transform: translateY(-2px) !important;
}

.back-link-btn {
    background: transparent !important;
    color: #8C6D3D !important;
    border: none !important;
    margin-top: 15px !important;
    font-size: 14px !important;
}

.back-link-btn:hover {
    color: #D48806 !important;
    text-decoration: underline !important;
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