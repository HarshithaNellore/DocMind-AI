"""
Sidebar component.
"""

from __future__ import annotations

import streamlit as st

from managers import DocumentManager

from ui.components.document_library import (
    DocumentLibrary,
)


class Sidebar:
    """
    Application sidebar.
    """

    def __init__(
        self,
        document_manager: DocumentManager,
    ) -> None:

        self._document_manager = document_manager

    def render(self) -> None:

        with st.sidebar:

            st.title("📄 DocMind AI")

            st.divider()

            documents = (
                self._document_manager.list_documents()
            )

            total_documents = len(documents)

            total_pages = sum(
                document.total_pages
                for document in documents
            )

            total_chunks = sum(
                document.total_chunks
                for document in documents
            )

            st.subheader("📊 Workspace")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Documents",
                    total_documents,
                )

            with col2:

                st.metric(
                    "Pages",
                    total_pages,
                )

            st.metric(
                "Chunks",
                total_chunks,
            )

            st.divider()

            DocumentLibrary(
                self._document_manager,
            ).render()

            st.divider()

            st.caption("Version 2")