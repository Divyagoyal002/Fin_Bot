import os
import re
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("api_key")

# Set Google API Key explicitly
os.environ["Gemini_API_KEY"] = API_KEY

def extract_metadata(text):
    """Auto-detects finance-related data (e.g., loans, amounts, credit scores)."""
    metadata = {}

    loan_types = ["Home Loan", "Personal Loan", "Business Loan", "Credit Card", "Auto Loan"]
    for loan in loan_types:
        if re.search(rf"\b{loan}\b", text, re.IGNORECASE):
            metadata["Loan Type"] = loan

    amount_match = re.search(r"₹?(\d{1,3}(,\d{3})*(\.\d{1,2})?)", text)
    if amount_match:
        metadata["Amount"] = amount_match.group(0)

    return metadata

def create_vector_store(chunks, faiss_path):
    """Creates a FAISS vector store for a specific document and saves it."""
    if not chunks:
        raise ValueError("No chunks were provided to create the vector store.")

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=API_KEY
    )

    metadatas = [extract_metadata(chunk) for chunk in chunks]

    # Optional: ensure metadatas and chunks are the same length
    if len(metadatas) != len(chunks):
        raise ValueError("Mismatch between number of chunks and metadata entries.")

    # Optional: check if embeddings are being returned
    try:
        # This will throw if something is wrong with the model
        embeddings = embedding_model.embed_documents(chunks)
        if not embeddings:
            raise ValueError("Embedding model returned no vectors.")
    except Exception as e:
        raise RuntimeError(f"Failed to generate embeddings: {e}")

    # If all checks pass, proceed to create vector store
    vectorstore = FAISS.from_texts(chunks, embedding_model, metadatas=metadatas)
    vectorstore.save_local(faiss_path)
    return vectorstore


def load_vector_store(faiss_path):
    """Loads FAISS vector store for a specific document if it exists."""
    if os.path.exists(faiss_path):
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)
        return FAISS.load_local(faiss_path, embedding_model, allow_dangerous_deserialization=True)
    return None





