"""
Document chunking for DocMind AI.

Splits processed documents into overlapping chunks suitable
for embedding and retrieval.
"""

from __future__ import annotations
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models import (
    DocumentChunk,
    ProcessedDocument,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class Chunker:
    """
    Splits documents into overlapping text chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _build_chunk_id(
        document_id: str,
        chunk_index: int,
    ) -> str:
        """
        Build a deterministic chunk identifier.
        """

        return f"{document_id}_{chunk_index:04d}"
    
    def _find_chunk_end(
        self,
        text: str,
        start: int,
    ) -> int:
        """
        Determine the best end position for a chunk.

        Preference order:
        1. Newline
        2. Whitespace
        3. Hard boundary
        """

        hard_end = min(
            start + self.chunk_size,
            len(text),
        )

        # End of document
        if hard_end >= len(text):
            return len(text)

        # Search backwards for newline
        newline = text.rfind(
            "\n",
            start,
            hard_end,
        )

        if newline != -1 and newline > start:
            return newline

        # Search backwards for whitespace
        whitespace = text.rfind(
            " ",
            start,
            hard_end,
        )

        if whitespace != -1 and whitespace > start:
            return whitespace

        return hard_end


    # ==========================================================
    # Public API
    # ==========================================================

    def chunk_document(
        self,
        document: ProcessedDocument,
    ) -> list[DocumentChunk]:
        """
        Split a processed document into overlapping chunks.
        """

        logger.info(
            "Chunking '%s'.",
            document.metadata.file_name,
        )

        chunks: list[DocumentChunk] = []

        chunk_index = 0

        step = self.chunk_size - self.chunk_overlap

        for page in document.pages:

            text = page.text

            if not text.strip():
                continue

            start = 0

            while start < len(text):

                end = self._find_chunk_end(
                    text,
                    start,
                )

                chunk_text = text[start:end].strip()

                if not chunk_text:
                    start += step
                    continue

                chunks.append(
                    DocumentChunk(
                        chunk_id=self._build_chunk_id(
                            document.metadata.document_id,
                            chunk_index,
                        ),
                        document_id=document.metadata.document_id,
                        chunk_index=chunk_index,
                        page_number=page.page_number,
                        start_char=start,
                        end_char=end,
                        text=chunk_text,
                       metadata={
                           "file_name": document.metadata.file_name,
                           "processor": document.processor,
                           "document_type": document.metadata.file_type.value,
                           "page": page.page_number,
                           },
                    )
                )

                chunk_index += 1

                start += step

        logger.info(
            (
                "Chunking complete | "
                "Document='%s' | "
                "Pages=%d | "
                "Chunks=%d | "
                "Chunk Size=%d | "
                "Overlap=%d"
                
            ),
            document.metadata.file_name,
            len(document.pages),
            len(chunks),
            self.chunk_size,
            self.chunk_overlap,
            )

        return chunks