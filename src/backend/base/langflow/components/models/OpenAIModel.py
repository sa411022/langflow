from typing import Optional

from langchain_openai import ChatOpenAI

from langflow.base.models.model import LCModelComponent
from langflow.field_typing import NestedDict, Text


class OpenAIModelComponent(LCModelComponent):
    display_name = "OpenAI"
    description = "Generates text using OpenAI LLMs."
    icon = "OpenAI"

    field_order = [
        "max_tokens",
        "model_kwargs",
        "model_name",
        "openai_api_base",
        "openai_api_key",
        "temperature",
        "input_value",
        "system_message",
        "stream",
    ]

    def build_config(self):
        return {
            "input_value": {"display_name": "Input"},
            "max_tokens": {
                "display_name": "Max Tokens",
                "advanced": True,
            },
            "model_kwargs": {
                "display_name": "Model Kwargs",
                "advanced": True,
            },
            "model_name": {
                "display_name": "Model Name",
                "advanced": False,
                "options": [
                    "gpt-4-turbo-preview",
                    "gpt-3.5-turbo",
                    "gpt-4-0125-preview",
                    "gpt-4-1106-preview",
                    "gpt-4-vision-preview",
                    "gpt-3.5-turbo-0125",
                    "gpt-3.5-turbo-1106",
                ],
                "value": "gpt-4-turbo-preview",
            },
            "openai_api_base": {
                "display_name": "OpenAI API Base",
                "advanced": True,
                "info": (
                    "The base URL of the OpenAI API. Defaults to https://api.openai.com/v1.\n\n"
                    "You can change this to use other APIs like JinaChat, LocalAI and Prem."
                ),
            },
            "openai_api_key": {
                "display_name": "OpenAI API Key",
                "info": "The OpenAI API Key to use for the OpenAI model.",
                "advanced": False,
                "password": True,
            },
            "temperature": {
                "display_name": "Temperature",
                "advanced": False,
                "value": 0.1,
            },
            "stream": {
                "display_name": "Stream",
                "info": "Stream the response from the model.",
                "advanced": True,
            },
            "system_message": {
                "display_name": "System Message",
                "info": "System message to pass to the model.",
                "advanced": True,
            },
        }

    def build(
        self,
        input_value: Text,
        openai_api_key: str,
        temperature: float,
        model_name: str,
        max_tokens: Optional[int] = 256,
        model_kwargs: NestedDict = {},
        openai_api_base: Optional[str] = None,
        stream: bool = False,
        system_message: Optional[str] = None,
    ) -> Text:
        if not openai_api_base:
            openai_api_base = "https://api.openai.com/v1"
        output = ChatOpenAI(
            max_tokens=max_tokens,
            model_kwargs=model_kwargs,
            model=model_name,
            base_url=openai_api_base,
            api_key=openai_api_key,
            temperature=temperature,
        )

        return self.get_chat_result(output, stream, input_value, system_message)
