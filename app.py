from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import User, Project, Assessment, QuestionBank, Question, UserAlgorithm
from routes import user_router, project_router, assessment_router, question_bank_router, question_router, question_generation_router, user_algorithm_router
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
    await init_beanie(database=db, document_models=[User, Project, Assessment, QuestionBank, Question, UserAlgorithm])
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
app.include_router(project_router, prefix="/projects")
app.include_router(assessment_router, prefix="/assessments")
app.include_router(question_bank_router, prefix="/question_banks")
app.include_router(question_router, prefix="/questions")
app.include_router(question_generation_router, prefix="/question_generation")
app.include_router(user_algorithm_router, prefix="/users_algorithms")

@app.get("/")
async def index():
    return {"message": "Edcraft API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
