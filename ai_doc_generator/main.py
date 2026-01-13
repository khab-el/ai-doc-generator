from pathlib import Path
import logging

from ai_doc_generator.analysis.analyzer import AnalyzerService
from ai_doc_generator.config import settings
from ai_doc_generator.fs.scanner import FileSystemScanner
from ai_doc_generator.guide.generator import GuideGenerator
from ai_doc_generator.llm.openai_local import OpenAILocalClient
from ai_doc_generator.prompts.builder import PromptBuilder
from ai_doc_generator.storage.findings import FindingsRepository
from ai_doc_generator.storage.summaries import SummaryWriter

logger = logging.getLogger(__file__)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    project_dir = Path(settings.GUIDE_TARGET_PROJECT_DIRECTORY)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    llm = OpenAILocalClient()
    prompts = PromptBuilder()
    analyzer = AnalyzerService(llm, prompts)

    scanner = FileSystemScanner(project_dir)
    findings = FindingsRepository(output_dir / "findings.json")
    summaries = SummaryWriter(output_dir / "summaries.txt")

    logger.info("Initialized ProjectAnalyzer:")
    logger.info(f"- Project directory: {project_dir}")
    logger.info(f"- Initial summaries: {output_dir}/summaries.txt")
    logger.info(f"- Findings JSON: {output_dir}/findings.json")

    logger.info(f"Starting analysis of project: {project_dir}")
    analyzer.analyze_project(
        project_dir=project_dir,
        findings=findings,
        summaries=summaries,
        scanner=scanner,
    )
    logger.info("Project analysis complete")

    logger.info("Generating developer guide...")
    guide = GuideGenerator(llm, prompts)
    guide_md = guide.generate(open(summaries.path).read(), findings.load())

    with open(output_dir / "GUIDE.md", "w") as f:
        f.write(guide_md)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
