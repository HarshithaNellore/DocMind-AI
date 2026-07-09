"""
Document ingestion manager.

Coordinates the complete document ingestion workflow.
"""

from __future__ import annotations
from pathlib import Path
from datetime import datetime
from time import perf_counter

from exceptions import DuplicateDocumentError
from managers.file_manager import FileManager
from models import (
    DocumentMetadata,
    DocumentStatus,
    DocumentType,
    IngestionResult,
)
from processors import ProcessorFactory
from repositories import MetadataRepository
from utils.logger import get_logger
from rag import Chunker, Indexer


logger = get_logger(__name__)


class DocumentManager:
    """
    Coordinates document ingestion.
    """

    def __init__(
        self,
        repository: MetadataRepository,
        file_manager: FileManager,
        chunker: Chunker,
        indexer: Indexer,
    ) -> None:

        self._repository = repository
        self._file_manager = file_manager
        self._chunker = chunker
        self._indexer = indexer

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _elapsed_ms(start: float) -> float:
        """
        Return elapsed milliseconds.
        """
        return round((perf_counter() - start) * 1000, 2)

    @staticmethod
    def _detect_document_type(
        filename: str,
    ) -> DocumentType:
        """
        Detect document type from filename.
        """

        extension = filename.rsplit(".", 1)[-1].lower()

        mapping = {
            "pdf": DocumentType.PDF,
            "docx": DocumentType.DOCX,
            "txt": DocumentType.TXT,
        }

        return mapping.get(
            extension,
            DocumentType.UNKNOWN,
        )

    def _create_metadata(
        self,
        upload,
    ) -> DocumentMetadata:
        """
        Create metadata for an uploaded document.
        """

        return DocumentMetadata(
            document_id=upload.document_id,
            file_name=upload.original_filename,
            stored_name=upload.stored_filename,
            file_path=upload.saved_path,
            file_type=self._detect_document_type(
                upload.original_filename,
            ),
            sha256=upload.sha256,
            file_size=upload.file_size,
            uploaded_at=datetime.now(),
            status=DocumentStatus.PROCESSING,
        )

    def _check_duplicate(
        self,
        sha256: str,
    ) -> None:
        """
        Raise if a duplicate document exists.
        """

        if self._repository.get_by_sha256(sha256):
            raise DuplicateDocumentError(
                "Duplicate document detected."
            )

    def _update_metadata(
        self,
        metadata: DocumentMetadata,
        *,
        total_pages: int,
        total_chunks: int = 0,
        status: DocumentStatus = DocumentStatus.READY,
    ) -> DocumentMetadata:
        """
        Update metadata after successful processing.
        """

        updated = metadata.model_copy(
            update={
                "status": status,
                "total_pages": total_pages,
                "total_chunks": total_chunks,
            }
        )

        self._repository.update(updated)

        logger.info(
            "Metadata updated for '%s'.",
            updated.file_name,
        )

        return updated

    def _mark_failed(
        self,
        metadata: DocumentMetadata,
    ) -> DocumentMetadata:
        """
        Mark document processing as failed.
        """

        failed = metadata.model_copy(
            update={
                "status": DocumentStatus.FAILED,
            }
        )

        self._repository.update(failed)

        logger.error(
            "Processing failed for '%s'.",
            failed.file_name,
        )

        return failed
    

    def _get_processor(
        self,
        document_type: DocumentType,
    ):
        """
        Return the correct processor for the document type.
        """

        return ProcessorFactory.create(document_type)

    def _build_result(
        self,
        metadata: DocumentMetadata,
        processed_document,
        processing_time_ms: float,
    ):
        """
        Build the final ingestion result.
        """

        return IngestionResult(
            metadata=metadata,
            processed_document=processed_document,
            processing_time_ms=processing_time_ms,
            warnings=processed_document.warnings,
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def ingest_document(
        self,
        uploaded_file,
    ) -> IngestionResult:
        """
        Upload and process a document.
        """

        logger.info(
            "Starting ingestion for '%s'.",
            uploaded_file.name,
        )

        start = perf_counter()

        upload = self._file_manager.prepare_upload(
            uploaded_file,
        )

        self._check_duplicate(upload.sha256)

        metadata = self._create_metadata(upload)

        self._repository.add(metadata)

        try:

            processor = self._get_processor(
                metadata.file_type,
            )

            processed_document = processor.process(
                Path(upload.saved_path),
                metadata,
            )

            # ==========================================================
            # Chunking
            # ==========================================================

            chunks = self._chunker.chunk_document(
            processed_document
            )

            # ==========================================================
            # Indexing
            # ==========================================================

            indexed_chunks = self._indexer.index_document(
            chunks
            )

            logger.info(
            "Indexed %d chunks.",
            indexed_chunks,
            )

            metadata = self._update_metadata(
                metadata,
                total_pages=len(processed_document.pages),
            )

        except Exception:

            self._mark_failed(metadata)

            raise

        elapsed = self._elapsed_ms(start)

        logger.info(
            "Finished ingestion in %.2f ms.",
            elapsed,
        )

        return self._build_result(
            metadata,
            processed_document,
            elapsed,
        )

    def list_documents(self) -> list[DocumentMetadata]:
        """
        Return all registered documents.
        """

        return self._repository.get_all()
    
    def get_document(
        self,
        document_id: str,
    ) -> DocumentMetadata | None:
        """
        Return a document by ID.
        """

        return self._repository.get_by_id(
            document_id,
        )
    

    def delete_document(
        self,
        document_id: str,
    ) -> bool:
        """
        Delete a document and all associated data.
        """

        metadata = self.get_document(
            document_id,
        )

        if metadata is None:

            logger.warning(
                "Document '%s' not found.",
                document_id,
            )

            return False

        # Delete uploaded file
        self._file_manager.delete_file(
            metadata.file_path,
        )

        # Delete vectors from ChromaDB
        self._indexer.remove_document(
            document_id,
        )

        # Delete metadata
        deleted = self._repository.delete(
            document_id,
        )

        if deleted:

            logger.info(
                "Deleted document '%s'.",
                metadata.file_name,
            )

        return deleted