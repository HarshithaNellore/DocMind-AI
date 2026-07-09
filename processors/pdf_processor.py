"""
PDF document processor.
"""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from exceptions import ProcessingError
from models import (
    DocumentMetadata,
    ProcessedPage,
)
from processors.base_processor import BaseProcessor


class PDFProcessor(BaseProcessor):
    """
    Processor responsible for PDF documents.
    """

    PROCESSOR_NAME = "PDF Processor"

    SUPPORTED_EXTENSION = ".pdf"

    def process(
        self,
        file_path: Path,
        metadata: DocumentMetadata,
    ):
        """
        Extract text from a PDF.
        """

        self.validate_file(file_path)

        self.logger.info(
            "Processing PDF '%s'.",
            file_path.name,
        )

        try:
            reader = PdfReader(file_path)

        except Exception as exc:
            raise ProcessingError(
                f"Unable to open PDF '{file_path.name}'."
            ) from exc

        pages: list[ProcessedPage] = []

        warnings: list[str] = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):

            try:
                text = page.extract_text() or ""

            except Exception as exc:

                warnings.append(
                    f"Page {page_number}: extraction failed."
                )

                self.logger.warning(
                    "Failed extracting page %d: %s",
                    page_number,
                    exc,
                )

                text = ""

            text = self.normalize_text(text)

            if not text:

                warnings.append(
                    f"Page {page_number}: no extractable text."
                )

            pages.append(
                ProcessedPage(
                    page_number=page_number,
                    text=text,
                )
            )

        self.logger.info(
            "Extracted %d pages from '%s'.",
            len(pages),
            file_path.name,
        )

        return self.build_processed_document(
            metadata=metadata,
            pages=pages,
            warnings=warnings,
        )