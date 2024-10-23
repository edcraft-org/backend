from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional

class UserAlgorithm(Document):
    id: Optional[PydanticObjectId] = Field(None, alias="_ =id", description="The unique identifier of the algorithm")
    user_id: str = Field(..., description="The ID of the user who created the algorithm")
    topic: str = Field(..., description="The topic associated with the algorithm")
    subtopic: str = Field(..., description="The subtopic associated with the algorithm")
    processor_class_code: str = Field(..., description="The code for the processor class")

    class Settings:
        name = "user_algorithms"

class UserAlgorithmCreate(BaseModel):
    user_id: str = Field(..., description="The ID of the user who created the algorithm")
    topic: str = Field(..., description="The topic associated with the algorithm")
    subtopic: str = Field(..., description="The subtopic associated with the algorithm")
    processor_class_code: str = Field(..., description="The code for the processor class")

class UserAlgorithmUpdate(BaseModel):
    topic: Optional[str] = None
    subtopic: Optional[str] = None
    processor_class_code: Optional[str] = None
