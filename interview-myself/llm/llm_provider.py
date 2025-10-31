import os

from langchain_openai import ChatOpenAI
from pydantic import SecretStr


def get_tongyi_langchain_llm(model: str = None):
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    base_model_name = os.getenv("BASE_MODEL_NAME")
    llm = ChatOpenAI(
        temperature=0.8,
        model=model if model else base_model_name,
        api_key=SecretStr(api_key),
        base_url=base_url
    )
    return llm
