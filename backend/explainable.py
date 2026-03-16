from nlp import extract_skills

def explain_match(candidate_skills, job_text):
    # Extract job skills using same NLP
    job_skills = extract_skills(job_text)

    matched = []
    missing = []

    for skill in candidate_skills:
        if skill in job_skills:
            matched.append(skill)

    for skill in job_skills:
        if skill not in candidate_skills:
            missing.append(skill)

    return {
        "matched_skills": matched,
        "missing_skills": missing
    }