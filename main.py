import anthropic
import os
from dotenv import load_dotenv
from cv import tailor_cv
from coverletter import tailor_coverletter
from fastapi import FastAPI
from fastapi import Form
from fastapi.responses import FileResponse
import zipfile


load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = FastAPI()

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/create_documents")
def create_documents(
    company_name: str = Form(...),
    job_description: str = Form(...)

):

    with open("example_cv.tex", "r") as f:
        cv_text = f.read()

    with open("example_coverletter.tex", "r") as f:
        cover_letter_text = f.read()

    tailored_cv = tailor_cv(client, job_description, cv_text)
    tailored_cover_letter = tailor_coverletter(client, job_description, cover_letter_text)

    # Save CV to file instead of printing
    cv_file = f"Salaar_Mir_CV_{company_name}.tex"
    with open(cv_file, "w") as f:
        f.write(tailored_cv)
    
    print(f"Done! Saved to {cv_file}")

    # Save cover letter to file instead of printing
    cl_file = f"Salaar_Mir_CoverLetter_{company_name}.tex"
    with open(cl_file, "w") as f:
        f.write(tailored_cover_letter)
    
    print(f"Done! Saved to {cl_file}")

    zip_filename = f"Salaar_Mir_{company_name}.zip"

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(cv_file)
        zipf.write(cl_file)
    
    return FileResponse(

    path=zip_filename,
    media_type="application/zip",
    filename=zip_filename
    )

