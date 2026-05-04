def tailor_cv(client: str,job_description: str, cv_text: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=4095,
        messages=[
            {
                "role": "user",
                "content":f"""You are an expert CV consultant helping tailor a CV to a specific job description.

Your task:
1. Keep all facts, dates, and experiences EXACTLY as they are - do not invent or exaggerate anything
2. Rewrite bullet points to use keywords and language from the job description where it genuinely fits
3. Reorder bullet points to put the most relevant ones first
4. Rewrite the profile summary to mirror the job's priorities - keep it to 3 lines maximum
5. Do NOT add skills or experience the candidate doesn't have
6. Industry experience: maximum 4 bullet points, each one line only
7. Each project: exactly 2 bullet points, one line each
8. Skills section: keep exactly as is, do not expand it
9. Profile summary: 3 lines maximum

IMPORTANT: Be ruthlessly concise. Every bullet point must be a single line.
Return ONLY raw LaTeX, no markdown, no backticks, no explanation.

Job Description:
{job_description}

Current CV (LaTeX):
{cv_text}

Return the full rewritten LaTeX CV. Only change wording, ordering, and emphasis - not facts."""
            }
        ]
    )
    return message.content[0].text