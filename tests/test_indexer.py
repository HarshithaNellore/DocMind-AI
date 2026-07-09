from datetime import datetime

from models import (
    DocumentChunk,
)
from rag import (
    GeminiEmbeddingProvider,
    Indexer,
    VectorStore,
)


provider = GeminiEmbeddingProvider()

store = VectorStore()

indexer = Indexer(
    provider,
    store,
)

chunk = DocumentChunk(
    chunk_id="index_test_0001",
    document_id="doc001",
    chunk_index=0,
    page_number=1,
    start_char=0,
    end_char=40,
    text="Deep learning uses neural networks.",
    metadata={},
)

count = indexer.index_document(
    [chunk]
)

print("Indexed:", count)

print("Vectors:", store.count())