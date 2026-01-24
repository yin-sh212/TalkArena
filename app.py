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
    handle_user_register
)
from ui.theme import CUSTOM_CSS
from ui.components import render_aura_dashboard, render_avatar_section
from ui.user import get_current_user, register_user

SCENARIOS = {
    "negotiation": {"name": "商务谈判", "desc": "与王总进行一场商务价格谈判"},
    "debate": {"name": "辩论赛", "desc": "与反方辩手进行一场激烈辩论"},
    "interview": {"name": "压力面试", "desc": "挑战刷人的HR总监压力面试"},
}


def create_ui():
    init_models()
    scenarios_data = get_scenarios()

    with gr.Blocks(title="TalkArena", css=CUSTOM_CSS) as demo:
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
        with gr.Row(visible=False, elem_classes="chat-page") as page_chat:
            with gr.Column(scale=0, min_width=260):
                gr.HTML('<div class="brand-title">TalkArena</div>')
                aura_display = gr.HTML(render_aura_dashboard(50, 50))
                
                # 语音输入放左侧
                mic = gr.Audio(
                    sources=["microphone", "upload"],
                    type="filepath",
                    label="🎙️ 语音输入"
                )
                
                end_btn = gr.Button("🏁 结束对决", elem_classes="end-btn")
                back_btn = gr.Button("↩ 返回场景选择", elem_classes="back-btn", visible=False)

            with gr.Column(scale=1):
                # 头像区
                avatar_display = gr.HTML(render_avatar_section("我", "对手", 50, 50))
                
                # 聊天框
                chatbot = gr.Chatbot(
                    show_label=False,
                    height=300,
                    elem_classes="chat-box-container"
                )
                
                # 总结区域（初始隐藏）
                summary_display = gr.Markdown(visible=False, elem_classes="summary-box")
                
                # 输入区
                with gr.Row(elem_classes="input-row"):
                    txt = gr.Textbox(
                        show_label=False,
                        placeholder="输入消息...",
                        container=False,
                        scale=10
                    )
                    btn_send = gr.Button("⬆", scale=0, min_width=36)
                
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
            return (
                gr.update(visible=False),
                gr.update(visible=True),
                sess,
                {"name": name, "sid": sid},
                hist,
                render_aura_dashboard(user_d, ai_d),
                render_avatar_section(user.name or "我", name, user_d, ai_d),
                gr.update(visible=False),  # 隐藏总结
                gr.update(visible=True),   # 显示结束按钮
                gr.update(visible=False)   # 隐藏返回按钮
            )

        for btn, sid, name, desc in scenario_buttons:
            btn.click(
                fn=lambda s=sid, n=name, d=desc: on_select_scene(s, n, d),
                outputs=[page_select, page_chat, session_id, current_scene, chatbot, 
                         aura_display, avatar_display, summary_display, end_btn, back_btn]
            )

        def on_end(sess, history):
            """结束对决，显示总结"""
            if not sess:
                return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
            
            from ui.handlers import get_orchestrator
            orch = get_orchestrator()
            
            if sess not in orch.sessions:
                return gr.update(value="对决已结束", visible=True), gr.update(visible=False), gr.update(visible=True)
            
            summary, _ = orch.end_session_with_summary(sess)
            summary_md = f"### 🏆 对决总结\n\n{summary}"
            
            return (
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
                return history, "", render_aura_dashboard(50, 50), render_avatar_section("我", "对手", 50, 50), None
            user = get_current_user()
            for chat, _, ai_d, user_d, audio in send_message(sess, text, history):
                yield (
                    chat, "",
                    render_aura_dashboard(user_d, ai_d),
                    render_avatar_section(user.name or "我", scene.get("name", "对手"), user_d, ai_d),
                    audio
                )

        def handle_voice(sess, scene, audio_path, history):
            if not sess or not audio_path:
                return history, "", render_aura_dashboard(50, 50), render_avatar_section("我", "对手", 50, 50), None
            user = get_current_user()
            for chat, _, ai_d, user_d, audio in process_voice_input(sess, audio_path, history):
                yield (
                    chat, "",
                    render_aura_dashboard(user_d, ai_d),
                    render_avatar_section(user.name or "我", scene.get("name", "对手"), user_d, ai_d),
                    audio
                )

        txt.submit(
            fn=handle_msg,
            inputs=[session_id, current_scene, txt, chatbot],
            outputs=[chatbot, txt, aura_display, avatar_display, audio_player]
        )
        btn_send.click(
            fn=handle_msg,
            inputs=[session_id, current_scene, txt, chatbot],
            outputs=[chatbot, txt, aura_display, avatar_display, audio_player]
        )
        mic.change(
            fn=handle_voice,
            inputs=[session_id, current_scene, mic, chatbot],
            outputs=[chatbot, txt, aura_display, avatar_display, audio_player]
        )

    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
