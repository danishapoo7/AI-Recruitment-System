from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["ai_recruitment"]
resume_collection = db["resumes"]
interview_collection = db["interviews"]