import streamlit as st
from generator import generate_answer

# ---- Page config ----
st.set_page_config(
    page_title="PDF Study Assistant (RAG)",
    page_icon="📚",
    layout="centered"
)
# ---- Sidebar ----
with st.sidebar:
    st.header("About")
    st.write(
        "This is a Retrieval-Augmented Generation (RAG) app built from scratch "
        "using LangChain, ChromaDB, and Google's Gemini API."
    )
    st.write(
        "It answers questions using **only** the content of an AI/ML "
        "interview prep PDF (50 curated Q&As) — not the model's general knowledge."
    )
    st.markdown("---")
    st.write("**Tech stack:**")
    st.write("- LangChain\n- ChromaDB (local vector store)\n- Gemini Embeddings\n- Gemini 2.5 Flash-Lite\n- Streamlit")

# ---- Main UI ----
st.title("📚 PDF Study Assistant")
st.write("Ask a question about ML fundamentals, deep learning, NLP/LLMs, MLOps, or interview prep.")

# Text input for the question
question = st.text_input(
    "Your question:",
    placeholder="e.g. What is the difference between bagging and boosting?"
)

# Number of chunks to retrieve (exposed as a slider for demo/interview purposes)
k = st.slider("Number of context chunks to retrieve (k)", min_value=1, max_value=8, value=4)

if st.button("Get Answer") and question.strip():
    with st.spinner("Retrieving relevant context and generating answer..."):
        try:
            result = generate_answer(question, k=k)

            st.markdown("### Answer")
            st.write(result["answer"])

            with st.expander("View source chunks used"):
                for i, doc in enumerate(result["sources"]):
                    page = doc.metadata.get("page_label", "unknown")
                    st.markdown(f"**Source {i+1} (page {page})**")
                    st.write(doc.page_content)
                    st.markdown("---")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

elif question.strip() == "" and st.session_state.get("clicked_once"):
    st.warning("Please enter a question first.")