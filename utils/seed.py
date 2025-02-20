# utils/seed.py
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.database import AsyncSessionLocal as async_session
from repositories import UserRepositories
from utils import hash

data = [{
    "username": "admin",
    "email": "admin@admin.com",
    "password": "adminadmin",
    "role": "admin",
    "is_active": True,
}]
async def seed_db():  # Remove Depends(get_db)
    async with async_session() as db:  # Get session directly
        user_reps = UserRepositories(db)
        for user in data:
            # Fix logic: Check if user DOES NOT exist
            if not (await user_reps.get_by_email(user["email"]) or await user_reps.get_by_username(user["username"])):
                hash_password = hash.get_hash_password(user["password"])
                await user_reps.create({
                    "username": user["username"],
                    "email": user["email"],
                    "password_hash": hash_password,
                    "role": user["role"],
                    "is_active": user["is_active"]
                })
                print(f"Seeded user: {user['username']}")
            else:
                print(f"User exists: {user['username']}")