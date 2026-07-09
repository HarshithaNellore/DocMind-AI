from datetime import datetime

from models import (
    DocumentMetadata,
    DocumentType,
)
from repositories import MetadataRepository

repo = MetadataRepository()

doc = DocumentMetadata(
    document_id="1",
    file_name="paper.pdf",
    stored_name="paper.pdf",
    file_path="data/uploads/paper.pdf",
    file_type=DocumentType.PDF,
    sha256="abcdef",
    file_size=100,
    uploaded_at=datetime.now(),
)

repo.add(doc)

print(repo.get_all())

print(repo.get_by_id("1"))

print(repo.get_by_sha256("abcdef"))