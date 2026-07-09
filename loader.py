from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_pdf(pdf_path: str, chunk_size: int = 800, chunk_overlap: int = 150):
    # Step 1: Load the PDF. PyPDFLoader reads it page by page.
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()  # returns one Document object per PDF page
    print(f"Loaded PDF with {len(pages)} pages.")

    # Step 2: Split the pages into smaller overlapping chunks.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(pages)

    print(f"Split into {len(chunks)} chunks.")

    return chunks

if __name__ == "__main__":
    test_path = "ai_ml_interview_qa.pdf"
    chunks = load_and_chunk_pdf(test_path)

    # Print the first chunk so we can visually check it looks correct
    print("\n--- Sample Chunk 0 ---")
    print(chunks[0].page_content)
    print("\nMetadata:", chunks[0].metadata)