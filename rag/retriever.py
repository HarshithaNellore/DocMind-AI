"""
Retriever for DocMind AI.
"""

from __future__ import annotations

from rag.embeddings import EmbeddingProvider
from rag.vector_store import VectorStore
from utils.logger import get_logger
from models import RetrievedChunk


logger = get_logger(__name__)


class Retriever:
    """
    Retrieve relevant chunks from the vector store.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:

        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Retrieve relevant chunks.
        """

        logger.info(
            "Retrieving context."
        )

        query_embedding = (
            self._embedding_provider.embed_query(
                question
            )
        )

        return self._vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )