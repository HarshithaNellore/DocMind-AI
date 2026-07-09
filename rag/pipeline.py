"""
RAG pipeline.

Coordinates retrieval, prompt construction,
and response generation.
"""

from __future__ import annotations

from models import RAGResponse

from rag.llm import ChatProvider
from rag.prompt_builder import PromptBuilder
from rag.retriever import Retriever

from utils.logger import get_logger
from collections.abc import Iterator


logger = get_logger(__name__)


class RAGPipeline:
    """
    Main Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        chat_provider: ChatProvider,
    ) -> None:

        self._retriever = retriever
        self._prompt_builder = prompt_builder
        self._chat_provider = chat_provider

    # ==========================================================
    # Public API
    # ==========================================================

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ) -> RAGResponse:
        """
        Answer a question using retrieved context.
        """

        logger.info(
            "Processing question."
        )

        retrieved_chunks = self._retriever.retrieve(
            question=question,
            top_k=top_k,
        )

        prompt = self._prompt_builder.build(
            question=question,
            chunks=retrieved_chunks,
        )

        answer = self._chat_provider.generate(
            prompt
        )

        logger.info(
            "Question answered successfully."
        )

        return RAGResponse(
            answer=answer,
            sources=retrieved_chunks,
        )
    def stream(
        self,
        question: str,
        top_k: int = 5,
    ) -> Iterator[str]:
        """
        Stream an answer using retrieved context.
        """

        logger.info("Streaming response.")

        retrieved_chunks = self._retriever.retrieve(
            question=question,
            top_k=top_k,
        )

        prompt = self._prompt_builder.build(
            question=question,
            chunks=retrieved_chunks,
        )

        yield from self._chat_provider.stream(prompt)


    def retrieve_context(
        self,
        question: str,
        top_k: int = 5,
    ):
        """
        Retrieve supporting document chunks.

        Returns
        -------
        list[RetrievedChunk]
        """

        return self._retriever.retrieve(
            question=question,
            top_k=top_k,
        )