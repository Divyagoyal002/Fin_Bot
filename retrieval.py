def retrieve_relevant_chunks(query, vectorstore, top_k=25):
    """Finds the most relevant document sections."""
    return vectorstore.similarity_search(query, k=top_k)
