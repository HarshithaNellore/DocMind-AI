"""
Chat component.
"""

from __future__ import annotations

import streamlit as st

from rag.pipeline import RAGPipeline


class Chat:
    """
    Chat interface component.
    """

    SESSION_KEY = "chat_messages"

    def __init__(
        self,
        pipeline: RAGPipeline,
    ) -> None:

        self._pipeline = pipeline

        if self.SESSION_KEY not in st.session_state:

            st.session_state[self.SESSION_KEY] = []

    @property
    def messages(self):

        return st.session_state[self.SESSION_KEY]

    def render(self) -> None:

        header_col, button_col = st.columns(
            [6, 1]
        )

        with header_col:

            st.header("💬 Chat")

        with button_col:

            if st.button(
                "🗑",
                help="Clear conversation",
            ):

                self.messages.clear()

                st.rerun()

        # ==========================================================
        # Welcome Card
        # ==========================================================

        if not self.messages:

            st.info(
                """
👋 **Welcome to DocMind AI**

Upload one or more documents and ask questions about them.

### Try asking:

• Summarize this document.

• What are the key findings?

• Explain section 2.

• Compare two uploaded documents.
"""
            )

        # ==========================================================
        # Conversation History
        # ==========================================================

        for message in self.messages:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )

        prompt = st.chat_input(
            "Ask a question about your documents..."
        )

        if not prompt:

            return

        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            placeholder = st.empty()

            full_response = ""

            try:

                for token in self._pipeline.stream(
                    prompt,
                ):

                    full_response += token

                    placeholder.markdown(
                        full_response
                    )

                self.messages.append(
                    {
                        "role": "assistant",
                        "content": full_response,
                    }
                )

            except Exception as exc:

                st.error(str(exc))

                self.messages.append(
                    {
                        "role": "assistant",
                        "content": str(exc),
                    }
                )