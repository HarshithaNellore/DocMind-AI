"""
Integration test for the complete ingestion pipeline.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from managers import DocumentManager, FileManager
from repositories import MetadataRepository
from fake_uploaded_file import FakeUploadedFile


def main() -> None:

    repository = MetadataRepository()

    file_manager = FileManager()

    manager = DocumentManager(
        repository=repository,
        file_manager=file_manager,
    )

    uploaded_file = FakeUploadedFile(
        Path("tests/assets/sample.txt")
    )

    result = manager.ingest_document(uploaded_file)

    print("\n===== INGESTION RESULT =====\n")

    print("Document ID :", result.metadata.document_id)

    print("File Name   :", result.metadata.file_name)

    print("Status      :", result.metadata.status)

    print("Pages       :", result.metadata.total_pages)

    print("Warnings    :", result.warnings)

    print("Processor   :", result.processed_document.processor)

    print(
        "Time (ms)   :",
        result.processing_time_ms,
    )


if __name__ == "__main__":
    main()