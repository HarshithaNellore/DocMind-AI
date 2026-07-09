"""
Integration test for the dependency container.
"""

from services import ServiceContainer


container = ServiceContainer()

print()

print("DocumentManager:", type(container.document_manager).__name__)

print("Chunker:", type(container.chunker).__name__)

print("Indexer:", type(container.indexer).__name__)

print("Retriever:", type(container.retriever).__name__)

print("Pipeline:", type(container.pipeline).__name__)

print()

print(
    "Vector count:",
    container.vector_store.count(),
)