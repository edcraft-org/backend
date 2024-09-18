from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

class User(Document):
    id: Optional[PydanticObjectId] = Field(None, alias="_id", description="The unique identifier of the user")
    name: str
    email: str
    role: str

    class Settings:
        name = "users"

class UserCreate(BaseModel):
    name: str = Field(..., description="The name of the user")
    email: str = Field(..., description="The email of the user")
    role: str = Field(..., description="The role of the user")
