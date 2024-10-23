from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional


class Project(Document):
    id: Optional[PydanticObjectId] = Field(None, alias="_id", description="The unique identifier of the project")
    title: str = Field(..., description="The title of the project")
    user_id: str = Field(..., description="The ID of the user who created the project")

    class Settings:
        name = "projects"


class ProjectCreate(BaseModel):
    title: str = Field(..., description="The title of the project")
    user_id: str = Field(..., description="The ID of the user who created the project")


class ProjectTitleUpdate(BaseModel):
    title: str
