import time
from typing import Any, Generator, Tuple

import gradio as gr
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import ValidationError
from langchain_openai import ChatOpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict

from prompt_teacher.messages import system_message
from prompt_teacher.metaprompts import metaprompts_dict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    openai_api_key: str = ""
    anthropic_api_key: str = ""


settings = Settings()


def get_llm(
    model_name: str = "gpt-4-turbo",
    api_key: str = settings.openai_api_key,
    structured_output=None,
):
    if model_name in ["gpt-4-turbo", "gpt-4o"]:
        llm = ChatOpenAI(
            model=model_name,
            api_key=settings.openai_api_key if not api_key else api_key,
        )
    elif model_name in ["claude-3-opus-20240229"]:
        llm = ChatAnthropic(
            model=model_name,
            api_key=settings.anthropic_api_key if not api_key else api_key,
        )
    else:
        raise ValueError(f"Model {model_name} not supported")
    if structured_output:
        llm = llm.with_structured_output(structured_output)
    return llm


def explain_metaprompt(explanation_history, metaprompt):
    explanation_history += [
        [f"❓How does **{metaprompt.capitalize()}** improve my prompt? 💡🚀", ""]
    ]
    answer = f"""{metaprompts_dict[metaprompt]}"""

    for character in answer:
        explanation_history[-1][1] += character
        time.sleep(0.001)
        yield explanation_history


def update_widgets(metaprompt, feedback):
    button_variant = "primary" if metaprompt else "secondary"
    feedback_visibility = True if metaprompt == "Apply feedback" else False
    return [
        gr.Button(variant=button_variant),
        gr.Textbox(
            visible=feedback_visibility, value=feedback if feedback_visibility else ""
        ),
    ]


def explain_improvement(
    model_name, api_key, prompt, metaprompt, improved_prompt, prompt_teacher
):
    llm = get_llm(model_name, api_key)
    prompt_template = """The following prompt: 
    ---
    {prompt} 
    ---
    was improved using the metaprompt:
    ---
    {metaprompt}
    ---
    As a result, the following improved version was created:
    ---
    {improved_prompt}
    ---
    Concisely explain the improvement.
    """

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", prompt_template),
        ]
    )
    llm = get_llm(model_name, api_key)
    parser = StrOutputParser()
    llm_chain = prompt_template | llm | parser

    prompt_teacher += [
        [
            "❓Can you please **explain** the **improved prompt**? 📝✨",
            "**Explanation**:\n\n",
        ]
    ]
    for response in llm_chain.stream(
        {"prompt": prompt, "metaprompt": metaprompt, "improved_prompt": improved_prompt}
    ):
        prompt_teacher[-1][1] += response
        yield prompt_teacher


def improve_prompt(
    model_name: str,
    api_key: str,
    prompt: str,
    metaprompt: str,
    feedback: str | None,
    explanation_history,
) -> Generator[Tuple[str, str], Any, Any]:
    metaprompt_template = metaprompts_dict[metaprompt].template

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", metaprompt_template),
        ]
    )
    parser = StrOutputParser()
    llm = get_llm(model_name, api_key)
    llm_chain = prompt_template | llm | parser

    explanation_history += [
        [
            f"""
            **📝 Please Improve the following Prompt:**
            ```
            {prompt}
            ```
            """,
            "**Improved Prompt**:\n\n",
        ]
    ]

    improved_prompt = ""

    input = {"prompt": prompt, "feedback": feedback} if feedback else {"prompt": prompt}

    for response in llm_chain.stream(input):
        explanation_history[-1][1] += response
        improved_prompt += response
        yield improved_prompt, explanation_history


def robustly_improve_prompt(*args, **kwargs):
    history = args[5]
    user_txt = "Oh no, there is an error!💥 What should I do?"
    try:
        yield from improve_prompt(*args, **kwargs)
    except ValidationError as e:
        error_msg = "\n".join([err["msg"] for err in e.errors()])
        error_msg += (
            "\n\nPlease paste your API key into the textbox on the right side :)"
        )
        gr.Warning(error_msg)
        history += [[user_txt, error_msg]]
        yield "", history
    except Exception as e:
        msg = "\n\nPlease check if you inserted a correct API key on the right side :)"
        try:
            error_msg = e.body["message"]
            error_msg += msg
            history += [[user_txt, error_msg]]
            gr.Warning(error_msg)
            yield "", history
        except Exception as ee:
            error_msg = str(e) + msg
            history += [[user_txt, error_msg]]
            gr.Warning(error_msg)
            yield "", history
