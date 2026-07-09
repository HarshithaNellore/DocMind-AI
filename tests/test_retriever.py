from rag import (
    GeminiEmbeddingProvider,
    Retriever,
    VectorStore,
)

provider = GeminiEmbeddingProvider()

store = VectorStore()

retriever = Retriever(
    provider,
    store,
)

results = retriever.retrieve(
    "What is artificial intelligence?"
)

print()

print("Retrieved:", len(results))

print()

for result in results:

    print(result["id"])

    print(result["distance"])

    print(result["text"][:80])

    print("-" * 50)