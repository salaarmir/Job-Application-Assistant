# Job Application Assistant

A web-based tool that tailors your CV and cover letter to a specific job description using Claude AI, and exports them as PDFs.

## Features

- Paste a job description and generate a tailored LaTeX CV and cover letter
- Preview both documents as PDFs directly in the browser
- Download each document as a named PDF (e.g. `Salaar_Mir_CV_CompanyName.pdf`)

## Stack

- **Frontend:** HTML/CSS/JavaScript
- **Backend:** Python, FastAPI
- **AI:** Anthropic Claude API
- **PDF Generation:** pdflatex (TeX Live)

## Setup

1. Install dependencies:
```bash
   pip install fastapi uvicorn anthropic python-multipart
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

1. Enter the company name and paste the job description
2. Click **Generate Documents** to tailor the CV and cover letter
3. Click **Preview PDF** to render either document
4. Click **Download PDF** to save it locally
