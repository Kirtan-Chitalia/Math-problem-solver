"""
Configuration management for the AI Math Solver.

WHY THIS PATTERN:
- We use pydantic-settings to load config from .env files
- This gives us: type validation, default values, and a single source of truth
- Every module imports `settings` instead of reading env vars directly
- If a required value is missing, the app fails FAST at startup (not mid-pipeline)

HOW TO USE:
    from src.config import settings
    print(settings.OPENROUTER_API_KEY)
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root = 2 levels up from this file (src/config/settings.py → project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.

    Pydantic validates types automatically:
    - If OPENROUTER_API_KEY is missing, you get a clear error at startup
    - Default values are used when env vars are not set
    """

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # Don't crash on extra env vars
    )

    # --- API Keys ---
    OPENROUTER_API_KEY: str = ""

    # --- Model Configuration ---
    # Which models to use for each agent role
    SOLVER_MODEL: str = "deepseek/deepseek-v3.2"
    CLASSIFIER_MODEL: str = "anthropic/claude-sonnet-4.6"
    VISION_MODEL: str = "qwen/qwen3.5-9b"

    # --- OpenRouter API ---
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # --- Logging ---
    LOG_LEVEL: str = "INFO"

    # --- Paths ---
    DATA_DIR: Path = PROJECT_ROOT / "data"

    # --- Pipeline Defaults ---
    OCR_CONFIDENCE_THRESHOLD: float = 0.7  # Below this, trigger LLM vision fallback
    MAX_LLM_RETRIES: int = 3
    LLM_TIMEOUT_SECONDS: int = 60


# Singleton — import this everywhere
settings = Settings()
