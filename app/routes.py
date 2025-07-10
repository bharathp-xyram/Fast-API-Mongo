from fastapi import APIRouter, HTTPException
from app.models import User, UpdateUser
from app.database import user_collection
from bson import ObjectId

router = APIRouter()

# Helper to convert ObjectId to string
def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user

@router.post("/users/")
def create_user(user: User):
    result = user_collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}

@router.get("/users/")
def get_users():
    users = user_collection.find()
    return [serialize_user(u) for u in users]

@router.get("/users/{user_id}")
def get_user(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return serialize_user(user)
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}")
def update_user(user_id: str, user: UpdateUser):
    result = user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {k: v for k, v in user.dict().items() if v is not None}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or not updated")
    return {"message": "User updated"}

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}