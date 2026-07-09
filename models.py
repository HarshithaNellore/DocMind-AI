"""
Core domain models for DocMind AI.

These models define the contracts shared between managers,
repositories, processors, and the RAG pipeline.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from custom_types import (
    ChunkId,
    DocumentId,
    FileName,
    FilePath,
    SHA256Hash,
    StoredFileName,
)


# ============================================================================
# Enums
# ============================================================================


class DocumentType(str, Enum):
    """Supported document types."""

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    UNKNOWN = "unknown"


class DocumentStatus(str, Enum):
    """Document processing lifecycle."""

    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


# ============================================================================
# Metadata
# ============================================================================


class DocumentMetadata(BaseModel):
    """Metadata stored for each uploaded document."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    document_id: DocumentId

    file_name: FileName

    stored_name: StoredFileName

    file_path: FilePath

    file_type: DocumentType

    sha256: SHA256Hash

    file_size: int

    uploaded_at: datetime

    status: DocumentStatus = DocumentStatus.PENDING

    total_pages: int = 0

    total_chunks: int = 0


# ============================================================================
# Processing
# ============================================================================


class ProcessedPage(BaseModel):
    """Represents one extracted page."""

    model_config = ConfigDict(extra="forbid")

    page_number: int

    text: str


class ProcessedDocument(BaseModel):
    """
    Result returned by a document processor.

    This model represents extracted document content before chunking.
    """

    model_config = ConfigDict(extra="forbid")

    metadata: DocumentMetadata

    pages: list[ProcessedPage]

    processor: str

    extracted_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    warnings: list[str] = Field(
        default_factory=list,
    )


# ============================================================================
# Chunking
# ============================================================================


class DocumentChunk(BaseModel):
    """
    A chunk ready for embedding.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    chunk_id: ChunkId

    document_id: DocumentId

    chunk_index: int

    page_number: int

    start_char: int

    end_char: int

    text: str

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


# ============================================================================
# Embeddings
# ============================================================================


class EmbeddedChunk(BaseModel):
    """
    A document chunk together with its embedding vector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    chunk: DocumentChunk

    embedding: list[float]


# ============================================================================
# Retrieval
# ============================================================================

class RetrievedChunk(BaseModel):
    """
    A chunk retrieved from the vector store.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    chunk_id: str

    text: str

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    distance: float

# ============================================================================
# RAG
# ============================================================================

class RAGResponse(BaseModel):
    """
    Final response returned by the RAG pipeline.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    answer: str

    sources: list[RetrievedChunk]

    
# ============================================================================
# Upload
# ============================================================================


class UploadResult(BaseModel):
    """
    Result returned after successfully saving an uploaded document.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    document_id: DocumentId

    original_filename: FileName

    stored_filename: StoredFileName

    saved_path: FilePath

    sha256: SHA256Hash

    file_size: int


# ============================================================================
# Ingestion
# ============================================================================


class IngestionResult(BaseModel):
    """
    Result returned after document ingestion.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    metadata: DocumentMetadata

    processed_document: ProcessedDocument

    processing_time_ms: float

    is_duplicate: bool = False

    warnings: list[str] = Field(default_factory=list)



# ============================================================================
# Registry
# ============================================================================


class MetadataRegistry(BaseModel):
    """Persistent metadata registry."""

    model_config = ConfigDict(extra="forbid")

    documents: list[DocumentMetadata] = Field(default_factory=list)


# ============================================================================
# Chat
# ============================================================================


class ChatRequest(BaseModel):
    """Incoming chat request."""

    model_config = ConfigDict(extra="forbid")

    question: str

    document_ids: list[str] | None = None


class Citation(BaseModel):
    """Citation returned with an answer."""

    model_config = ConfigDict(extra="forbid")

    document_name: str

    page_number: int

    chunk_index: int


class ChatResponse(BaseModel):
    """Response returned by the RAG pipeline."""

    model_config = ConfigDict(extra="forbid")

    answer: str

    citations: list[Citation] = Field(default_factory=list)
