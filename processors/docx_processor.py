"""
DOCX document processor.
"""

from __future__ import annotations

from pathlib import Path

from docx import Document

from exceptions import ProcessingError
from models import (
    DocumentMetadata,
    ProcessedPage,
)
from processors.base_processor import BaseProcessor


class DOCXProcessor(BaseProcessor):
    """
    Processor for Microsoft Word (.docx) documents.
    """

    PROCESSOR_NAME = "DOCX Processor"

    SUPPORTED_EXTENSION = ".docx"

    def process(
        self,
        file_path: Path,
        metadata: DocumentMetadata,
    ):
        self.validate_file(file_path)

        self.logger.info(
            "Processing DOCX '%s'.",
            file_path.name,
        )

        try:
            document = Document(file_path)

        except Exception as exc:
            raise ProcessingError(
                f"Unable to open DOCX '{file_path.name}'."
            ) from exc

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

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
                "Document contains no extractable text."
            )

        return self.build_processed_document(
            metadata=metadata,
            pages=pages,
            warnings=warnings,
        )