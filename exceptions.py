"""
Application-specific exceptions for DocMind AI.

The project uses a small hierarchy of custom exceptions instead of
generic ValueError/RuntimeError to make error handling explicit.
"""

from __future__ import annotations


class DocMindError(Exception):
    """Base exception for DocMind AI."""


# ==========================================================
# Repository
# ==========================================================


class RepositoryError(DocMindError):
    """Raised for repository-related failures."""


# ==========================================================
# Files
# ==========================================================


class FileError(DocMindError):
    """Base class for file-related exceptions."""


class UnsupportedFileTypeError(FileError):
    """Raised when an unsupported file type is uploaded."""


class DuplicateDocumentError(FileError):
    """Raised when a duplicate document is detected."""


class InvalidDocumentError(FileError):
    """Raised when a document is invalid or corrupted."""


# ==========================================================
# Processing
# ==========================================================


class ProcessingError(DocMindError):
    """Raised when document processing fails."""


# ==========================================================
# RAG
# ==========================================================


class RAGError(DocMindError):
    """Raised for Retrieval-Augmented Generation failures."""