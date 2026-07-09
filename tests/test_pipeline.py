from rag import (
    GeminiChatProvider,
    PromptBuilder,
    RAGPipeline,
    Retriever,
    VectorStore,
    GeminiEmbeddingProvider,
)

provider = GeminiEmbeddingProvider()

store = VectorStore()

retriever = Retriever(
    provider,
    store,
)

builder = PromptBuilder()

chat = GeminiChatProvider()

pipeline = RAGPipeline(
    retriever=retriever,
    prompt_builder=builder,
    chat_provider=chat,
)

response = pipeline.ask(
    "What is artificial intelligence?"
)

print("\n========== ANSWER ==========\n")

print(response.answer)

print("\n========== SOURCES ==========\n")

for source in response.sources:

    print(source.chunk_id)

    print(source.distance)

    print(source.metadata)

    print("-" * 50)