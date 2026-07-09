"""
Application configuration for DocMind AI.

This module exposes a singleton `settings` object that is used
throughout the application.

Configuration values are loaded from environment variables and
validated using Pydantic Settings.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# ============================================================================
# Project Paths
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """
    Application settings.

    Values are loaded from environment variables when available,
    otherwise the defaults defined below are used.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ========================================================================
    # Application
    # ========================================================================

    app_name: str = "DocMind AI"

    app_version: str = "2.0.0"

    environment: str = Field(
        default="development",
        alias="APP_ENV",
    )

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    # ========================================================================
    # Google Gemini
    # ========================================================================

    google_api_key: str = Field(
        alias="GOOGLE_API_KEY",
    )

    chat_model: str = "gemini-3.1-flash-lite"

    embedding_model: str = "gemini-embedding-001"

    # ========================================================================
    # Chunking
    # ========================================================================

    chunk_size: int = 1000

    chunk_overlap: int = 200

    min_chunk_size: int = 100

    # ========================================================================
    # Embeddings
    # ========================================================================

    embedding_batch_size: int = 32

    # ========================================================================
    # Project Directories
    # ========================================================================

    base_dir: Path = BASE_DIR

    data_dir: Path = BASE_DIR / "data"

    upload_dir: Path = data_dir / "uploads"

    metadata_file: Path = data_dir / "metadata.json"

    logs_dir: Path = BASE_DIR / "logs"

    assets_dir: Path = BASE_DIR / "assets"

    # ========================================================================
    # Vector Store
    # ========================================================================

    vector_store_path: Path = BASE_DIR / "chroma_db"

    vector_collection_name: str = "docmind_documents"

    # ========================================================================
    # Supported Files
    # ========================================================================

    supported_extensions: tuple[str, ...] = (
        ".pdf",
        ".docx",
        ".txt",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    The configuration is loaded only once during the application's
    lifetime.
    """
    return Settings()


settings = get_settings()