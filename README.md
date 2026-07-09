# 📚 DocMind AI – RAG-Powered PDF Question Answering Assistant

> An end-to-end **Retrieval-Augmented Generation (RAG)** application that enables users to ask natural language questions about a PDF and receive answers grounded **only** in the document's content.

Built from scratch to demonstrate a complete RAG pipeline including **document ingestion, text chunking, semantic embeddings, vector search, prompt engineering, and grounded response generation** using **Google Gemini**, **LangChain**, and **ChromaDB**.

---

## 🚀 Features

- 📄 Ask questions about any PDF
- 🔍 Semantic search using vector embeddings
- 🧠 Grounded answers generated only from retrieved document context
- 🚫 Hallucination reduction through prompt engineering
- ⚡ Local ChromaDB vector database
- 🎛 Adjustable retrieval depth (Top-K)
- 🏗 Modular architecture for easy extension

---

## 🎥 Demo

![DocMind AI Demo](Sample_image.png)

### Example

**Question**

> What is the difference between Bagging and Boosting?

**Answer**

> Bagging trains multiple models independently on bootstrapped datasets and combines their predictions to reduce variance. Boosting trains models sequentially, where each model focuses on correcting errors made by previous models, reducing bias.

If a question is outside the uploaded document, the assistant responds with:

> *"I don't have enough information in the document to answer that."*

This ensures answers remain grounded in the provided context rather than relying on the model's general knowledge.

---

# ✨ Why I Built This

Large Language Models are powerful, but they often hallucinate when answering domain-specific questions.

This project was built to understand the internal workings of **Retrieval-Augmented Generation (RAG)** by implementing each stage of the pipeline from scratch instead of relying on black-box frameworks.

The primary goal was to build a modular architecture where every stage—from retrieval to generation—can be independently replaced or upgraded.

---

# 🧠 RAG Pipeline

```
                     PDF Document
                           │
                           ▼
                Document Loader (PyPDF)
                           │
                           ▼
          Recursive Character Text Splitter
                           │
                           ▼
         Gemini Embedding Model (Vectors)
                           │
                           ▼
                     ChromaDB
                           ▲
                           │
User Question ─► Embedding ─► Similarity Search
                           │
                           ▼
              Relevant Document Chunks
                           │
                           ▼
           Prompt + Retrieved Context
                           │
                           ▼
          Gemini 2.5 Flash Lite LLM
                           │
                           ▼
                Grounded Final Answer
```

The system follows the standard **two-stage Retrieval-Augmented Generation architecture**:

1. **Retrieval**
   - Split document into chunks
   - Convert chunks into embeddings
   - Store embeddings inside ChromaDB
   - Retrieve the most relevant chunks using semantic similarity

2. **Generation**
   - Combine retrieved chunks with the user's query
   - Send them to Gemini
   - Generate an answer using only the supplied context

---

# 🏗 Project Structure

```
DocMind-AI/
│
├── app.py                  # Streamlit UI
├── loader.py               # PDF loading & chunking
├── embedder.py             # Embedding generation & ChromaDB creation
├── retriever.py            # Semantic similarity search
├── generator.py            # Prompt construction & answer generation
├── requirements.txt
├── README.md
├── .env.example
└── Sample_image.png
```

Each component is isolated to make the system modular and extensible.

---

# ⚙️ Tech Stack

| Component | Technology |
|------------|------------|
| Language | Python |
| UI | Streamlit |
| LLM | Google Gemini 2.5 Flash Lite |
| Embedding Model | Gemini Embedding-001 |
| Framework | LangChain |
| Vector Database | ChromaDB |
| PDF Processing | PyPDF |
| Environment Management | Python Dotenv |

---

# 💡 Skills Demonstrated

- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Semantic Search
- Vector Embeddings
- ChromaDB
- LangChain
- Google Gemini API
- Streamlit
- Python
- Modular Software Design

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/<YOUR_USERNAME>/DocMind-AI.git
cd DocMind-AI
```

---

## 2. Create a virtual environment

Using **uv**

```bash
uv venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

You can obtain a free API key from Google AI Studio.

---

## 5. Add your PDF

Place your PDF inside the project directory.

By default the project expects

```
ai_ml_interview_qa.pdf
```

Update the filename inside `loader.py` if using a different document.

---

## 6. Build the Vector Database

Run once whenever the PDF changes.

```bash
uv run python embedder.py
```

This creates a local

```
chroma_db/
```

directory.

---

## 7. Start the Application

```bash
uv run streamlit run app.py
```

Visit

```
Local URL : http://localhost:8501
Network URL: http://192.168.0.106:8501
```

---

# 🎯 Design Decisions

### Chunk Size

- chunk_size = **800**
- chunk_overlap = **150**

Maintains semantic continuity while avoiding oversized chunks.

---

### Low Temperature

Generation temperature = **0.2**

Produces more factual and deterministic answers.

---

### Hallucination Prevention

The prompt explicitly instructs Gemini to answer only from the retrieved context.

If sufficient information isn't found, the assistant returns

> "I don't know based on the provided document."

---

### Adjustable Retrieval

Users can modify **Top-K retrieval** directly from the interface to observe how retrieval breadth affects answer quality.

---

### Modular Design

Retrieval and generation are completely decoupled.

This allows replacing

- Gemini → OpenAI
- ChromaDB → Pinecone
- ChromaDB → FAISS

without affecting other components.

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ If you found this project useful

Please consider giving it a ⭐ on GitHub.