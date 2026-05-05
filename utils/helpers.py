import re

def clean_latex(text):
    # Remove ```latex ... ``` or ``` ... ``` wrappers
    text = re.sub(r'^```(?:latex)?\s*', '', text.strip())
    text = re.sub(r'\s*```$', '', text.strip())
    return text.strip()