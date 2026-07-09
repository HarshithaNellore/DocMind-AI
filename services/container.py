"""
Dependency container for DocMind AI.

Creates and wires together all application services.
"""

from __future__ import annotations

from managers import DocumentManager, FileManager
from repositories import MetadataRepository

from rag import (
    Chunker,
    GeminiEmbeddingProvider,
    GeminiChatProvider,
    Indexer,
    Retriever,
    PromptBuilder,
    RAGPipeline,
    VectorStore,
)


class ServiceContainer:
    """
    Central dependency container.
    """

    def __init__(self) -> None:

        # ==========================
        # Core Services
        # ==========================

        self.metadata_repository = MetadataRepository()
        self.file_manager = FileManager()

        # ==========================
        # RAG Services
        # ==========================

        self.chunker = Chunker()

        self.embedding_provider = GeminiEmbeddingProvider()

        self.vector_store = VectorStore()

        self.indexer = Indexer(
            embedding_provider=self.embedding_provider,
            vector_store=self.vector_store,
        )

        self.document_manager = DocumentManager(
            repository=self.metadata_repository,
            file_manager=self.file_manager,
            chunker=self.chunker,
            indexer=self.indexer,
        )

        self.retriever = Retriever(
            embedding_provider=self.embedding_provider,
            vector_store=self.vector_store,
        )

        self.prompt_builder = PromptBuilder()

        self.chat_provider = GeminiChatProvider()

        self.pipeline = RAGPipeline(
            retriever=self.retriever,
            prompt_builder=self.prompt_builder,
            chat_provider=self.chat_provider,
        )