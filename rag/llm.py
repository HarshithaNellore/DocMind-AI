"""
Gemini chat provider for DocMind AI.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

from google import genai

from config import settings
from utils.logger import get_logger


logger = get_logger(__name__)


class ChatProvider(ABC):
    """
    Base interface for chat providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a complete response.
        """
        raise NotImplementedError

    @abstractmethod
    def stream(
        self,
        prompt: str,
    ) -> Iterator[str]:
        """
        Stream a response token by token.
        """
        raise NotImplementedError


class GeminiChatProvider(ChatProvider):
    """
    Google Gemini chat provider.
    """

    def __init__(self) -> None:

        self._client = genai.Client(
            api_key=settings.google_api_key,
        )

        self._model = settings.chat_model

        logger.info(
            "Initialized Gemini chat provider."
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a complete response.
        """

        logger.info("Generating response.")

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )

        return response.text

    def stream(
        self,
        prompt: str,
    ) -> Iterator[str]:
        """
        Stream a response.
        """

        logger.info("Streaming response.")

        stream = self._client.models.generate_content_stream(
            model=self._model,
            contents=prompt,
        )

        for chunk in stream:

            if chunk.text:
                yield chunk.text