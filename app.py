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
        with gr.Row(visible=True, elem_classes="scene-select-page") as page_select:
            with gr.Column(scale=0, min_width=280):
                gr.HTML('<div class="brand-title">TalkArena</div>')
                gr.HTML('<div class="brand-subtitle">选择挑战场景</div>')

                scenario_buttons = []
                for display_name, sid in scenarios_data:
                    cfg = SCENARIOS.get(sid, {"name": display_name, "desc": "开始挑战！"})
                    btn = gr.Button(
                        value=f"📋 {cfg['name']}\n{cfg['desc']}",
                        elem_classes="scenario-card"
                    )
                    scenario_buttons.append((btn, sid, cfg["name"], cfg["desc"]))

                gr.HTML('<div class="footer-action">自定义场景 ?</div>')

            with gr.Column(scale=1):
                gr.Markdown("### 登录")
                name_input = gr.Textbox(label="姓名", placeholder="请输入姓名")
                email_input = gr.Textbox(label="邮箱", placeholder="可选")
                login_btn = gr.Button("保存", variant="primary")

        # ========== Page 2: 对话页 ==========
        with gr.Column(visible=False, elem_classes="chat-page") as page_chat:
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
                        height=400
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
        
        # ========== 事件处理 ==========
        def on_login(name, email):
            if name.strip():
                register_user(name.strip(), "", email.strip(), "")
            return gr.update(), gr.update()

        login_btn.click(fn=on_login, inputs=[name_input, email_input], outputs=[name_input, email_input])

        def on_select_scene(sid, name, desc):
            sess, hist, _, ai_d, user_d = start_session(sid)
            user = get_current_user()
            
            # 获取场景配置
            from ui.handlers import get_orchestrator
            orch = get_orchestrator()
            scene_cfg = orch.scenarios.get(sid, {})
            theme_color = scene_cfg.get("theme_color", "#4A90E2")
            characters = scene_cfg.get("characters")
            
            return (
                gr.update(visible=False),
                gr.update(visible=True),
                sess,
                {"name": name, "sid": sid, "theme_color": theme_color, "characters": characters},
                hist,
                render_visual_stage(characters, None, user_d, ai_d),
                render_aura_sidebar(user_d, ai_d),
                gr.update(value=render_critique_box("开始对决"), visible=True),
                gr.update(visible=False),  # 隐藏总结
                gr.update(visible=True),   # 显示结束按钮
                gr.update(visible=False)   # 隐藏返回按钮
            )

        for btn, sid, name, desc in scenario_buttons:
            btn.click(
                fn=lambda s=sid, n=name, d=desc: on_select_scene(s, n, d),
                outputs=[page_select, page_chat, session_id, current_scene, chatbot, 
                         visual_stage, aura_sidebar, critique_display, summary_display, end_btn, back_btn]
            )

        def toggle_mic(visible):
            return gr.update(visible=not visible)

        mic_toggle.click(fn=toggle_mic, inputs=[mic_box], outputs=[mic_box])

        def handle_rescue_ui(sess, scene, history):
            if not sess:
                yield (history, "❌ 请先开始对决", "", "", "", None)
                return
            theme_color = scene.get("theme_color", "#4A90E2")
            characters = scene.get("characters")
            for res in handle_rescue(sess, history):
                if len(res) != 5:
                    print(f"[ERROR] handle_rescue yielded {len(res)} values instead of 5: {res}")
                chat, status, ai_d, user_d, audio = res
                
                # 极其重要的调试日志
                print(f"[DEBUG] handle_rescue_ui: ai_d={type(ai_d)}:{ai_d}, user_d={type(user_d)}:{user_d}")
                
                yield (
                    chat, status,
                    render_visual_stage(characters, "救场大师", user_d, ai_d),
                    render_aura_sidebar(user_d, ai_d),
                    render_critique_box("大师助阵中..."),
                    audio
                )

        rescue_btn.click(
            fn=handle_rescue_ui,
            inputs=[session_id, current_scene, chatbot],
            outputs=[chatbot, status_display, visual_stage, aura_sidebar, critique_display, audio_player]
        )

        def on_end(sess, history):
            """结束对决，显示总结"""
            print(f"[DEBUG] on_end called, sess={sess}")
            
            if not sess:
                print("[DEBUG] No session")
                return gr.update(value="请先开始对决", visible=True), gr.update(visible=False), gr.update(visible=True)
            
            from ui.handlers import get_orchestrator
            orch = get_orchestrator()
            
            if sess not in orch.sessions:
                print(f"[DEBUG] Session {sess} not found")
                return gr.update(value="对决已结束", visible=True), gr.update(visible=False), gr.update(visible=True)
            
            # 立即显示"正在生成总结"
            yield (
                gr.update(value="⏳ **正在生成对决总结...**\n\n_请稍候，正在分析对话记录..._", visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )
            
            print(f"[DEBUG] Generating summary for {sess}")
            summary, _ = orch.end_session_with_summary(sess)
            summary_md = f"### 🏆 对决总结\n\n{summary}"
            
            yield (
                gr.update(value=summary_md, visible=True),
                gr.update(visible=False),
                gr.update(visible=True)
            )

        end_btn.click(
            fn=on_end,
            inputs=[session_id, chatbot],
            outputs=[summary_display, end_btn, back_btn]
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

    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True, css=CUSTOM_CSS)
