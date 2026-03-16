from auth import users_collection, hash_password

users_collection.insert_one({
    "username": "recruiter",
    "password": hash_password("recruiter123"),
    "role": "recruiter"
})
