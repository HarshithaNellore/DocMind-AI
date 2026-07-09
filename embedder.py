import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

from loader import load_and_chunk_pdf

# Load environment variables (GOOGLE_API_KEY) from .env
load_dotenv()

PERSIST_DIRECTORY = "chroma_db"  # folder where ChromaDB will save its data
COLLECTION_NAME = "pdf_study_assistant"


def get_embedding_model():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
def build_vector_store(chunks, persist_directory=PERSIST_DIRECTORY):
    embedding_model = get_embedding_model()

    print(f"Embedding {len(chunks)} chunks... (this calls the Gemini API)")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=persist_directory
    )

    print(f"Vector store built and saved to '{persist_directory}/'")

    return vector_store


def load_existing_vector_store(persist_directory=PERSIST_DIRECTORY):
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )

    return vector_store


if __name__ == "__main__":
    pdf_path = "ai_ml_interview_qa.pdf"  
    chunks = load_and_chunk_pdf(pdf_path)
    vector_store = build_vector_store(chunks)

    # Quick sanity check: run a similarity search directly
    results = vector_store.similarity_search("What is bias-variance tradeoff?", k=2)

    print("\n--- Sanity Check: Top 2 Similar Chunks ---")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:")
        print(doc.page_content[:200], "...")