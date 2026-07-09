from models import RetrievedChunk
from rag.prompt_builder import PromptBuilder

builder = PromptBuilder()

chunks = [
    RetrievedChunk(
        chunk_id="c1",
        text="Artificial intelligence enables machines to perform tasks that normally require human intelligence.",
        metadata={
            "page": 1,
        },
        distance=0.15,
    ),
    RetrievedChunk(
        chunk_id="c2",
        text="Machine learning is a subset of artificial intelligence.",
        metadata={
            "page": 2,
        },
        distance=0.22,
    ),
]

prompt = builder.build(
    question="What is artificial intelligence?",
    chunks=chunks,
)

print(prompt)