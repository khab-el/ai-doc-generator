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

    logger.info(f"Initialized ProjectAnalyzer:")
    logger.info(f"- Project directory: {project_dir}")
    logger.info(f"- Initial summaries: {output_dir}/summaries.txt")
    logger.info(f"- Findings JSON: {output_dir}/findings.json")

    logging.info(f"Starting analysis of project: {project_dir}")
    logger.info("Analyzing root directory...")
    structure = "\n".join(p.name for p in project_dir.iterdir())
    extensions = scanner.extension_stats()
    root_summary = analyzer.analyze_root(structure, extensions)
    logger.info("Root analysis complete")

    findings.update_root(root_summary)
    summaries.append("Project Overview", root_summary)

    for directory in scanner.iter_directories():
        file_summaries = []
        for file in scanner.iter_files(directory):
            logger.info(f"Analyzing file: {file}")
            summary = analyzer.analyze_file(file)
            if summary:
                findings.update_file(file, summary)
                summaries.append(f"File: {file}", summary)
                file_summaries.append(summary)
            logger.info(f"Completed analysis of file: {file}")

        if file_summaries:
            logger.info(f"Analyzing directory: {directory}")
            dir_summary = analyzer.analyze_directory(directory, "\n".join(file_summaries))
            findings.update_directory(directory, dir_summary)
            summaries.append(f"Directory: {directory}", dir_summary)
            logger.info(f"Completed analysis of directory: {directory}")

    logger.info("Project analysis complete")

    logger.info("Generating developer guide...")
    guide = GuideGenerator(llm, prompts)
    guide_md = guide.generate(open(summaries.path).read(), findings.load())

    with open(output_dir / "GUIDE.md", "w") as f:
        f.write(guide_md)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
