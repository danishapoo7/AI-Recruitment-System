import spacy
from pdfminer.high_level import extract_text as pdf_text
import tempfile
from skills import skills_list
import re

nlp = spacy.load("en_core_web_sm")


def extract_text(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.file.read())
        text = pdf_text(tmp.name)
    return text


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))

def extract_email(text):
    email_pattern = r'\S+@\S+'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else "Not found"


def extract_name(text):
    lines = text.split("\n")
    for line in lines[:5]:  # usually name at top
        if len(line.split()) <= 4:
            return line.strip()
    return "Unknown"

def extract_experience(text):

    import re

    pattern = r'(\d+)\s+years'

    matches = re.findall(pattern, text.lower())

    if matches:
        years = [int(x) for x in matches]
        return max(years)

    return 0