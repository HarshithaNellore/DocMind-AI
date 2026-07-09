"""
Metadata repository.

This repository is responsible for storing and retrieving
DocumentMetadata objects from metadata.json.

No other module should access metadata.json directly.
"""

from __future__ import annotations

from json import JSONDecodeError
from typing import Optional

from pydantic import ValidationError
from config import settings
from models import (
    DocumentMetadata,
    DocumentStatus,
    MetadataRegistry,
)
from repositories.base_repository import BaseRepository
from utils.logger import get_logger
logger = get_logger(__name__)


class MetadataRepository(BaseRepository):
    """
    Repository responsible for managing document metadata.
    """

    def __init__(self) -> None:
        super().__init__(settings.metadata_file)

        self._initialize()

    # ==========================================================
    # Private Helpers
    # ==========================================================

    def _initialize(self) -> None:
        """
        Create an empty registry if it does not exist.
        """

        if self.exists():
            return

        logger.info("Creating metadata registry.")

        self._save_registry(MetadataRegistry())

    def _load_registry(self) -> MetadataRegistry:
        """
        Load and validate the metadata registry.
        """

        try:
            raw = self._load_json()

            return MetadataRegistry.model_validate(raw)

        except FileNotFoundError:

            logger.warning(
                "Metadata registry missing. Creating a new one."
            )

        except (ValidationError, JSONDecodeError):

            logger.warning(
                "Metadata registry corrupted. Recreating it."
            )

        registry = MetadataRegistry()

        self._save_registry(registry)

        return registry

    def _save_registry(
        self,
        registry: MetadataRegistry,
    ) -> None:
        """
        Persist registry to disk.
        """

        self._save_json(
            registry.model_dump(mode="json")
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def get_all(self) -> list[DocumentMetadata]:
        """
        Return every registered document.
        """

        return self._load_registry().documents

    def get_by_id(
        self,
        document_id: str,
    ) -> Optional[DocumentMetadata]:
        """
        Find a document by its ID.
        """

        for document in self.get_all():

            if document.document_id == document_id:
                return document

        return None

    def get_by_sha256(
        self,
        sha256: str,
    ) -> Optional[DocumentMetadata]:
        """
        Find a document using its SHA256 hash.
        """

        for document in self.get_all():

            if document.sha256 == sha256:
                return document

        return None
    

    def add(self,metadata: DocumentMetadata,) -> DocumentMetadata:
        """
        Register a new document.
        """

        registry = self._load_registry()

        registry.documents.append(metadata)

        self._save_registry(registry)

        logger.info(
            "Registered document '%s'.",
            metadata.file_name,
        )

    def update(
        self,
        metadata: DocumentMetadata,
    ) -> bool:
        """
        Replace an existing metadata entry.

        Returns
        -------
        bool
            True if updated.
        """

        registry = self._load_registry()

        for index, document in enumerate(registry.documents):

            if document.document_id == metadata.document_id:

                registry.documents[index] = metadata

                self._save_registry(registry)

                logger.info(
                    "Updated '%s'.",
                    metadata.file_name,
                )

                return True

        return False

    def update_status(
        self,
        document_id: str,
        status: DocumentStatus,
    ) -> bool:
        """
        Update processing status.
        """

        document = self.get_by_id(document_id)

        if document is None:
            return False

        updated = document.model_copy(
            update={
                "status": status
            }
        )

        return self.update(updated)

    def delete(
        self,
        document_id: str,
    ) -> bool:
        """
        Remove metadata entry.
        """

        registry = self._load_registry()

        before = len(registry.documents)

        registry.documents = [
            document
            for document in registry.documents
            if document.document_id != document_id
        ]

        if before == len(registry.documents):
            return False

        self._save_registry(registry)

        logger.info(
            "Deleted metadata '%s'.",
            document_id,
        )

        return True