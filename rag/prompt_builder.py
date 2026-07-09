"""
Prompt builder for the RAG pipeline.
"""

from __future__ import annotations

from models import RetrievedChunk


class PromptBuilder:
    """
    Builds prompts for the language model.
    """

    SYSTEM_PROMPT = """
You are DocMind AI.

Answer ONLY using the supplied context.

If the answer is not contained in the context,
reply that you do not know.

Always be concise and accurate.
""".strip()

    def build(
        self,
        question: str,
        chunks: list[RetrievedChunk],
    ) -> str:
        """
        Build a RAG prompt.
        """

        context = "\n\n".join(
            f"[Source {i + 1}]\n{chunk.text}"
            for i, chunk in enumerate(chunks)
        )

        return f"""
{self.SYSTEM_PROMPT}

======================
Context
======================

{context}

======================
Question
======================

{question}

======================
Answer
======================
""".strip()