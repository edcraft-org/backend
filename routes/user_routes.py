from fastapi import APIRouter
from typing import List
from models.user import User, UserCreate

user_router = APIRouter()


@user_router.post("/", response_model=User)
async def add_user(user: UserCreate):
    new_user = User(**user.model_dump())
    await new_user.insert()
    return new_user


@user_router.get("/", response_model=List[User])
async def get_users():
    users = await User.find().to_list()
    return users
