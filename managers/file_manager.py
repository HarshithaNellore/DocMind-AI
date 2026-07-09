"""
File management for DocMind AI.

The FileManager owns all filesystem-related operations for uploaded
documents. It validates file types, generates document identifiers,
constructs storage filenames, and persists uploaded files.

It deliberately does NOT know anything about repositories,
DocumentMetadata, processors, embeddings, or Streamlit UI.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4

from config import settings
from custom_types import (
    DocumentId,
    FileName,
    StoredFileName,
)
from exceptions import UnsupportedFileTypeError
from utils.hashing import calculate_file_sha256
from utils.logger import get_logger
from models import UploadResult
from utils.hashing import calculate_file_sha256


logger = get_logger(__name__)


class FileManager:
    """
    Handles filesystem operations for uploaded documents.
    """

    def __init__(self) -> None:
        """
        Initialize the file manager and ensure the upload directory exists.
        """

        self._upload_dir = settings.upload_dir

        if self._upload_dir.exists():
            if not self._upload_dir.is_dir():
                raise NotADirectoryError(
                    f"{self._upload_dir} exists but is not a directory."
                )
        else:
            self._upload_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

        logger.info(
            "Upload directory initialized: %s",
            self._upload_dir,
        )

    @property
    def upload_directory(self) -> Path:
        """Return the upload directory."""
        return self._upload_dir

    def generate_document_id(self) -> DocumentId:
        """
        Generate a unique document identifier.
        """
        return str(uuid4())

    def validate_file_type(self, file_name: FileName) -> None:
        """
        Validate that the uploaded file extension is supported.

        Raises
        ------
        UnsupportedFileTypeError
        """
        extension = Path(file_name).suffix.lower()

        if extension not in settings.supported_extensions:
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {extension}"
            )

    def build_storage_filename(
        self,
        document_id: DocumentId,
        original_filename: FileName,
    ) -> StoredFileName:
        """
        Build the filename used for storage.

        Example
        -------
        UUID.pdf
        """
        extension = Path(original_filename).suffix.lower()

        return f"{document_id}{extension}"

    def save_uploaded_file(
        self,
        uploaded_file: BinaryIO,
        stored_filename: StoredFileName,
    ) -> Path:
        """
        Save an uploaded file to disk.

        Parameters
        ----------
        uploaded_file
            File-like object opened in binary mode.

        stored_filename
            Filename used inside the uploads directory.

        Returns
        -------
        Path
            Saved file path.
        """

        destination = self._upload_dir / stored_filename

        logger.info(
            "Saving uploaded file '%s'.",
            destination.name,
        )

        uploaded_file.seek(0)

        with destination.open("wb") as output:
            shutil.copyfileobj(uploaded_file, output)

        uploaded_file.seek(0)

        return destination

    def calculate_sha256(
        self,
        file_path: Path,
    ) -> str:
        """
        Calculate SHA256 for a saved file.
        """
        return calculate_file_sha256(file_path)
    

    def prepare_upload(self, uploaded_file: BinaryIO) -> UploadResult:
        """Validate and persist an uploaded document.

        Returns
        -------
        UploadResult
        """

        # Validate file extension
        self.validate_file_type(getattr(uploaded_file, "name", ""))

        # Generate identifiers and storage names
        document_id = self.generate_document_id()
        stored_name = self.build_storage_filename(document_id, getattr(uploaded_file, "name", ""))

        # Save file and compute metadata
        saved_path = self.save_uploaded_file(uploaded_file, stored_name)
        sha256 = calculate_file_sha256(saved_path)

        return UploadResult(
            document_id=document_id,
            original_filename=getattr(uploaded_file, "name", ""),
            stored_filename=stored_name,
            saved_path=str(saved_path),
            sha256=sha256,
            file_size=saved_path.stat().st_size,
        )
    
    def delete_file(
        self,
        file_path: str | Path,
    ) -> bool:
        """
        Delete a stored file.
        """

        path = Path(file_path)

        if not path.exists():
            return False

        path.unlink()

        logger.info(
            "Deleted file '%s'.",
            path.name,
        )

        return True