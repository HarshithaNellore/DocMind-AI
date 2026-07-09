"""
Processor factory.

Creates the correct processor implementation
for a supported document type.
"""

from __future__ import annotations

from models import DocumentType
from exceptions import ProcessingError

from .base_processor import BaseProcessor
from .docx_processor import DOCXProcessor
from .pdf_processor import PDFProcessor
from .txt_processor import TXTProcessor


_PROCESSOR_MAP: dict[DocumentType, type[BaseProcessor]] = {
    DocumentType.PDF: PDFProcessor,
    DocumentType.DOCX: DOCXProcessor,
    DocumentType.TXT: TXTProcessor,
}


class ProcessorFactory:
    """Factory responsible for creating document processors."""

    @staticmethod
    def create(document_type: DocumentType) -> BaseProcessor:
        """
        Return the processor corresponding to the document type.

        Raises
        ------
        ProcessingError
            If no processor is registered.
        """

        processor_cls = _PROCESSOR_MAP.get(document_type)

        if processor_cls is None:
            raise ProcessingError(
                f"No processor registered for '{document_type.value}'."
            )

        return processor_cls()