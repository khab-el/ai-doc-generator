from pathlib import Path
import logging

from ai_doc_generator.fs.reader import ContentReader
from ai_doc_generator.llm.base import LLMClient
from ai_doc_generator.prompts.builder import PromptBuilder
from ai_doc_generator.storage.findings import FindingsRepository
from ai_doc_generator.storage.summaries import SummaryWriter
from ai_doc_generator.fs.scanner import FileSystemScanner

logger = logging.getLogger(__file__)


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
        if desc == "binary" or desc == "empty":
            return None
        s, u = self.prompts.file(path, content, desc)
        return self.llm.chat(system_prompt=s, user_prompt=u, max_tokens=100, temperature=0)

    def _analyze_directory(self, path: Path, summaries: str) -> str:
        s, u = self.prompts.directory(path, summaries)
        return self.llm.chat(system_prompt=s, user_prompt=u, max_tokens=100, temperature=0)

    def analyze_directory(
        self,
        directory: Path,
        findings: FindingsRepository,
        summaries: SummaryWriter,
        scanner: FileSystemScanner,
    ) -> None:
        file_summaries = []
        for file in scanner.iter_files(directory):
            logger.info(f"Analyzing file: {file}")
            summary = self.analyze_file(file)
            if summary:
                findings.update_file(file, summary)
                summaries.append(f"File: {file}", summary)
                file_summaries.append(summary)
            logger.info(f"Completed analysis of file: {file}")

        if file_summaries:
            logger.info(f"Analyzing directory: {directory}")
            dir_summary = self._analyze_directory(directory, "\n".join(file_summaries))
            findings.update_directory(directory, dir_summary)
            summaries.append(f"Directory: {directory}", dir_summary)
            logger.info(f"Completed analysis of directory: {directory}")

    def analyze_project(
        self,
        project_dir: Path,
        findings: FindingsRepository,
        summaries: SummaryWriter,
        scanner: FileSystemScanner,
    ) -> None:
        logger.info("Analyzing root directory...")
        structure = "\n".join(p.name for p in project_dir.iterdir())
        extensions = scanner.extension_stats()
        root_summary = self.analyze_root(structure, extensions)
        logger.info("Root analysis complete")

        findings.update_root(root_summary)
        summaries.append("Project Overview", root_summary)
        
        self.analyze_directory(
            project_dir,
            findings=findings,
            summaries=summaries,
            scanner=scanner,
        )

        for directory in scanner.iter_directories():
            self.analyze_directory(
                directory,
                findings=findings,
                summaries=summaries,
                scanner=scanner,
            )
