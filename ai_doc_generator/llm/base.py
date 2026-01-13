class LLMClient:
    def chat(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        raise NotImplementedError
