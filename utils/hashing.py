"""
SHA256 hashing utilities.

All hashing is performed using streaming reads to avoid loading
large files entirely into memory.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import BinaryIO

from streamlit.logger import get_logger

from custom_types import SHA256Hash
from .logger import get_logger

logger = get_logger(__name__)

BUFFER_SIZE = 8192


def _calculate_stream_hash(stream: BinaryIO) -> SHA256Hash:
    """
    Calculate SHA256 for an open binary stream.
    """

    hasher = hashlib.sha256()

    while chunk := stream.read(BUFFER_SIZE):
        hasher.update(chunk)

    return hasher.hexdigest()


def calculate_file_sha256(path: Path) -> SHA256Hash:
    """
    Calculate SHA256 for a file on disk.
    """

    logger.debug("Calculating SHA256: %s", path.name)

    with path.open("rb") as file:
        return _calculate_stream_hash(file)


def calculate_uploaded_file_sha256(uploaded_file) -> SHA256Hash:
    """
    Calculate SHA256 for a Streamlit UploadedFile.

    The file pointer is restored afterwards.
    """

    logger.debug("Calculating uploaded file SHA256.")

    uploaded_file.seek(0)

    digest = _calculate_stream_hash(uploaded_file)

    uploaded_file.seek(0)

    return digest