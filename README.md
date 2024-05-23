# 🤖 Prompt Teacher 📝✨

<img src="thumbnail.png" alt="Screenshot of the Prompt Teacher"/>

## Quickstart 🚀

### 👉 Click here to try out the app directly without any setup:
[**Prompt Teacher @ Huggingface Spaces**](https://pwenker-prompt-teacher.hf.space/)

### 🔍 Inspect code at:
- **GitHub:** [pwenker/prompt_teacher](https://github.com/pwenker/prompt_teacher)
- **Hugging Face Spaces:** [pwenker/prompt_teacher](https://huggingface.co/spaces/pwenker/prompt_teacher)

## Local Deployment 🏠

### Prerequisites 📋

#### Rye 🌾
[Install `Rye`](https://rye-up.com/guide/installation/#installing-rye)
> Rye is a comprehensive tool designed for Python developers. It simplifies your workflow by managing Python installations and dependencies. Simply install Rye, and it takes care of the rest.


### Secrets Management  🔑

- Create an environment file: `.env` in the `prompt_teacher` folder and add the following variables:

```
OPENAI_API_KEY=... # Token for the OpenAI API
ANTHROPIC_API_KEY=... # Token for the Anthropic API
```

### Set-Up 🛠️

Clone the repository, e.g. with:
```
git clone https://github.com/pwenker/prompt_teacher.git
```
Navigate to the directory:
```
cd prompt_teacher
```
And execute:
```
rye sync
```
This creates a virtual environment in `.venv` and synchronizes the repo.

For more details, visit: [Basics - Rye](https://rye-up.com/guide/basics/)

### Start the App 🌟

> [!NOTE]  
> If you choose to install `prompt_teacher` without `rye` just omit `rye run` for the following commands.

Launch the app using:
```
rye run python src/prompt_teacher/app.py
```

Finally, open your browser and visit [http://localhost:7860](http://localhost:7860/) to start prompting!
