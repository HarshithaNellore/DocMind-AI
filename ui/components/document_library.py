"""
Document library component.
"""

from __future__ import annotations

import streamlit as st

from managers import DocumentManager
from ui.components.document_card import DocumentCard


class DocumentLibrary:
    """
    Sidebar document library.
    """

    def __init__(
        self,
        document_manager: DocumentManager,
    ) -> None:

        self._document_manager = document_manager

    def render(self) -> None:

        documents = self._document_manager.list_documents()

        st.subheader("📚 Documents")

        if not documents:
            st.info(
                """
        📂 **No documents uploaded**

        Upload a PDF, DOCX or TXT file to start building your knowledge base.
        """
            )

            return
        st.caption(
            f"{len(documents)} document(s)"
        )

        st.divider()

        for document in documents:

            DocumentCard(
                document=document,
                document_manager=self._document_manager,
            ).render()