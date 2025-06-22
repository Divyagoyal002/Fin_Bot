
# RAG Chatbot for Fitnechd 

A Retrieval-Augmented Generation (RAG) chatbot designed for **Fitnechd** using vector-based semantic search to provide precise answers from PDF documents. Built using **FAISS**, **LangChain**, and **Google Generative AI embeddings**, this chatbot can parse PDFs, chunk data, index it semantically, and deliver context-aware responses.

---

## Features

- Extracts text from PDF files (even scanned ones via OCR)
- Splits and chunks large documents for efficient processing
- Uses **Google Generative AI Embeddings**
- Stores and retrieves vectors using **FAISS**
- Simple Streamlit UI to interact with the chatbot

---

## Tech Stack

- **Python**
- **LangChain**
- **FAISS (Facebook AI Similarity Search)**
- **Google Generative AI Embeddings**
- **PyMuPDF / PyPDF2 / pdf2image / pytesseract**
- **Streamlit**

---

## Project Structure

```

.
├── app.py                      # Main Streamlit application
├── document\_processing.py     # Handles PDF text extraction and chunking
├── vector\_storage.py          # Vector store creation and loading logic
├── retrieval.py               # Retrieves relevant chunks using FAISS
├── chatbot.py                 # Interfaces with the LLM for answers
├── .env                       # Environment variables (API keys, etc.)
└── README.md                  # This file

````

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/fitnechd-rag-chatbot.git
cd fitnechd-rag-chatbot
````

2. **Create a virtual environment and activate it:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up your `.env` file:**

```ini
GOOGLE_API_KEY=your_google_genai_api_key
```

---

##  How It Works

1. Upload PDF(s) via Streamlit.
2. The PDF text is extracted using a combination of:

   * `PyMuPDF` and `PyPDF2` for native PDFs
   * `pdf2image` + `pytesseract` for scanned PDFs
3. Text is chunked using LangChain's `RecursiveCharacterTextSplitter`.
4. Embeddings are generated using Google Generative AI.
5. Vectors are stored and queried using FAISS.
6. The LLM generates answers based on retrieved chunks.

---

## Run the Chatbot

```bash
streamlit run app.py
```

---

## Example Usage

Ask questions like:

* *"What is the onboarding process described in the document?"*
* *"Summarize the compliance section from page 5."*

---

##  Notes

* Ensure `Tesseract OCR` is installed and accessible in your system PATH for OCR support.
* FAISS indexes are stored locally for fast retrieval.
* Designed for internal use at **Fitnechd**; customize as per your organization's document types.

