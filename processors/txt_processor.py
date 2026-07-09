"""
Plain text processor.
"""

from __future__ import annotations

from pathlib import Path

from exceptions import ProcessingError
from models import (
    DocumentMetadata,
    ProcessedPage,
)
from processors.base_processor import BaseProcessor


class TXTProcessor(BaseProcessor):
    """
    Processor for text documents.
    """

    PROCESSOR_NAME = "TXT Processor"

    SUPPORTED_EXTENSION = ".txt"

    def process(
        self,
        file_path: Path,
        metadata: DocumentMetadata,
    ):
        self.validate_file(file_path)

        try:
            text = file_path.read_text(
                encoding="utf-8",
            )

        except Exception as exc:
            raise ProcessingError(
                f"Unable to read '{file_path.name}'."
            ) from exc

        text = self.normalize_text(text)

        pages = [
            ProcessedPage(
                page_number=1,
                text=text,
            )
        ]

        warnings = []

        if not text:
            warnings.append(
                "Document is empty."
            )

        return self.build_processed_document(
            metadata=metadata,
            pages=pages,
            warnings=warnings,
        )