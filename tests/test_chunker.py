from datetime import datetime

from models import (
    DocumentMetadata,
    DocumentType,
    ProcessedDocument,
    ProcessedPage,
)
from rag import Chunker


metadata = DocumentMetadata(
    document_id="doc123",
    file_name="sample.txt",
    stored_name="sample.txt",
    file_path="sample.txt",
    file_type=DocumentType.TXT,
    sha256="a" * 64,
    file_size=100,
    uploaded_at=datetime.now(),
)

document = ProcessedDocument(
    metadata=metadata,
    pages=[
        ProcessedPage(
            page_number=1,
            text="A" * 2500,
        )
    ],
    processor="TXTProcessor",
)

chunker = Chunker(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = chunker.chunk_document(document)

print(f"Chunks: {len(chunks)}")

for chunk in chunks:
    print(
        chunk.chunk_id,
        chunk.start_char,
        chunk.end_char,
    )