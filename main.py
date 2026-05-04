import anthropic
import os
from dotenv import load_dotenv
from cv import tailor_cv
from coverletter import tailor_coverletter

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

if __name__ == "__main__":
    job_desc = input("Paste the job description (press Enter twice when done):\n")
    company = input("Enter the company name: ")
    
    # Load CV from file instead of pasting
    with open("cv.tex", "r") as f:
        cv = f.read()
    
    # Load cover letter from file instead of pasting
    with open("coverletter.tex", "r") as f:
        cover_letter = f.read()
    
    print("\nTailoring your CV...\n")
    tailored_cv = tailor_cv(client, job_desc, cv)

    print("Tailoring your cover letter...\n")
    tailored_cover_letter = tailor_coverletter(client, job_desc, cover_letter)
    
    # Save CV to file instead of printing
    output_file1 = f"Salaar_Mir_CV_{company}.tex"
    with open(output_file1, "w") as f:
        f.write(tailored_cv)
    
    print(f"Done! Saved to {output_file1}")

    # Save cover letter to file instead of printing
    output_file2 = f"Salaar_Mir_CoverLetter_{company}.tex"
    with open(output_file2, "w") as f:
        f.write(tailored_cover_letter)
    
    print(f"Done! Saved to {output_file2}")