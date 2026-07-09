from datetime import datetime

from models import (
    DocumentChunk,
)
from rag.embeddings import GeminiEmbeddingProvider

provider = GeminiEmbeddingProvider()

chunk = DocumentChunk(
    chunk_id="chunk_0001",
    document_id="doc001",
    chunk_index=0,
    page_number=1,
    start_char=0,
    end_char=40,
    text="Machine learning enables computers to learn from data.",
    metadata={},
)

embedded = provider.embed_chunks([chunk])

print(len(embedded))

print(len(embedded[0].embedding))

print(type(embedded[0].embedding[0]))