"""
Lightweight replacement for Streamlit UploadedFile
used during integration testing.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path


class FakeUploadedFile(BytesIO):
    """
    A minimal replacement for Streamlit's UploadedFile.

    Behaves like a binary file object while exposing
    the `.name` attribute expected by FileManager.
    """

    def __init__(self, file_path: str | Path):
        self.path = Path(file_path)

        super().__init__(self.path.read_bytes())

        self.name = self.path.name