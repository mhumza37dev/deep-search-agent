from typing import List, Dict
from langchain_openai import AzureChatOpenAI
from src.agent.llm_services.llm_strategy import LLMStrategy
from src.config.app_config import config


class GrokStrategy(LLMStrategy):
    """Strategy for Grok model operations"""

    def __init__(self):
        self.client = AzureChatOpenAI(
            azure_endpoint=config.AZURE_GROK_ENDPOINT,
            api_key=config.AZURE_GROK_API_KEY,
            deployment_name=config.AZURE_GROK_DEPLOYMENT,
            model_name=config.AZURE_GROK_MODEL,
            api_version=config.AZURE_GROK_API_VERSION,
            temperature=0.1,
        )

    def invoke(self, messages: List[Dict]) -> str:
        response = self.client.invoke(messages)
        return response.content

    def stream_invoke(self, messages: List[Dict]):
        response_stream = self.client.stream(messages)
        for chunk in response_stream:
            yield chunk.content
