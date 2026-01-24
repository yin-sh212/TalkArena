"""
TalkArena 主题样式 - 简化版
"""

CUSTOM_CSS = """
/* 全局 */
.gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Page 1: 场景选择页 */
.scene-select-page {
    min-height: 100vh !important;
    background: #E6F0FF !important;
}

.scene-select-page > div:first-child {
    width: 280px !important;
    min-width: 280px !important;
    background: #E6F0FF !important;
    padding: 20px !important;
}

.scene-select-page > div:last-child {
    flex: 1 !important;
    background: #E6F0FF !important;
    padding: 40px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
}

.scene-select-page > div:last-child > div {
    background: white !important;
    padding: 30px !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
    min-width: 300px !important;
}

/* Page 2: 对话页 */
.chat-page {
    min-height: 100vh !important;
}

.chat-page > div:first-child {
    width: 220px !important;
    min-width: 220px !important;
    background: #E6F0FF !important;
    padding: 8px !important;
}

.chat-page > div:last-child {
    flex: 1 !important;
    background: #F5F7FA !important;
    padding: 10px 20px !important;
    display: flex !important;
    flex-direction: column !important;
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

/* 气场仪表盘 */
.aura-dashboard {
    background: linear-gradient(180deg, #89C4F4 0%, #66A6FF 100%);
    border-radius: 10px;
    padding: 8px;
    margin: 6px 0;
    box-shadow: 0 2px 6px rgba(74, 144, 226, 0.3);
}

.aura-header {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: bold;
    color: #1a237e;
    margin-bottom: 6px;
}

.aura-scores {
    display: flex;
    justify-content: space-between;
    font-size: 28px;
    font-weight: 900;
    color: #1a237e;
    margin-bottom: 6px;
}

.progress-container {
    height: 10px;
    background: #D8D8D8;
    border-radius: 5px;
    overflow: hidden;
}

.progress-bar-red {
    background: #C62828;
    height: 100%;
    transition: width 0.3s;
}

.rules-list-box {
    margin-top: 15px;
    font-size: 12px;
    color: #1a237e;
    opacity: 0.8;
    line-height: 1.8;
}

/* 结束按钮 */
.end-btn {
    background: #D32F2F !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    margin-top: 6px !important;
    cursor: pointer !important;
    pointer-events: auto !important;
    padding: 6px 12px !important;
}

.end-btn:hover {
    background: #B71C1C !important;
}

/* 头像区 */
.avatar-section {
    display: flex;
    justify-content: center;
    gap: 30px;
    align-items: flex-end;
    padding: 5px;
}

.avatar-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.avatar-circle {
    border-radius: 50%;
    background: white;
    border: 2px solid #66A6FF;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: #1a237e;
    transition: all 0.3s;
}

.avatar-circle.opponent {
    border-color: #FF8A80;
}

.avatar-name {
    margin-top: 4px;
    font-weight: bold;
    font-size: 12px;
    color: #333;
}

.avatar-score {
    font-size: 16px;
    font-weight: 900;
    color: #1a237e;
}

/* 聊天框 */
.chat-box-container {
    min-height: 200px !important;
    max-height: 280px !important;
    overflow-y: auto !important;
}

/* 总结区域 */
.summary-box {
    background: #f0f8ff !important;
    border: 2px solid #66A6FF !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin: 10px 0 !important;
    min-height: 150px !important;
    max-height: 350px !important;
    overflow-y: auto !important;
    color: #333 !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}

.summary-box h3 {
    color: #1a237e !important;
    margin-bottom: 12px !important;
}

.summary-box p, .summary-box li {
    color: #333 !important;
}

/* 返回按钮 */
.back-btn {
    background: #4A90E2 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    margin-top: 10px !important;
}

/* 输入区 */
.input-row {
    background: #6495ED !important;
    border-radius: 20px !important;
    padding: 4px 10px !important;
    margin-top: 8px !important;
    display: flex !important;
    align-items: center !important;
}

.input-row > div {
    background: transparent !important;
    border: none !important;
}

.input-row input {
    background: transparent !important;
    border: none !important;
    color: white !important;
    flex: 1 !important;
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
    height: 32px !important;
    padding: 0 16px !important;
    font-weight: bold !important;
    font-size: 14px !important;
}

.send-btn {
    background: rgba(255,255,255,0.9) !important;
    color: #4A90E2 !important;
    border-radius: 16px !important;
}

/* 隐藏footer */
footer {
    display: none !important;
}
"""
