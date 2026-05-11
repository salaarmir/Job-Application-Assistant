import chromadb
from pypdf import PdfReader
import re
import uuid
import os

# Create a persistent client that will store data in the specified directory
client = chromadb.PersistentClient(path="/home/salaarmir/Desktop/Projects/job-application-assistant/chroma_db")

# Create a collection for academic documents (if it doesn't already exist)
collection = client.get_or_create_collection(name="academic-documents")

MIN_CHUNK_SIZE = int(os.getenv("MIN_CHUNK_SIZE", 50))

def ingest_document(file_path: str, metadata: dict):

    # Create a unique ID for the document (you can use a hash of the file or a UUID)
    document_id = str(uuid.uuid4())

    document_text = ""

    # Read the PDF file and extract text (you can use libraries like PyPDF2 or pdfminer)
    with open(file_path, "rb") as f:
        pdf_text = PdfReader(f)  # Replace with actual text extraction logic

        for page in pdf_text.pages:
            document_text += page.extract_text()
            # Process the text as needed (e.g., clean it, split into chunks, etc.)

    chunks = chunk_document(document_text = document_text, min_chunk_size=MIN_CHUNK_SIZE)

    chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]

    # Add the document to the ChromaDB collection
    collection.add(
        ids=chunk_ids,
        documents=chunks,
        metadatas=[metadata] * len(chunks)
    )

    print("INGESTING:", file_path)
    print("TEXT LENGTH:", len(document_text))
    print("CHUNKS:", len(chunks))

def chunk_document(document_text: str, min_chunk_size: int = 50) -> list:

    paragraphs = re.split(r"\n\n", document_text)  # Split by paragraphs
    chunks = [p.strip() for p in paragraphs if len(p.strip()) >= min_chunk_size]  # Filter out short paragraphs

    return chunks

def get_documents():

    results = collection.get(include=["metadatas"])

    filenames = list(set(metadata["filename"] for metadata in results["metadatas"]))
    
    return {"filenames": filenames}

def delete_file(filename: str):

    collection = client.get_collection(name="academic-documents")
    collection.delete(where={"filename": filename})

def query_documents(query: str, top_k: int = 5):

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    return results

