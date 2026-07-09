"""
Document indexing pipeline.

Coordinates embedding generation and vector storage.
"""

from __future__ import annotations

from models import DocumentChunk
from rag.embeddings import EmbeddingProvider
from rag.vector_store import VectorStore
from utils.logger import get_logger


logger = get_logger(__name__)


class Indexer:
    """
    Coordinates document indexing.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:

        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def index_document(
        self,
        chunks: list[DocumentChunk],
    ) -> int:
        """
        Generate embeddings and store them.

        Returns
        -------
        int
            Number of indexed chunks.
        """

        if not chunks:

            logger.warning(
                "No chunks supplied for indexing."
            )

            return 0

        logger.info(
            "Indexing %d chunks.",
            len(chunks),
        )

        embedded_chunks = (
            self._embedding_provider.embed_chunks(
                chunks
            )
        )

        self._vector_store.add_chunks(
            embedded_chunks
        )

        logger.info(
            "Indexed %d chunks successfully.",
            len(embedded_chunks),
        )

        return len(embedded_chunks)
    
    def remove_document(
        self,
        document_id: str,
    ) -> None:
        """
        Remove document vectors.
        """

        self._vector_store.delete_document(
            document_id
        )