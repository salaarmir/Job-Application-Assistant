from utils.helpers import clean_latex

def tailor_coverletter(client: str, job_description: str, cover_letter_text: str) -> str:

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=4095,
        messages=[
            {
                "role": "user",
                "content":f"""You are an expert cover letter consultant helping tailor a cover letter to a specific job description.
Your task:
1. Keep all facts, experiences, and personal details EXACTLY as they are - do not invent anything
2. Rephrase and reorder content to mirror the language and priorities of the job description
3. Opening paragraph should directly reference what excites the candidate about this specific role/company
4. Middle paragraphs should emphasise the most relevant experience and skills for this role
5. Keep the same structure and length as the original cover letter
6. Tone should be professional but natural - not generic or robotic

Job Description:
{job_description}

Current Cover Letter (LaTeX):
{cover_letter_text}

Return ONLY raw LaTeX, no markdown, no backticks, no explanation."""
            }
        ]
    )
    return clean_latex(message.content[0].text)