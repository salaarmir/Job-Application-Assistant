import anthropic
import os
from dotenv import load_dotenv
from utils.cv import tailor_cv
from utils.coverletter import tailor_coverletter
from fastapi import FastAPI
from fastapi import Form, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import zipfile
import subprocess

from backend import ingest_document, get_documents, delete_file


load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/rag")
def RAG():
    return FileResponse("pages/rag.html")

@app.post("/create_documents")
def create_documents(
    company_name: str = Form(...),
    job_description: str = Form(...),
    user_prompts: str = Form("")
):

    with open("documents/example_cv.tex", "r") as f:
        cv_text = f.read()

    with open("documents/example_coverletter.tex", "r") as f:
        cover_letter_text = f.read()

    tailored_cv = tailor_cv(client, job_description, cv_text, user_prompts)
    tailored_cover_letter = tailor_coverletter(client, job_description, cover_letter_text, user_prompts)

    # Save CV to file instead of printing
    cv_file = f"tailored_documents/Salaar_Mir_CV_{company_name}.tex"
    with open(cv_file, "w") as f:
        f.write(tailored_cv)
    
    print(f"Done! Saved to {cv_file}")

    # Save cover letter to file instead of printing
    cl_file = f"tailored_documents/Salaar_Mir_CoverLetter_{company_name}.tex"
    with open(cl_file, "w") as f:
        f.write(tailored_cover_letter)
    
    print(f"Done! Saved to {cl_file}")

    return {
        "latex_cv": tailored_cv,
        "latex_cover_letter": tailored_cover_letter
      }

@app.post("/convert_to_pdf")
async def convert_to_pdf(latex_content: str = Form(...), filetype: str = Form(...), company_name: str = Form(...)):
    with open ("output.tex", "w") as f:
        f.write(latex_content)

    subprocess.run(["pdflatex", "output.tex"])

    if filetype == "cv":
        os.rename("output.pdf", f"Salaar_Mir_CV_{company_name}.pdf")
        return FileResponse(f"Salaar_Mir_CV_{company_name}.pdf", media_type="application/pdf", filename=f"Salaar_Mir_CV_{company_name}.pdf")
    else:
        os.rename("output.pdf", f"Salaar_Mir_CoverLetter_{company_name}.pdf")
        return FileResponse(f"Salaar_Mir_CoverLetter_{company_name}.pdf", media_type="application/pdf", filename=f"Salaar_Mir_CoverLetter_{company_name}.pdf")

@app.post("/upload_documents")
async def upload_documents(academic_file: UploadFile = File(...)):

    print(f"Received file: {academic_file.filename}")


    file_path = f"uploaded_documents/{academic_file.filename}"

    with open(file_path, "wb") as f:
        f.write(await academic_file.read())

    ingest_document(file_path=file_path, metadata={"filename": academic_file.filename})
    return {"message": "File uploaded and ingested successfully!"}

@app.get("/documents")
async def documents():
    return get_documents()

@app.delete("/delete_document/{filename}")
async def delete_document(filename: str):
    
    delete_file(filename=filename)
    return {"message": f"Document with filename {filename} deleted successfully!"}