from rag.llm import GeminiChatProvider

provider = GeminiChatProvider()

response = provider.generate(
    """
Explain what Retrieval-Augmented Generation is
in one short paragraph.
"""
)

print("\nResponse:\n")
print(response)