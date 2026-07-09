"""
File uploader component.
"""

from __future__ import annotations

import streamlit as st


class Uploader:
    """
    Reusable file uploader.
    """

    SUPPORTED_TYPES = [
        "pdf",
        "docx",
        "txt",
    ]

    def render(self):
        """
        Render uploader.

        Returns
        -------
        list[UploadedFile] | None
        """

        st.subheader("📂 Upload Documents")

        return st.file_uploader(
            label="Choose one or more documents",
            type=self.SUPPORTED_TYPES,
            accept_multiple_files=True,
            help=(
                "Supported formats: "
                "PDF, DOCX and TXT"
            ),
        )