from embedder import load_existing_vector_store


def retrieve_relevant_chunks(query: str, k: int = 4):
    vector_store = load_existing_vector_store()
    results = vector_store.similarity_search(query, k=k)

    return results

def retrieve_with_scores(query: str, k: int = 4):
    vector_store = load_existing_vector_store()
    results = vector_store.similarity_search_with_score(query, k=k)
    return results



if __name__ == "__main__":
    test_query = "What is the difference between bagging and boosting?"

    print(f"Query: {test_query}\n")

    results = retrieve_with_scores(test_query, k=3)

    for i, (doc, score) in enumerate(results):
        print(f"--- Result {i+1} (distance score: {score:.4f}) ---")
        print(doc.page_content[:250], "...")
        print(f"Source page: {doc.metadata.get('page_label')}\n")