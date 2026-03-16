from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = None

def semantic_match(resume_text, job_text):

    global model

    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    sections = resume_text.split("\n")

    job_embedding = model.encode([job_text])[0]

    scores = []

    for sec in sections:

        sec = sec.strip()

        if len(sec) < 10:
            continue

        sec_embedding = model.encode([sec])[0]

        similarity = cosine_similarity(
            [sec_embedding], [job_embedding]
        )[0][0]

        scores.append(similarity)

    if len(scores) == 0:
        return 0

    return sum(scores) / len(scores)