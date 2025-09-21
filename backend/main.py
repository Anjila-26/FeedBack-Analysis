from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route.feedback import router as feedback_router
from database import init_database

app = FastAPI()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feedback_router)