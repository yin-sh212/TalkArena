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
    background: #FFFFFF !important;
    padding: 40px !important;
}

/* Page 2: 对话页 */
.chat-page {
    min-height: 100vh !important;
}

.chat-page > div:first-child {
    width: 260px !important;
    min-width: 260px !important;
    background: #E6F0FF !important;
    padding: 16px !important;
}

.chat-page > div:last-child {
    flex: 1 !important;
    background: #F5F7FA !important;
    padding: 20px 40px !important;
    display: flex !important;
    flex-direction: column !important;
}

/* 品牌标题 */
.brand-title {
    color: #1a237e;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 8px;
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
    border-radius: 16px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 8px 20px rgba(74, 144, 226, 0.3);
}

.aura-header {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    font-weight: bold;
    color: #1a237e;
    margin-bottom: 10px;
}

.aura-scores {
    display: flex;
    justify-content: space-between;
    font-size: 48px;
    font-weight: 900;
    color: #1a237e;
    margin-bottom: 15px;
}

.progress-container {
    height: 20px;
    background: #D8D8D8;
    border-radius: 10px;
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
    border-radius: 8px !important;
    margin-top: 20px !important;
}

/* 头像区 */
.avatar-section {
    display: flex;
    justify-content: center;
    gap: 40px;
    align-items: flex-end;
    padding: 10px;
}

.avatar-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.avatar-circle {
    border-radius: 50%;
    background: white;
    border: 3px solid #66A6FF;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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
    margin-top: 6px;
    font-weight: bold;
    font-size: 14px;
    color: #333;
}

.avatar-score {
    font-size: 18px;
    font-weight: 900;
    color: #1a237e;
}

/* 聊天框 */
.chat-box-container {
    min-height: 250px !important;
    max-height: 400px !important;
    overflow-y: auto !important;
}

/* 总结区域 */
.summary-box {
    background: #f0f8ff;
    border: 1px solid #66A6FF;
    border-radius: 12px;
    padding: 16px;
    margin: 10px 0;
    max-height: 300px;
    overflow-y: auto;
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
    border-radius: 25px !important;
    padding: 6px 12px !important;
    margin-top: 15px !important;
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
    background: rgba(255,255,255,0.3) !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    padding: 0 !important;
}

/* 隐藏footer */
footer {
    display: none !important;
}
"""
