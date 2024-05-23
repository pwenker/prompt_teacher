import yaml
from pydantic import BaseModel, ValidationError


class Metaprompt(BaseModel):
    explanation: str
    example_prompt: str
    example_prompt_explanation: str
    name: str
    template: str

    def __str__(self):
        return f"✨**{self.name}**\n\n📝 *{self.explanation}*\n\n📚 **Example Prompt:** {self.example_prompt}\n\n📖 **Example Prompt Explanation:** {self.example_prompt_explanation}"


class MetapromptLibrary(BaseModel):
    Metaprompts: list[Metaprompt]


def read_and_validate(file_path: str = "metaprompts.yml"):
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            validated_data = MetapromptLibrary(**data)
            return validated_data
    except FileNotFoundError:
        return "Error: The file was not found."
    except yaml.YAMLError as e:
        return f"Error parsing YAML: {e}"
    except ValidationError as e:
        return f"Validation error: {e}"


metaprompts = read_and_validate().Metaprompts
metaprompts_dict = {mp.name: mp for mp in metaprompts}

if __name__ == "__main__":
    file_path = "metaprompts.yml"  # Specify the path to your YAML file
    result = read_and_validate(file_path)
    if isinstance(result, MetapromptLibrary):
        print("Data validated successfully:", result)
    else:
        print(result)
