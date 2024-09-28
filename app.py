from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import User, Assessment, QuestionBank, Question
from routes.user_routes import user_router
from routes.assessment_routes import assessment_router
from routes.question_bank_routes import question_bank_router
from routes.question_routes import question_router
from routes.question_generation_routes import question_generation_router

from config import Config
# Load configuration
config = Config()

app = FastAPI()

# Initialize MongoDB client
client = AsyncIOMotorClient(config.MONGO_URI)
db = client[config.MONGO_DBNAME]

# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(database=db, document_models=[User, Assessment, QuestionBank, Question])
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router, prefix="/users")
app.include_router(assessment_router, prefix="/assessments")
app.include_router(question_bank_router, prefix="/question_banks")
app.include_router(question_router, prefix="/questions")
app.include_router(question_generation_router, prefix="/question_generation")

@app.get("/")
async def index():
    return {"message": "Edcraft API"}

@app.get("/test_db_connection")
async def test_db_connection():
    users_collection = db["users"]
    users = await users_collection.find().to_list(10)
    for user in users:
        if "_id" in user:
            user["_id"] = str(user["_id"])

    return {"users": users}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
