from datetime import datetime

from models import (
    DocumentMetadata,
    DocumentType,
    ProcessedDocument,
    ProcessedPage,
)

metadata = DocumentMetadata(
    document_id="123",
    file_name="sample.pdf",
    stored_name="123.pdf",
    file_path="data/uploads/123.pdf",
    file_type=DocumentType.PDF,
    sha256="a" * 64,
    file_size=100,
    uploaded_at=datetime.now(),
)

document = ProcessedDocument(
    metadata=metadata,
    pages=[
        ProcessedPage(
            page_number=1,
            text="Hello World",
        )
    ],
    processor="PDFProcessor",
)

print(document.processor)
print(document.extracted_at)
print(document.warnings)