"""
Upload page.
"""

from __future__ import annotations

import streamlit as st

from ui.components import (
    Chat,
    Uploader,
)
from ui.components.workspace_header import WorkspaceHeader
from ui.components import Workspace


class UploadPage:
    """
    Upload page.
    """

    def __init__(
        self,
        container,
    ) -> None:

        self.container = container

    def render(self) -> None:

        WorkspaceHeader().render()

        left_column, right_column = st.columns(
            [1, 2],
            gap="large",
        )

        # ==========================================================
        # Left Column
        # ==========================================================

        with left_column:

            st.subheader("📂 Upload Documents")

            workspace = Workspace(
                self.container,
            )

            uploaded_files = workspace.render()

            if uploaded_files:

                button_text = (
                    f"🚀 Process Documents ({len(uploaded_files)})"
                )

                if st.button(
                    button_text,
                    type="primary",
                    use_container_width=True,
                ):

                    progress = st.progress(0)

                    status = st.empty()

                    total = len(uploaded_files)

                    for index, uploaded_file in enumerate(
                        uploaded_files,
                        start=1,
                    ):

                        status.info(
                            f"Processing {uploaded_file.name}..."
                        )

                        try:

                            result = (
                                self.container.document_manager.ingest_document(
                                    uploaded_file
                                )
                            )

                            st.toast(
                                f"Indexed {result.metadata.file_name}",
                                icon="✅",
                            )

                        except Exception as exc:

                            st.error(str(exc))

                        progress.progress(index / total)

                    status.success(
                        "Processing complete."
                    )

            else:

              st.info(
    """
👆 Select one or more documents from your computer.

Supported formats:

• PDF

• DOCX

• TXT
"""
)

        # ==========================================================
        # Right Column
        # ==========================================================

        with right_column:

            Chat(
                pipeline=self.container.pipeline,
            ).render()