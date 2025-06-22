import streamlit as st
import os
from document_processing import extract_text_from_pdf, chunk_text
from vector_storage import create_vector_store, load_vector_store
from retrieval import retrieve_relevant_chunks
from chatbot import query_llm

# Set up Streamlit app
st.set_page_config(page_title="Finance Document Chatbot", layout="wide")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# UI Header
st.title("📄 Finance Document Chatbot")
st.write("Upload a finance document (e.g., CIBIL report, loan statement) and ask questions!")

# Ensure temp storage exists
if not os.path.exists("temp_files"):
    os.makedirs("temp_files")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF Document", type=["pdf"])

if uploaded_file is not None:
    pdf_name = os.path.basename(uploaded_file.name).replace(".pdf", "")  # Get clean file name
    pdf_path = os.path.join("temp_files", uploaded_file.name)
    
    # Save the uploaded file
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"✅ Document '{uploaded_file.name}' uploaded! Processing...")

    # Define a FAISS index path unique to this document
    faiss_path = f"temp_files/faiss_index_{pdf_name}"

    # Check if a FAISS index already exists for this document
    vectorstore = load_vector_store(faiss_path)

    if vectorstore is None:  # If no existing FAISS index, create a new one
        text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(text)
        vectorstore = create_vector_store(chunks, faiss_path)
        st.success(f"✅ FAISS index created for '{uploaded_file.name}'!")

    st.success(f"✅ Document processed! You can now ask questions about '{uploaded_file.name}'.")

    # User Query
    user_query = st.text_input("Ask a question about the document:")

    if user_query:
        relevant_chunks = retrieve_relevant_chunks(user_query, vectorstore)
        response = query_llm(relevant_chunks, user_query)

        # Save chat history (Last 5 conversations)
        st.session_state.chat_history.append({"user": user_query, "bot": response})
        st.session_state.chat_history = st.session_state.chat_history[-5:]

    # Display Chat History
    st.subheader("🗨️ Chat History")
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**Bot:** {chat['bot']}")
        st.write("---")
