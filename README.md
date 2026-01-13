# AI Documentation Generator Developer Guide

This guide provides comprehensive information for developers working with the AI Documentation Generator, a Python-based tool that automatically analyzes codebases and generates comprehensive developer documentation using AI capabilities.

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Installation & Setup](#installation--setup)
4. [Core Components](#core-components)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Extending the System](#extending-the-system)
8. [Development Workflow](#development-workflow)

## Overview

The AI Documentation Generator is a Python-based tool designed to automatically analyze software projects and generate comprehensive developer documentation. It leverages AI capabilities, particularly OpenAI APIs, to understand codebases and produce meaningful documentation.

Key features:
- Automated codebase analysis
- AI-powered documentation generation
- Modular architecture for extensibility
- Support for local LLM integration
- Comprehensive file exclusion mechanisms

## Project Structure

```
ai_doc_generator/
├── __init__.py
├── config.py              # Configuration management
├── main.py                # Main entry point
├── guide/
│   └── generator.py       # Documentation guide generation
├── llm/
│   ├── __init__.py
│   ├── base.py            # Base LLM client interface
│   └── openai_local.py    # Local OpenAI-compatible LLM client
├── analysis/
│   └── analyzer.py        # Core analysis engine
├── storage/
│   ├── findings.py        # Findings persistence
│   └── summaries.py       # Summary storage
├── prompts/
│   └── builder.py         # Prompt generation
└── fs/
    ├── scanner.py         # Filesystem scanning
    └── reader.py          # Content reading utilities
```

## Installation & Setup

### Prerequisites
- Python 3.10+
- uv package manager (recommended)

### Installation Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd ai_doc_generator
```

2. **Install dependencies:**
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

3. **Set up environment variables:**
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_api_key_here
LOCAL_LLM_ENDPOINT=http://localhost:11434/v1
```

## Core Components

### 1. Configuration (`config.py`)
Manages application settings using Pydantic's BaseSettings:
```python
class Settings(BaseSettings):
    EXCLUSION_LIST: List[str] = [
        ".git",
        "__pycache__",
        "*.pyc",
        "venv",
        "node_modules"
    ]
    # ... other settings
```

### 2. Main Entry Point (`main.py`)
Coordinates the entire documentation generation workflow:
```python
def main(project_dir: str):
    # Initialize components
    # Scan filesystem
    # Analyze files
    # Generate documentation
    pass
```

### 3. Analysis Engine (`analysis/analyzer.py`)
The core component that orchestrates the analysis process:
- Scans file system recursively
- Reads file contents intelligently
- Generates summaries using LLM
- Stores findings in structured format

### 4. LLM Integration (`llm/`)
Provides standardized interfaces for different language model providers:
- `base.py`: Abstract base class for LLM clients
- `openai_local.py`: Client for local OpenAI-compatible models

### 5. Storage Layer (`storage/`)
Handles persistence of analysis results:
- `findings.py`: Structured data storage for analysis findings
- `summaries.py`: Text summary storage

### 6. File System Utilities (`fs/`)
Provides efficient filesystem operations:
- `scanner.py`: Smart filesystem traversal with exclusion rules
- `reader.py`: Safe file content reading with error handling

### 7. Prompt Generation (`prompts/builder.py`)
Creates AI prompts for different analysis scenarios:
```python
class PromptBuilder:
    def project_summary(self) -> tuple[str, str]:
        # Returns system and user prompts for project analysis
        pass
    
    def file_analysis(self) -> tuple[str, str]:
        # Returns prompts for individual file analysis
        pass
```

## Configuration

### Environment Variables
The application reads configuration from environment variables and `.env` files:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | None |
| `LOCAL_LLM_ENDPOINT` | URL for local LLM service | None |
| `PROJECT_DIR` | Target project directory | Current directory |

### Exclusion List
Configurable list of paths/files to exclude from analysis:
```python
EXCLUSION_LIST = [
    ".git",
    "__pycache__",
    "*.pyc",
    "venv",
    "node_modules",
    "dist",
    "build"
]
```

## Usage

### Command Line Interface
```bash
# Generate documentation for current directory
python -m ai_doc_generator

# Generate documentation for specific project
python -m ai_doc_generator /path/to/project

# Generate documentation with custom settings
export OPENAI_API_KEY="your-key-here"
python -m ai_doc_generator /path/to/project
```

### Programmatic Usage
```python
from ai_doc_generator.main import main

# Generate documentation for a specific project
main("/path/to/your/project")

# With custom configuration
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"
main("/path/to/your/project")
```

## Extending the System

### Adding New LLM Providers
1. Create a new class inheriting from `LLMClient` in `llm/`
2. Implement required methods:
```python
class NewLLMClient(LLMClient):
    def generate_response(self, messages: List[Dict]) -> str:
        # Implementation for new provider
        pass
```

### Custom Analysis Types
Extend the `AnalyzerService` in `analysis/analyzer.py` to add new analysis capabilities:
```python
class ExtendedAnalyzer(AnalyzerService):
    def analyze_custom_metrics(self, project_path: Path) -> Dict:
        # Custom analysis logic
        pass
```

### New Storage Backends
Implement new storage classes following the existing patterns in `storage/`:
```python
class CustomStorage:
    def save_findings(self, data: Dict) -> None:
        # Custom storage implementation
        pass
```

## Development Workflow

### Setting Up Development Environment
1. Install development dependencies:
```bash
uv sync --dev
```

2. Run tests:
```bash
uv run pytest
```

3. Format code:
```bash
uv run black .
uv run ruff check --fix
```

### Contributing Guidelines
1. Follow PEP 8 style guidelines
2. Write comprehensive docstrings
3. Include unit tests for new functionality
4. Update documentation when making changes
5. Ensure backward compatibility

### Testing Strategy
The project uses pytest for testing:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_analyzer.py

# Run with coverage
pytest --cov=ai_doc_generator
```

## Troubleshooting

### Common Issues

**1. Missing Dependencies**
```bash
# Reinstall dependencies
uv sync
```

**2. LLM Connection Errors**
- Verify API keys are set correctly
- Check local LLM service is running if using local models
- Ensure network connectivity for cloud services

**3. File Reading Issues**
- Check file permissions
- Verify exclusions aren't blocking important files
- Review file size limits in `fs/reader.py`

### Debugging Tips
- Use verbose logging to trace execution flow
- Check output directory for intermediate results
- Validate configuration settings before running analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and feature requests, please submit them through the project's issue tracker. Contributions are welcome via pull requests.