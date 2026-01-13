
from openai import OpenAI
from ai_doc_generator.config import settings
from ai_doc_generator.llm.base import LLMClient


class OpenAILocalClient(LLMClient):
    def __init__(self) -> None:
        self.client = OpenAI(
            base_url=settings.LOCAL_LLM_BASE_URL,
            api_key=settings.LOCAL_LLM_API_KEY,
        )
        self.model = settings.LOCAL_LLM_MODEL

    def chat(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content
