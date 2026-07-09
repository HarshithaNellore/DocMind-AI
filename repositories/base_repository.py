"""
Base repository implementation.

Provides reusable JSON persistence for repositories.
"""

from __future__ import annotations

import json
from abc import ABC
from pathlib import Path
from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)


class BaseRepository(ABC):
    """
    Base class for JSON-backed repositories.
    """

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

        self._file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    @property
    def file_path(self) -> Path:
        return self._file_path

    def exists(self) -> bool:
        return self._file_path.exists()

    def _ensure_exists(
        self,
        default_data: dict[str, Any],
    ) -> None:
        """
        Ensure the repository file exists.
        """

        if self.exists():
            return

        logger.info(
            "Creating repository: %s",
            self.file_path.name,
        )

        self._save_json(default_data)

    def _load_json(self) -> dict[str, Any]:
        """
        Load JSON from disk.

        Assumes the file already exists.
        """

        with self.file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def _save_json(
        self,
        data: dict[str, Any],
    ) -> None:
        """
        Atomically save JSON.
        """

        temp_path = self.file_path.with_suffix(".tmp")

        with temp_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        temp_path.replace(self.file_path)

        logger.debug(
            "Saved repository '%s'.",
            self.file_path.name,
        )