# Job Application Assistant

An end-to-end AI-powered tool that tailors CVs and cover letters to specific job descriptions using Claude AI, with a RAG pipeline that grounds outputs in your real academic and professional background.

## Overview

Most CV tools do generic rewording. This tool automatically retrieves the most relevant parts of your uploaded academic documents and injects them as grounded context when generating tailored CVs and cover letters — producing outputs that reference your actual work rather than hallucinated achievements.

## Features

- Paste a job description and generate a tailored LaTeX CV and cover letter
- RAG pipeline over uploaded academic documents (papers, thesis, reports) using ChromaDB and sentence-transformers
- Preview both documents as PDFs directly in the browser before downloading
- Download each document as a named PDF (e.g. `Salaar_Mir_CV_CompanyName.pdf`)
- Document management UI — upload, view, and delete documents from the vector store
- Slide-in sidebar for document management
- Persistent vector store that survives server restarts

## Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **AI:** Anthropic Claude API (claude-haiku-4-5)
- **RAG:** ChromaDB, sentence-transformers
- **PDF Generation:** pdflatex (TeX Live)
- **Infrastructure:** Raspberry Pi 5, Tailscale

## Project Structure
```
job-application-assistant/
├── main.py              # FastAPI routes
├── backend.py           # RAG logic (ChromaDB, embeddings, ingestion)
├── utils/
│   ├── cv.py            # CV tailoring logic
│   ├── coverletter.py   # Cover letter generation logic
│   └── helpers.py       # Shared utilities
├── documents/           # Uploaded academic PDFs
├── chroma_db/           # Persistent ChromaDB vector store
├── tailored_documents/  # Generated LaTeX output files
├── pages/
│   └── rag.html         # Document upload and RAG management page
├── ui/                  # Static assets
└── index.html           # Main frontend
```

## Setup

1. Install Python dependencies:
```bash
   pip install fastapi uvicorn anthropic python-multipart chromadb sentence-transformers pypdf
```

2. Install pdflatex:
```bash
   sudo apt install texlive texlive-latex-extra
```

3. Add your Anthropic API key as an environment variable:
```bash
   export ANTHROPIC_API_KEY=your_key_here
```

4. Run the server:
```bash
   uvicorn main:app --reload
```

5. Open `index.html` in your browser.

## Usage

1. Upload your academic documents (thesis, papers, reports) via the sidebar
2. Enter the company name and paste the job description
3. Click **Generate Documents** to tailor the CV and cover letter
4. Click **Preview PDF** to render either document inline
5. Click **Download PDF** to save locally

## How the RAG Works

Uploaded PDFs are extracted, chunked by paragraph, embedded using a local sentence-transformers model, and stored in a persistent ChromaDB collection. When generating documents, the job description is embedded and used to query ChromaDB for the most semantically relevant chunks. These are injected into the Claude prompt as grounded context, allowing the model to reference specific technical details, methodologies, and achievements from your actual work.

## Planned Features

- Application tracker (company, JD, CV version, status, follow-up dates)
- Interview prep mode — generate likely questions and draft answers grounded in your documents
- Follow-up and thank you email generation
- Multi-user support with authentication
- Hosted web version

## Infrastructure

The application runs on a Raspberry Pi 5 (8GB) accessed remotely via Tailscale, with uvicorn kept alive using tmux.
