from datetime import datetime

from models import (
    DocumentMetadata,
    DocumentStatus,
    DocumentType,
)

doc = DocumentMetadata(
    document_id="123",
    file_name="paper.pdf",
    stored_name="abc123.pdf",
    file_path="data/uploads/abc123.pdf",
    file_type=DocumentType.PDF,
    sha256="abcdef123456",
    file_size=1024,
    uploaded_at=datetime.now(),
)

print(doc)

print(doc.status == DocumentStatus.PENDING)