from auth import users_collection, hash_password

users_collection.insert_one({
    "username": "admin",
    "password": hash_password("admin123"),
    "role": "admin"
})