# test_pdf_processor.py

from pathlib import Path
from datetime import datetime

from models import (
    DocumentMetadata,
    DocumentType,
)
from processors.pdf_processor import PDFProcessor

processor = PDFProcessor()

metadata = DocumentMetadata(
    document_id="123",
    file_name="sample.pdf",
    stored_name="sample.pdf",
    file_path="sample.pdf",
    file_type=DocumentType.PDF,
    sha256="a" * 64,
    file_size=100,
    uploaded_at=datetime.now(),
)

document = processor.process(
    Path("sample.pdf"),
    metadata,
)

print(document.processor)

print(len(document.pages))

print(document.warnings)