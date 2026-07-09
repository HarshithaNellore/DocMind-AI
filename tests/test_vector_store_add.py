from datetime import datetime

from models import (
    DocumentChunk,
    EmbeddedChunk,
)
from rag.embeddings import GeminiEmbeddingProvider
from rag.vector_store import VectorStore


provider = GeminiEmbeddingProvider()

chunk = DocumentChunk(
    chunk_id="chunk_0001",
    document_id="doc001",
    chunk_index=0,
    page_number=1,
    start_char=0,
    end_char=20,
    text="Artificial intelligence is transforming software.",
    metadata={},
)

embedded = provider.embed_chunks([chunk])

store = VectorStore()

store.add_chunks(embedded)

print("Vectors:", store.count())