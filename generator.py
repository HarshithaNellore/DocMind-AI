import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from retriever import retrieve_relevant_chunks

load_dotenv()

PROMPT_TEMPLATE = """You are a helpful study assistant answering questions
based ONLY on the provided context from an AI/ML interview prep document.

Rules:
- Answer using only the information in the context below.
- If the context doesn't contain enough information to answer,
  say "I don't have enough information in the document to answer that."
- Keep answers clear and concise, as if explaining to someone studying for an interview.

Context:
{context}

Question: {question}

Answer:"""


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2  # low temperature = more focused, less "creative" answers
    )


def generate_answer(question: str, k: int = 4):
    # Step 1: Retrieve relevant chunks
    chunks = retrieve_relevant_chunks(question, k=k)

    # Step 2: Combine chunk text into one context block
    context = "\n\n---\n\n".join([doc.page_content for doc in chunks])

    # Step 3: Build the final prompt
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    # Step 4: Call Gemini
    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": chunks
    }


# ---- Quick standalone test ----
if __name__ == "__main__":
    test_question = "What is the difference between bagging and boosting?"

    result = generate_answer(test_question)

    print(f"Question: {test_question}\n")
    print(f"Answer:\n{result['answer']}\n")

    print("--- Sources used ---")
    for i, doc in enumerate(result["sources"]):
        print(f"Source {i+1} (page {doc.metadata.get('page_label')}): {doc.page_content[:100]}...")