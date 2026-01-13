import typing as t


class PromptBuilder:
    def root(self, structure: str, extensions: dict[str, t.Any]) -> tuple[str, str]:
        return (
            "You are an AI assistant that analyzes code directories.",
            f"Analyze this project: Structure:\n{structure}\nExtensions:\n{extensions}"
        )

    def file(self, path: str, content: str, desc: str) -> tuple[str, str]:
        return (
            "You are an AI assistant that analyzes source code files.",
            f"""Analyze this file: {path} ({desc})\n{content}. provide:
            1. Overall purpose of the file
            2. Key fields/variables and their purposes (not all, just the most important ones)
            3. Main function definitions with inputs, outputs, and purposes
            4. Any important structs/classes and their significance
            5. How this file fits into the project"""
        )

    def directory(self, path: str, summaries: str) -> tuple[str, str]:
        return (
            "You are an AI assistant that analyzes code directories.",
            f"Analyze this directory: {path}\n{summaries}. Provide a summary of this directory's purpose and how its contents work together."
        )

    def guide(self, summaries: str, findings: dict) -> tuple[str, str]:
        return (
            "You are an expert technical writer who creates clear, well-organized developer guides.",
            f"""
            Based on the following project analysis data, create a comprehensive developer guide in markdown format.
            Initial Summaries:
            {summaries}
            Detailed Findings:
            {findings}
            
            Create a developer guide."""
        )
