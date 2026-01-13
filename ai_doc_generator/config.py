from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    EXCLUSION_LIST: list[str] = [
        ".git",
        ".venv",
        "node_modules",
        "__pycache__",
        ".DS_Store",
        "pb_data",
        "pb_public",
        "migrations",
        ".pytest_cache",
        "venv",
        "data",
        ".vscode",
        ".idea",
        ".ruff_cache",
        ".mypy_cache",
        ".yamllint",
        "alembic.ini"
        "uv.lock",
        "poetry.lock",
        ".env",
        ".gitignore",
        ".dockerignore",
        "static",
        "images",
        "logo.png",
        "_static",
        "htmlcov",
        ".coverage",
        "tests",
        "scripts",
        "configs",
        ".gitlab",
        ".gitlab-ci.yml",
        ".airflow-cli.json",
    ]

    MAX_FILE_SIZE: int = 100 * 1024
    LOCAL_LLM_BASE_URL: str = "http://localhost:11434/v1"
    LOCAL_LLM_API_KEY: str = "local"
    LOCAL_LLM_MODEL: str = "llm_model"
    GUIDE_TARGET_PROJECT_DIRECTORY: str = "./target_project"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )

settings = Settings()
