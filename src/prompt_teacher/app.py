import gradio as gr

from prompt_teacher.callbacks import (explain_improvement, explain_metaprompt,
                                      robustly_improve_prompt, update_widgets)
from prompt_teacher.messages import *
from prompt_teacher.metaprompts import metaprompts

with gr.Blocks(title="Prompt Teacher", theme=gr.themes.Soft()) as gradio_app:
    gr.Markdown("### 🤖 Prompt Teacher 📝✨")
    with gr.Accordion("ℹ️ Info: Code 📜 and Documentation 📚", open=False):
        gr.Markdown(
            "Can be found at: [Github: pwenker/prompt_teacher](https://github.com/pwenker/prompt_teacher) 📄✨"
        )
    with gr.Row():
        with gr.Column(scale=2):
            prompt_teacher = gr.Chatbot(
                height=580,
                label="Prompt Teacher",
                show_copy_button=True,
                value=[[inital_usr_text, initial_bot_text]],
                avatar_images=("thinking.svg", "robot.svg"),
            )
            prompt = gr.Textbox(
                label="Prompt",
                interactive=True,
                placeholder="Type in your prompt",
                value="How to write a good prompt?",
                show_copy_button=True,
            )
            with gr.Row():
                explain_btn = gr.Button(
                    "Explain improvement 💡",
                    variant="primary",
                    visible=False,
                )
                replace_btn = gr.Button(
                    "Accept improvement 👍",
                    variant="primary",
                    visible=False,
                )
            with gr.Row():
                improve_btn = gr.Button("✨Improve prompt", variant="primary")
        with gr.Column(scale=1):
            model_name = gr.Dropdown(
                label="Large Language Model",
                info="Select Large Language Model",
                choices=[
                    ("gpt-4-turbo", "gpt-4-turbo"),
                    ("claude-3-opus", "claude-3-opus-20240229"),
                ],
                value="gpt-4-turbo",
            )
            api_key = gr.Textbox(
                placeholder="Paste in your API key (sk-...)",
                label="OpenAI/Anthropic API Key",
                info="Paste in your API key",
                lines=1,
                type="password",
            )
            metaprompt = gr.Radio(
                label="Improvements",
                info="Select how the prompt should be improved",
                value="Apply prompt engineering best practices",
                choices=[mp.name.replace("_", " ").capitalize() for mp in metaprompts],
            )
            feedback = gr.Textbox(
                label="Feedback",
                info="Write your own feedback to be used to improve the prompt",
                visible=False,
            )
            audience = gr.Textbox(
                label="Audience",
                info="Select the audience for the prompt",
                visible=False,
            )

    improved_prompt = gr.Textbox(label="Improved Prompt", visible=False)
    examples = gr.Examples(
        examples=[[mp.name, mp.example_prompt] for mp in metaprompts],
        examples_per_page=100,
        inputs=[metaprompt, prompt],
    )

    metaprompt.change(
        fn=update_widgets,
        inputs=[metaprompt],
        outputs=[improve_btn, feedback, audience],
    ).success(
        lambda: [gr.Button(visible=False), gr.Button(visible=False)],
        None,
        [replace_btn, explain_btn],
    ).success(
        fn=explain_metaprompt,
        inputs=[prompt_teacher, metaprompt],
        outputs=[prompt_teacher],
    )
    improve_btn.click(
        fn=robustly_improve_prompt,
        inputs=[
            model_name,
            api_key,
            prompt,
            metaprompt,
            feedback,
            audience,
            prompt_teacher,
        ],
        outputs=[improved_prompt, prompt_teacher],
    ).success(
        lambda: [gr.Button(visible=True), gr.Button(visible=True)],
        None,
        [replace_btn, explain_btn],
    )

    explain_btn.click(lambda: gr.Button(visible=False), None, explain_btn).success(
        explain_improvement,
        [
            model_name,
            api_key,
            prompt,
            metaprompt,
            improved_prompt,
            prompt_teacher,
        ],
        prompt_teacher,
    )

    replace_btn.click(lambda x: x, improved_prompt, prompt).success(
        lambda: [gr.Button(visible=False), gr.Button(visible=False)],
        None,
        [replace_btn, explain_btn],
    )

if __name__ == "__main__":
    gradio_app.launch(favicon_path="robot.svg")
