"""
Document card component.
"""

from __future__ import annotations

import streamlit as st

from managers import DocumentManager
from models import DocumentMetadata
from ui.components.badge import StatusBadge


class DocumentCard:
    """
    Displays one uploaded document.
    """

    def __init__(
        self,
        document: DocumentMetadata,
        document_manager: DocumentManager,
    ) -> None:

        self.document = document
        self.document_manager = document_manager

    def render(self) -> None:
        with st.expander(
            f"📄 {self.document.file_name}",
            expanded=False,
        ):

            # ----------------------------
            # Header
            # ----------------------------

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(
                    f"### {self.document.file_name}"
                )

                StatusBadge().render(
                    self.document.status
                )

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{self.document.document_id}",
                    help="Delete document",
                    use_container_width=True,
                ):

                    deleted = (
                        self.document_manager.delete_document(
                            self.document.document_id
                        )
                    )

                    if deleted:

                        st.toast(
                            "Document deleted.",
                            icon="🗑️",
                        )

                        st.rerun()

            st.divider()

            # ----------------------------
            # Metrics
            # ----------------------------

            metric1, metric2 = st.columns(2)

            with metric1:

                st.metric(
                    "Pages",
                    self.document.total_pages,
                )

            with metric2:

                st.metric(
                    "Chunks",
                    self.document.total_chunks,
                )

            st.caption(
                f"ID: {self.document.document_id}"
            )