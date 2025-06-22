# import fitz  # PyMuPDF
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# def extract_text_from_pdf(pdf_path):
#     """Extracts text from a PDF file."""
#     doc = fitz.open(pdf_path)
#     return "\n".join([page.get_text("text") for page in doc])

# def chunk_text(text, chunk_size=1000, overlap=200):
#     """Splits text into chunks for better retrieval."""
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
#     return text_splitter.split_text(text)


import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
import os

def is_scanned_pdf(pdf_path):
    """Detects whether a PDF is likely scanned (i.e., no extractable text)."""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text and text.strip():
                return False  # Has extractable text
    except Exception as e:
        print(f"Error during scanned check: {e}")
    return True  # No extractable text or failed parsing

def extract_text_from_regular_pdf(pdf_path):
    """Extracts text from a regular (non-scanned) PDF using PyMuPDF."""
    print("Extracting text using PyMuPDF...")
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text("text") for page in doc])

def extract_text_from_scanned_pdf(pdf_path):
    """Extracts text from a scanned PDF using OCR (Tesseract)."""
    print("Scanned PDF detected. Performing OCR...")
    images = convert_from_path(pdf_path)
    full_text = ""
    for idx, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        full_text += f"\n\n--- Page {idx + 1} ---\n{text}"
    return full_text

def extract_text_from_pdf(pdf_path):
    """Unified function that chooses the right method for text extraction."""
    if is_scanned_pdf(pdf_path):
        return extract_text_from_scanned_pdf(pdf_path)
    else:
        return extract_text_from_regular_pdf(pdf_path)

def chunk_text(text, chunk_size=1000, overlap=200):
    """Splits text into chunks for better retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return text_splitter.split_text(text)
