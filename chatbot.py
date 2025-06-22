import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("api_key")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def query_llm(chunks, user_query):
    """Uses Gemini API to answer based on extracted finance document content."""
    context = "\n\n".join([doc.page_content for doc in chunks])

    prompt = f"""
    You are analyzing a financial document (e.g., CIBIL report, loan statement). 
    Answer ONLY based on the provided content.
    
    Query: {user_query}
    Document Context:
    {context}

    If you cannot find the answer, respond with: "I could not find that information in the document."
    """

    response = model.generate_content(prompt)
    return response.text.strip()
