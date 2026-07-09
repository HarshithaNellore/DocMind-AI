"""
Base document processor.

Defines the common interface and shared functionality for all
document processors.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from pathlib import Path

from exceptions import ProcessingError
from models import (
    DocumentMetadata,
    ProcessedDocument,
    ProcessedPage,
)
from utils.logger import get_logger


class BaseProcessor(ABC):
    """
    Abstract base class for document processors.
    """

    PROCESSOR_NAME: str = "Base Processor"

    SUPPORTED_EXTENSION: str = ""

    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__module__)

    @property
    def processor_name(self) -> str:
        """
        Human-readable processor name.
        """
        return self.PROCESSOR_NAME

    @property
    def supported_extension(self) -> str:
        """
        Supported file extension.
        """
        return self.SUPPORTED_EXTENSION

    def validate_file(
        self,
        file_path: Path,
    ) -> None:
        """
        Validate that the file exists and can be processed.

        Raises
        ------
        ProcessingError
        """

        if not file_path.exists():
            raise ProcessingError(
                f"File does not exist: {file_path}"
            )

        if not file_path.is_file():
            raise ProcessingError(
                f"Expected a file but received: {file_path}"
            )

        if (
            file_path.suffix.lower()
            != self.supported_extension
        ):
            raise ProcessingError(
                f"{self.processor_name} "
                f"does not support "
                f"'{file_path.suffix}'."
            )

        self.logger.debug(
            "Validated file '%s'.",
            file_path.name,
        )

    def normalize_text(
        self,
        text: str,
    ) -> str:
        """
        Normalize extracted text.

        This keeps all processors consistent.
        """

        if not text:
            return ""

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Collapse repeated whitespace while preserving newlines.
        text = re.sub(r"[ \t]+", " ", text)

        # Remove repeated blank lines.
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
    

    def post_process_pages(
        self,
        pages: list[ProcessedPage],
    ) -> list[ProcessedPage]:
        """
        Optional post-processing hook.

        The default implementation performs no modifications.

        Subclasses may override this to remove headers,
        footers, OCR artefacts, or perform additional cleanup.
        """

        return pages

    def build_processed_document(
        self,
        metadata: DocumentMetadata,
        pages: list[ProcessedPage],
        warnings: list[str] | None = None,
    ) -> ProcessedDocument:
        """
        Construct a ProcessedDocument.

        This ensures every processor produces documents in
        a consistent format.
        """

        pages = self.post_process_pages(pages)

        return ProcessedDocument(
            metadata=metadata,
            pages=pages,
            processor=self.processor_name,
            warnings=warnings or [],
        )

    @abstractmethod
    def process(
        self,
        file_path: Path,
        metadata: DocumentMetadata,
    ) -> ProcessedDocument:
        """
        Extract a document into a ProcessedDocument.
        """
        raise NotImplementedError