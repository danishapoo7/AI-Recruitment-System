from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from bson import ObjectId
from semantic_matching import semantic_match
from nlp import extract_text, extract_skills, extract_email, extract_name, extract_experience
from matching import match_resume_job
from database import resume_collection, interview_collection
from explainable import explain_match
from auth import users_collection, verify_password
import re
from jwt_handler import create_access_token, verify_token
from email_service import send_email
from datetime import datetime, timedelta
import random
from passlib.hash import bcrypt

app = FastAPI()
otp_storage = {}


# =========================
# MATCH + STORE CANDIDATE
# =========================
@app.post("/match")
async def match_candidate(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        resume_text = extract_text(file)

        # Debug check
        print("Resume text length:", len(resume_text))

        # =========================
        # Bias mitigation
        # =========================
        resume_text = resume_text.lower()

        resume_text = re.sub(
            r"\b(male|female|gender|age|religion|hindu|muslim|christian|married|single)\b",
            "",
            resume_text
        )

        # =========================
        # NLP Processing
        # =========================
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        matched = set(resume_skills).intersection(set(job_skills))

        skill_score = len(matched) / max(len(job_skills), 1)

        name = extract_name(resume_text)
        email = extract_email(resume_text)

        resume_exp = extract_experience(resume_text)
        job_exp = extract_experience(job_description)

        if job_exp == 0:
            exp_score = 0
        else:
            exp_score = min(resume_exp / job_exp, 1)

        # =========================
        # AI Matching
        # =========================
        tfidf_score = float(match_resume_job(resume_text, job_description))
        bert_score = float(semantic_match(resume_text, job_description))

        final_score = float(
            0.5 * bert_score +
            0.2 * tfidf_score +
            0.2 * skill_score +
            0.1 * exp_score
        )

        explanation = explain_match(resume_skills, job_description)

        resume_data = {
            "name": name,
            "email": email,
            "resume_text": resume_text,
            "skills": resume_skills,
            "matched_skills": list(matched),
            "experience": resume_exp,
            "score": final_score,
            "status": "AI Recommended"
        }

        # =========================
        # PREVENT DUPLICATE RESUMES
        # =========================
        existing = resume_collection.find_one({"email": email})

        if existing:
            resume_collection.update_one(
                {"email": email},
                {
                    "$set": {
                        "resume_text": resume_text,
                        "skills": resume_skills,
                        "experience": resume_exp,
                        "score": final_score
                    }
                }
            )

            return {
                "message": "Candidate already exists. Updated.",
                "id": str(existing["_id"]),
                "score": final_score,
                "skills": resume_skills,
                "matched_skills": list(matched),
                "explanation": explanation
            }

        # =========================
        # INSERT NEW CANDIDATE
        # =========================
        result = resume_collection.insert_one(resume_data)

        return {
            "message": "Candidate inserted",
            "id": str(result.inserted_id),
            "score": final_score,
            "skills": resume_skills,
            "matched_skills": list(matched),
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# GET RANKED CANDIDATES
# =========================
@app.get("/ranked_candidates")
def get_ranked_candidates():
    try:
        candidates = list(
            resume_collection.find().sort("score", -1)
        )

        for c in candidates:
            c["_id"] = str(c["_id"])

        return candidates

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# DELETE ONE CANDIDATE
# =========================
@app.delete("/delete_candidate/{id}")
def delete_candidate(id: str, authorization: str = Header(...)):

    try:
        # Extract token
        token = authorization.split(" ")[1]

        # Verify JWT
        user = verify_token(token)

        # Role check
        if user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Not allowed")

        # Validate ID
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID")

        # Delete candidate
        result = resume_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Candidate not found")

        return {"message": "Deleted"}

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


# =========================
# CLEAR ALL
# =========================
@app.delete("/clear_all")
def clear_all():
    result = resume_collection.delete_many({})
    return {
        "message": "All removed",
        "count": result.deleted_count
    }


# =========================
# SEARCH
# =========================
@app.get("/search_candidates")
def search_candidates(skill: str):
    try:
        results = list(
            resume_collection.find(
                {"skills": {"$regex": skill, "$options": "i"}}
            ).sort("score", -1)
        )

        for r in results:
            r["_id"] = str(r["_id"])

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# RECOMMENDATION
# =========================
@app.get("/recommend_candidates")
def recommend_candidates(limit: int = 5):
    candidates = list(
        resume_collection.find().sort("score", -1).limit(limit)
    )

    for c in candidates:
        c["_id"] = str(c["_id"])

    return candidates


# =========================
# ANALYTICS
# =========================
@app.get("/analytics")
def analytics():

    candidates = list(resume_collection.find())

    total = len(candidates)

    skill_count = {}
    scores = []

    for c in candidates:
        scores.append(c.get("score", 0))

        for skill in c.get("skills", []):
            skill_count[skill] = skill_count.get(skill, 0) + 1

    return {
        "total_candidates": total,
        "skill_distribution": skill_count,
        "scores": scores
    }


# =========================
# LOGIN
# =========================
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    user = users_collection.find_one({"username": username})

    if user and verify_password(password, user["password"]):

        token = create_access_token({
            "username": username,
            "role": user["role"]
        })

        return {
            "access_token": token,
            "role": user["role"]
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/schedule_interview/{id}")
def schedule_interview(
    id: str,
    date: str = Form(...),
    time: str = Form(...)
):
    try:
        # Save interview
        interview_collection.insert_one({
            "candidate_id": id,
            "date": date,
            "time": time,
            "status": "Scheduled"
        })

        # 🔐 Get candidate details
        candidate = resume_collection.find_one({"_id": ObjectId(id)})

        # 📧 Send email notification
        if candidate and candidate.get("email"):

            send_email(
                candidate["email"],
                "Interview Invitation",
                f"""
                Dear {candidate.get("name", "Candidate")},

                You are invited for an interview.

                Date: {date}
                Time: {time}

                Please attend on time.

                Regards,
                HR Team
                """
            )

        return {"message": "Interview scheduled and email sent"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# =========================
# GET INTERVIEW DETAILS
# =========================
@app.get("/interview/{candidate_id}")
def get_interview(candidate_id: str):

    interview = interview_collection.find_one(
        {"candidate_id": candidate_id}
    )

    if interview:
        interview["_id"] = str(interview["_id"])
        return interview

    return {}


# =========================
# REMINDER SYSTEM
# =========================
@app.get("/send_reminders")
def send_reminders():

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    interviews = list(
        interview_collection.find({"date": tomorrow})
    )

    sent = 0

    for interview in interviews:
        candidate = resume_collection.find_one(
            {"_id": ObjectId(interview["candidate_id"])}
        )

        if candidate and candidate.get("email"):

            send_email(
                candidate["email"],
                "Interview Reminder",
                f"""
                Dear {candidate.get("name")},

                Reminder: Your interview is tomorrow.

                Date: {interview["date"]}
                Time: {interview["time"]}

                Best of luck!

                HR Team
                """
            )
            sent += 1

    return {"message": f"{sent} reminders sent"}

# =========================
# UPCOMING INTERVIEWS
# =========================
@app.get("/upcoming_interviews")
def upcoming_interviews():

    today = datetime.now().strftime("%Y-%m-%d")

    interviews = list(
        interview_collection.find({"date": {"$gte": today}})
    )

    data = []

    for i in interviews:
        candidate = resume_collection.find_one(
            {"_id": ObjectId(i["candidate_id"])}
        )

        if candidate:
            data.append({
                "name": candidate.get("name"),
                "email": candidate.get("email"),
                "date": i.get("date"),
                "time": i.get("time"),
            })

    return data

# =========================
# RECRUITER SIGNUP
# =========================
from passlib.hash import bcrypt

@app.post("/signup")
def recruiter_signup(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...)
):

    # Check existing user
    existing = users_collection.find_one({"username": username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password
    hashed_password = bcrypt.hash(password)

    # Save recruiter
    users_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "email": email,
        "role": "recruiter"
    })

    return {"message": "Recruiter registered successfully"}

import random

# =========================
# FORGOT PASSWORD - SEND OTP
# =========================
@app.post("/forgot_password")
def forgot_password(email: str = Form(...)):

    user = users_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate OTP
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    # Send email
    send_email(
        email,
        "Password Reset OTP",
        f"Your OTP is: {otp}"
    )

    return {"message": "OTP sent"}

# =========================
# VERIFY OTP
# =========================
@app.post("/verify_otp")
def verify_otp(email: str = Form(...), otp: str = Form(...)):

    if otp_storage.get(email) == otp:
        return {"message": "OTP verified"}

    raise HTTPException(status_code=400, detail="Invalid OTP")

# =========================
# RESET PASSWORD
# =========================
@app.post("/reset_password")
def reset_password(
    email: str = Form(...),
    new_password: str = Form(...)
):

    hashed = bcrypt.hash(new_password)

    users_collection.update_one(
        {"email": email},
        {"$set": {"password": hashed}}
    )

    # Remove OTP
    otp_storage.pop(email, None)

    return {"message": "Password reset successful"}

# =========================
# UPDATE STATUS
# =========================

@app.post("/update_status/{candidate_id}")
def update_status(candidate_id: str, status: str = Form(...)):

    result = resume_collection.update_one(
        {"_id": ObjectId(candidate_id)},
        {"$set": {"status": status}}
    )

    if result.modified_count == 1:
        return {"message": "Status updated"}
    else:
        return {"message": "No change"}