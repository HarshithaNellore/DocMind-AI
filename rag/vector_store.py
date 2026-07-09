"""
Persistent ChromaDB vector store.
"""

from __future__ import annotations

import chromadb

from config import settings

from utils.logger import get_logger
from models import (
    EmbeddedChunk,
    RetrievedChunk,
)


logger = get_logger(__name__)


class VectorStore:
    """
    Persistent vector store backed by ChromaDB.
    """

    def __init__(self) -> None:

        self._client = chromadb.PersistentClient(
            path=str(settings.vector_store_path),
        )

        self._collection = self._client.get_or_create_collection(
            name=settings.vector_collection_name,
        )

        logger.info(
            "Initialized vector store '%s'.",
            settings.vector_collection_name,
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def add_chunks(
        self,
        embedded_chunks: list[EmbeddedChunk],
    ) -> None:
        """
        Store embedded chunks in ChromaDB.
        """

        if not embedded_chunks:
            logger.warning(
                "No chunks supplied for indexing."
            )
            return

        ids: list[str] = []
        documents: list[str] = []
        embeddings: list[list[float]] = []
        metadatas: list[dict] = []

        for item in embedded_chunks:

            ids.append(item.chunk.chunk_id)
            documents.append(item.chunk.text)
            embeddings.append(item.embedding)

            metadata = dict(item.chunk.metadata)

            metadata.update(
                {
                    "document_id": item.chunk.document_id,
                    "page_number": item.chunk.page_number,
                    "chunk_index": item.chunk.chunk_index,
                }
            )

            metadatas.append(metadata)

        self._collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        logger.info(
            "Indexed %d chunks.",
            len(ids),
        )

    def count(self) -> int:
        """
        Return the number of vectors stored in the collection.
        """
        return self._collection.count()

    def search(self, query_embedding: list[float], top_k: int = 5,) -> list[RetrievedChunk]:
        """
        Perform similarity search.
        """
        results = self._collection.query(query_embeddings=[query_embedding],n_results=top_k,)
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        ids = results["ids"][0]
        distances = results["distances"][0]
        retrieved: list[RetrievedChunk] = []
        
        for chunk_id, text, metadata, distance in zip(ids,documents,metadatas,distances,):
            retrieved.append(RetrievedChunk(chunk_id=chunk_id,text=text,metadata=metadata or {},distance=float(distance),))
        logger.info("Retrieved %d chunks.",len(retrieved))
        return retrieved
    
    def delete_document(
            self,
            document_id: str,
        ) -> None:
            """
            Remove all vectors belonging to a document.
            """

            self._collection.delete(
                where={
                    "document_id": document_id,
                }
            )

            logger.info(
                "Deleted vectors for '%s'.",
                document_id,
            )