from ai_doc_generator.llm.base import LLMClient
from ai_doc_generator.prompts.builder import PromptBuilder


class GuideGenerator:
    def __init__(self, llm: LLMClient, prompts: PromptBuilder) -> None:
        self.llm = llm
        self.prompts = prompts

    def generate(self, summaries: str, findings: dict) -> str:
        s, u = self.prompts.guide(summaries, findings)
        return self.llm.chat(system_prompt=s, user_prompt=u, max_tokens=4000, temperature=0)
