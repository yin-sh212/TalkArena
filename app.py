"""
TalkArena - 主应用
"""
import gradio as gr
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ui.handlers import (
    get_scenarios, start_session, send_message,
    process_voice_input, end_session, init_models,
    handle_user_register, handle_rescue
)
from ui.theme import CUSTOM_CSS
from ui.components import (
    render_aura_dashboard, render_avatar_section,
    render_visual_stage, render_critique_box, render_aura_sidebar
)
from ui.user import get_current_user, register_user

SCENARIOS = {
    "negotiation": {"name": "商务谈判", "desc": "与王总进行一场商务价格谈判"},
    "debate": {"name": "辩论赛", "desc": "与反方辩手进行一场激烈辩论"},
    "interview": {"name": "压力面试", "desc": "挑战刷人的HR总监压力面试"},
    "shandong_dinner": {"name": "山东人的饭桌", "desc": "挑战大舅的劝酒功力和酒桌规矩"},
}


def create_ui():
    init_models()
    scenarios_data = get_scenarios()

    with gr.Blocks(title="TalkArena") as demo:
        session_id = gr.State("")
        current_scene = gr.State({"name": "", "sid": ""})

        # ========== Page 1: 场景选择页 ==========
        with gr.Column(visible=True, elem_classes="scene-select-page") as page_select:
            gr.HTML('<div class="brand-title">TalkArena</div>')
            gr.HTML('<div class="brand-subtitle">选择挑战场景</div>')

            scenario_buttons = []
            
            # 创建两列布局
            with gr.Row(elem_classes="scenario-grid"):
                with gr.Column(scale=1):
                    for i, (display_name, sid) in enumerate(scenarios_data):
                        if i % 2 == 0:  # 左列
                            cfg = SCENARIOS.get(sid, {"name": display_name, "desc": "开始挑战！"})
                            btn = gr.Button(
                                value=f"📋 {cfg['name']}\n{cfg['desc']}",
                                elem_classes="scenario-card"
                            )
                            scenario_buttons.append((btn, sid, cfg["name"], cfg["desc"]))
                
                with gr.Column(scale=1):
                    for i, (display_name, sid) in enumerate(scenarios_data):
                        if i % 2 == 1:  # 右列
                            cfg = SCENARIOS.get(sid, {"name": display_name, "desc": "开始挑战！"})
                            btn = gr.Button(
                                value=f"📋 {cfg['name']}\n{cfg['desc']}",
                                elem_classes="scenario-card"
                            )
                            scenario_buttons.append((btn, sid, cfg["name"], cfg["desc"]))

            gr.HTML('<div class="footer-action">自定义场景 ?</div>')

       # ========== Page 2: 角色配置页 (仅山东饭局) ==========
        with gr.Column(visible=False, elem_classes="config-page") as page_config:
            gr.HTML('<div class="config-page-title">山东人的饭桌</div>')
            gr.HTML('<div class="config-page-subtitle">选择你的饭局战场</div>')
            
            # 场景选择区
            gr.HTML('<div class="section-title">选择场景</div>')
            with gr.Row(elem_classes="scenario-cards-row"):
                scene_cards = []
                for scene in ["家庭聚会", "单位聚餐", "商务宴请", "同学聚会", "招待客户"]:
                    btn = gr.Button(scene, elem_classes="scene-card")
                    scene_cards.append(btn)
            
            selected_scene = gr.State("商务宴请")
            scene_desc = gr.Textbox(label="场景描述", value="高端局，主陪副陪分清，话权要巧妙抓住，让话题走在你的节奏。", lines=2, interactive=False)
            
            # 饭局成员区
            gr.HTML('<div class="section-title">饭局成员 <span class="ai-badge">AI生成</span></div>')
            
            with gr.Row(elem_classes="roster-row"):
                roster_html = gr.HTML("""
                <div class="roster-container">
                    <div class="roster-card">
                        <div class="roster-avatar">👨‍💼</div>
                        <div class="roster-name">王局长</div>
                        <div class="roster-role">主陪·局领导·威压全场</div>
                        <div class="roster-personality">深谙官场礼仪，对座次、敬酒顺序极为讲究，用话语掌控节奏…</div>
                    </div>
                    <div class="roster-card">
                        <div class="roster-avatar">👔</div>
                        <div class="roster-name">李总</div>
                        <div class="roster-role">副陪·商界老板·副驾驶</div>
                        <div class="roster-personality">能言善辩，擅长活跃气氛，总能找到话题接茬，能左右逢源…</div>
                    </div>
                    <div class="roster-card">
                        <div class="roster-avatar">👩</div>
                        <div class="roster-name">小赵</div>
                        <div class="roster-role">实诚晚辈·新手</div>
                        <div class="roster-personality">性格耿直但缺乏饭局经验，善于"酒桌踩雷"，为了替领导撑面子…</div>
                    </div>
                </div>
                """)
            
            with gr.Row():
                regenerate_btn = gr.Button("🔄 随机换人", elem_classes="secondary-btn")
                edit_btn = gr.Button("✏️ 手动编辑", elem_classes="secondary-btn")
            
            start_game_btn = gr.Button("🍺 入席开整", variant="primary", elem_classes="start-game-btn")
            back_to_scenes = gr.Button("← 返回场景选择", elem_classes="back-link-btn")

        # ========== Page 3: 对话页 ==========
        with gr.Column(visible=False, elem_classes="chat-page") as page_chat:
            with gr.Column(elem_classes="chat-page-inner"):
                # 视觉舞台区 (集成气场条)
                visual_stage = gr.HTML("", elem_id="visual-stage")
                
                with gr.Row():
                    # 侧边控制栏 (缩小)
                    with gr.Column(scale=1, min_width=120, elem_classes="side-controls"):
                        rescue_btn = gr.Button("🆘 救场", variant="secondary", elem_classes="summon-btn-styled")
                        end_btn = gr.Button("🏁 结束对决", elem_classes="end-btn")
                        back_btn = gr.Button("↩ 返回场景选择", elem_classes="back-btn", visible=False)
                        status_display = gr.Markdown("", elem_id="status-display")
                        
                        # 侧边气场条 (新位置)
                        aura_sidebar = gr.HTML(render_aura_sidebar(50, 50))

                    # 主对话区 (占满)
                    with gr.Column(scale=9, elem_classes="main-chat-col"):
                        # 判定反馈框 (顶部，可隐藏)
                        critique_display = gr.HTML(render_critique_box("正在分析局势..."), visible=False)
                        
                        # 聊天记录区（中间，可滚动）
                        chatbot = gr.Chatbot(
                            show_label=False,
                            elem_classes="chat-box-container",
                            avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=TalkArena"),
                            height=500
                        )
                                
                        # 总结区域（初始隐藏，结束时显示）
                        summary_display = gr.Markdown(visible=False, elem_classes="summary-box")
                        
                        # 语音输入浮动层（隐藏状态）
                        with gr.Column(visible=False, elem_classes="mic-container-floating") as mic_box:
                            mic = gr.Audio(
                                sources=["microphone", "upload"],
                                type="filepath",
                                label="🎙️ 语音输入",
                                container=False
                            )
                                
                        # 输入区（固定底部）
                        with gr.Row(elem_classes="input-row"):
                            mic_toggle = gr.Button("🎙️", scale=0, min_width=40, elem_classes="mic-toggle-btn")
                            txt = gr.Textbox(
                                show_label=False,
                                placeholder="输入消息...",
                                container=False,
                                scale=10
                            )
                            btn_send = gr.Button("发送", scale=0, min_width=60, elem_classes="send-btn")
                            
                    audio_player = gr.Audio(visible=False, autoplay=True)
        
        # ========== Page 4: 复盘报告页 ==========
        with gr.Column(visible=False, elem_classes="report-page") as page_report:
            report_html = gr.HTML("", elem_id="game-report")
            
            with gr.Row(elem_classes="report-buttons"):
                retry_btn = gr.Button("🔄 重新挑战", elem_classes="btn-dark")
                menu_btn = gr.Button("🏠 返回菜单", elem_classes="btn-light")
                share_btn = gr.Button("📤 分享成绩", elem_classes="btn-purple")
        
        # ========== 事件处理 ==========

        def on_select_scene(sid, name, desc):
            # 如果是山东饭局，跳转到配置页
            if sid == "shandong_dinner":
                return (
                    gr.update(visible=False),  # 隐藏场景选择页
                    gr.update(visible=True),   # 显示配置页
                    gr.update(visible=False),  # 隐藏对话页
                    sid  # 保存场景ID
                )
            
            # 其他场景直接开始
            sess, hist, _, ai_d, user_d = start_session(sid)
            user = get_current_user()
            
            from ui.handlers import get_orchestrator
            orch = get_orchestrator()
            scene_cfg = orch.scenarios.get(sid, {})
            theme_color = scene_cfg.get("theme_color", "#4A90E2")
            characters = scene_cfg.get("characters")
            
            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),
                sess,
                {"name": name, "sid": sid, "theme_color": theme_color, "characters": characters},
                hist,
                render_visual_stage(characters, None, user_d, ai_d),
                render_aura_sidebar(user_d, ai_d),
                gr.update(value=render_critique_box("开始对决"), visible=True),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False)
            )

        pending_scenario = gr.State("")
        
        for btn, sid, name, desc in scenario_buttons:
            if sid == "shandong_dinner":
                btn.click(
                    fn=lambda s=sid, n=name, d=desc: on_select_scene(s, n, d),
                    outputs=[page_select, page_config, page_chat, pending_scenario]
                )
            else:
                btn.click(
                    fn=lambda s=sid, n=name, d=desc: on_select_scene(s, n, d),
                    outputs=[page_select, page_config, page_chat, session_id, current_scene, chatbot, 
                             visual_stage, aura_sidebar, critique_display, summary_display, end_btn, back_btn]
                )
        
        # 配置页返回场景选择
        def back_from_config():
            return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
        
        back_to_scenes.click(
            fn=back_from_config,
            outputs=[page_select, page_config, page_chat]
        )
        
        # 配置页开始游戏
        def start_from_config(sid):
            sess, hist, _, ai_d, user_d = start_session(sid)
            from ui.handlers import get_orchestrator
            orch = get_orchestrator()
            scene_cfg = orch.scenarios.get(sid, {})
            theme_color = scene_cfg.get("theme_color", "#4A90E2")
            characters = scene_cfg.get("characters")
            
            return (
                gr.update(visible=False),
                gr.update(visible=True),
                sess,
                {"name": "山东人的饭桌", "sid": sid, "theme_color": theme_color, "characters": characters},
                hist,
                render_visual_stage(characters, None, user_d, ai_d),
                render_aura_sidebar(user_d, ai_d),
                gr.update(value=render_critique_box("开始对决"), visible=True),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False)
            )
        
        start_game_btn.click(
            fn=start_from_config,
            inputs=[pending_scenario],
            outputs=[page_config, page_chat, session_id, current_scene, chatbot,
                     visual_stage, aura_sidebar, critique_display, summary_display, end_btn, back_btn]
        )

        def toggle_mic(visible):
            return gr.update(visible=not visible)

        mic_toggle.click(fn=toggle_mic, inputs=[mic_box], outputs=[mic_box])

        def handle_rescue_ui(sess, scene, history):
            """救场按钮 - 生成高情商回复建议填入输入框"""
            if not sess:
                return (history, "❌ 请先开始对决", "", "", "", None, "")
            
            characters = scene.get("characters")
            chat_result, status, ai_d, user_d, audio, suggestion = handle_rescue(sess, history, "")
            
            return (
                chat_result,
                status,
                render_visual_stage(characters, None, user_d, ai_d),
                render_aura_sidebar(user_d, ai_d),
                render_critique_box("💡 已生成高情商回复建议"),
                audio,
                suggestion
            )

        rescue_btn.click(
            fn=handle_rescue_ui,
            inputs=[session_id, current_scene, chatbot],
            outputs=[chatbot, status_display, visual_stage, aura_sidebar, critique_display, audio_player, txt]
        )

        def on_end(sess, scene, history):
            """结束对决，生成复盘报告"""
            if not sess:
                yield (
                    gr.update(visible=False),  # 隐藏对话页
                    gr.update(visible=True),   # 显示报告页
                    "⚠️ 请先开始对决"  # 报告内容
                )
                return
                    
            from ui.handlers import get_orchestrator
            orch = get_orchestrator()
                    
            if sess not in orch.sessions:
                yield (
                    gr.update(visible=False),
                    gr.update(visible=True),
                    "⚠️ 对决已结束"
                )
                return
                    
            # 显示加载界面
            loading_messages = [
                "正在复盘饭局细节...",
                "正在请教饭局高人...",
                "正在为你的人生捏一把汗...",
                "正在回收全场酒瓶...",
                "正在生成饭局勋章..."
            ]
                    
            loading_html = f'''
            <div style="width: 100%; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; background: #2c313c; color: white;">
                <div style="width: 50px; height: 50px; border: 5px solid rgba(255,255,255,0.1); border-top: 5px solid #4a5dca; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px;"></div>
                <div id="loading-text" style="font-size: 18px;">{loading_messages[0]}</div>
                <style>
                    @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
                </style>
            </div>
            '''
                    
            yield (
                gr.update(visible=False),
                gr.update(visible=True),
                loading_html
            )
                    
            # 获取场景信息
            scene_name = scene.get("name", "山东人的饭桌")
            characters = scene.get("characters", [])
            npc_list = [{"name": c.get("name", "NPC"), "avatar": c.get("avatar", "👤")} for c in characters]
                    
            # 生成报告
            try:
                report_data = orch.generate_game_report(sess, scene_name, npc_list)
                        
                # 渲染HTML
                from ui.report import render_report_card
                report_html_content = render_report_card(
                    scene_name=report_data["scene_name"],
                    medal=report_data["medal"],
                    scores=report_data["scores"],
                    summary=report_data["summary"],
                    npc_os_list=report_data["npc_os_list"],
                    suggestion=report_data["suggestion"]
                )
                        
                yield (
                    gr.update(visible=False),
                    gr.update(visible=True),
                    report_html_content
                )
                        
            except Exception as e:
                import traceback
                error_html = f'''
                <div style="padding: 40px; text-align: center; color: #e74c3c;">
                    <h2>⚠️ 生成报告失败</h2>
                    <p>{str(e)}</p>
                    <pre style="text-align: left; background: #f5f5f5; padding: 10px; border-radius: 5px; overflow: auto;">{traceback.format_exc()}</pre>
                </div>
                '''
                yield (
                    gr.update(visible=False),
                    gr.update(visible=True),
                    error_html
                )
        
        end_btn.click(
            fn=on_end,
            inputs=[session_id, current_scene, chatbot],
            outputs=[page_chat, page_report, report_html]
        )

        def on_back():
            """返回场景选择"""
            return (
                gr.update(visible=True),   # 显示场景页
                gr.update(visible=False),  # 隐藏对话页
                "",                        # 清空session
                {"name": "", "sid": ""},   # 清空场景
                []                         # 清空聊天
            )

        back_btn.click(
            fn=on_back,
            outputs=[page_select, page_chat, session_id, current_scene, chatbot]
        )

        def handle_msg(sess, scene, text, history):
            if not sess:
                return history, "", "", "", None
            user = get_current_user()
            theme_color = scene.get("theme_color", "#4A90E2")
            characters = scene.get("characters")
            for chat, _, ai_dom, user_dom, audio in send_message(sess, text, history):
                # 尝试解析当前讲话者
                last_msg = chat[-1]["content"] if chat else ""
                last_title = chat[-1].get("metadata", {}).get("title", "")
                
                # 去除头像前缀
                speaker = last_title.split(' ')[-1] if ' ' in last_title else last_title
                
                # 获取最后一次判定的点评内容（如果有）
                judgment = "对局中"
                if "📊" in last_msg:
                    parts = last_msg.split("📊")
                    if len(parts) > 1:
                        judgment = parts[1].split("(")[0].strip()

                yield (
                    chat, "",
                    render_visual_stage(characters, speaker, user_dom, ai_dom),
                    render_aura_sidebar(user_dom, ai_dom),
                    render_critique_box(judgment),
                    audio
                )

        def handle_voice(sess, scene, audio_path, history):
            if not sess or not audio_path:
                return history, "", "", "", "", None
            user = get_current_user()
            theme_color = scene.get("theme_color", "#4A90E2")
            characters = scene.get("characters")
            for chat, _, ai_dom, user_dom, audio in process_voice_input(sess, audio_path, history):
                last_title = chat[-1].get("metadata", {}).get("title", "")
                speaker = last_title.split(' ')[-1] if ' ' in last_title else last_title
                
                last_msg = chat[-1]["content"]
                judgment = "对局中"
                if "📊" in last_msg:
                    parts = last_msg.split("📊")
                    if len(parts) > 1:
                        judgment = parts[1].split("(")[0].strip()

                yield (
                    chat, "",
                    render_visual_stage(characters, speaker, user_dom, ai_dom),
                    render_aura_sidebar(user_dom, ai_dom),
                    render_critique_box(judgment),
                    audio
                )

        txt.submit(
            fn=handle_msg,
            inputs=[session_id, current_scene, txt, chatbot],
            outputs=[chatbot, txt, visual_stage, aura_sidebar, critique_display, audio_player]
        )
        btn_send.click(
            fn=handle_msg,
            inputs=[session_id, current_scene, txt, chatbot],
            outputs=[chatbot, txt, visual_stage, aura_sidebar, critique_display, audio_player]
        )
        mic.change(
            fn=handle_voice,
            inputs=[session_id, current_scene, mic, chatbot],
            outputs=[chatbot, txt, visual_stage, aura_sidebar, critique_display, audio_player]
        )
        
        # ========== 报告页按钮事件 ==========
        def on_retry(scene):
            """重新挑战 - 重启当前场景"""
            sid = scene.get("sid", "")
            if not sid:
                return (
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(visible=False),
                    "",
                    {"name": "", "sid": ""},
                    []
                )
            
            # 重新开始游戏
            sess, hist, _, ai_d, user_d = start_session(sid)
            from ui.handlers import get_orchestrator
            orch = get_orchestrator()
            scene_cfg = orch.scenarios.get(sid, {})
            characters = scene_cfg.get("characters")
            
            return (
                gr.update(visible=False),  # 隐藏报告页
                gr.update(visible=True),   # 显示对话页
                gr.update(visible=False),  # 隐藏配置页
                sess,
                scene,
                hist,
                render_visual_stage(characters, None, user_d, ai_d),
                render_aura_sidebar(user_d, ai_d)
            )
        
        def on_back_to_menu():
            """返回菜单 - 返回配置页"""
            return (
                gr.update(visible=False),  # 隐藏报告页
                gr.update(visible=False),  # 隐藏对话页
                gr.update(visible=True),   # 显示配置页
                "",
                {"name": "", "sid": ""},
                []
            )
        
        def on_share():
            """分享成绩 - 生成分享图片"""
            # TODO: 实现截图分享功能
            return gr.update()
        
        retry_btn.click(
            fn=on_retry,
            inputs=[current_scene],
            outputs=[page_report, page_chat, page_config, session_id, current_scene, chatbot, visual_stage, aura_sidebar]
        )
        
        menu_btn.click(
            fn=on_back_to_menu,
            outputs=[page_report, page_chat, page_config, session_id, current_scene, chatbot]
        )
        
        share_btn.click(
            fn=on_share,
            outputs=[]
        )

    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="127.0.0.1", server_port=1234)
