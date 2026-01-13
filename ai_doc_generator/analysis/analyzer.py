from pathlib import Path

from ai_doc_generator.fs.reader import ContentReader
from ai_doc_generator.llm.base import LLMClient
from ai_doc_generator.prompts.builder import PromptBuilder


class AnalyzerService:
    def __init__(self, llm: LLMClient, prompts: PromptBuilder) -> None:
        self.llm = llm
        self.prompts = prompts
        self.reader = ContentReader()

    def analyze_root(self, structure: str, extensions: dict) -> str:
        s, u = self.prompts.root(structure, extensions)
        return self.llm.chat(system_prompt=s, user_prompt=u, max_tokens=100, temperature=0)

    def analyze_file(self, path: Path) -> str | None:
        content, desc = self.reader.read(path)
        if desc == "binary":
            return None
        s, u = self.prompts.file(path, content, desc)
        return self.llm.chat(system_prompt=s, user_prompt=u, max_tokens=100, temperature=0)

    def analyze_directory(self, path: Path, summaries: str) -> str:
        s, u = self.prompts.directory(path, summaries)
        return self.llm.chat(system_prompt=s, user_prompt=u, max_tokens=100, temperature=0)
