"""
Embedding providers for DocMind AI.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from google import genai

from config import settings
from models import (
    DocumentChunk,
    EmbeddedChunk,
)
from utils.logger import get_logger


logger = get_logger(__name__)


class EmbeddingProvider(ABC):
    """
    Base class for embedding providers.
    """

    @abstractmethod
    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddedChunk]:
        """
        Generate embeddings for document chunks.
        """
        raise NotImplementedError
    
    @abstractmethod
    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a user query.
        """
        raise NotImplementedError


class GeminiEmbeddingProvider(EmbeddingProvider):
    """
    Google Gemini embedding provider.
    """

    MODEL_NAME = settings.embedding_model

    def __init__(
        self,
        batch_size: int = 32,
    ) -> None:
        self.batch_size = batch_size

        self._client = genai.Client(
            api_key=settings.google_api_key,
        )

        logger.info(
            "Initialized Gemini embedding provider."
        )

    # ==========================================================
    # Private Helpers
    # ==========================================================

    def _batch_chunks(
        self,
        chunks: list[DocumentChunk],
    ):
        """
        Yield successive batches of chunks.
        """

        for i in range(
            0,
            len(chunks),
            self.batch_size,
        ):
            yield chunks[i : i + self.batch_size]

    # ==========================================================
    # Public API
    # ==========================================================

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddedChunk]:
        """
        Generate embeddings for document chunks.
        """

        if not chunks:
            return []

        logger.info(
            "Generating embeddings for %d chunks.",
            len(chunks),
        )

        embedded_chunks: list[EmbeddedChunk] = []

        batches = list(
            self._batch_chunks(chunks)
        )

        total_batches = len(batches)

        for batch_index, batch in enumerate(
            batches,
            start=1,
        ):

            logger.info(
                "Embedding batch %d/%d (%d chunks).",
                batch_index,
                total_batches,
                len(batch),
            )

            texts = [
                chunk.text
                for chunk in batch
            ]

            try:

                response = self._client.models.embed_content(
                    model=self.MODEL_NAME,
                    contents=texts,
                )

            except Exception as exc:

                logger.exception(
                    "Embedding request failed."
                )

                raise RuntimeError(
                    "Failed to generate embeddings."
                ) from exc

            for chunk, embedding in zip(
                batch,
                response.embeddings,
            ):

                embedded_chunks.append(
                    EmbeddedChunk(
                        chunk=chunk,
                        embedding=embedding.values,
                    )
                )

        logger.info(
            "Generated %d embeddings.",
            len(embedded_chunks),
        )

        return embedded_chunks

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a search query.
        """

        logger.info(
            "Embedding query."
        )

        response = self._client.models.embed_content(
            model=self.MODEL_NAME,
            contents=query,
        )

        return response.embeddings[0].values