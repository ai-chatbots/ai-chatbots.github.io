from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, chatbot, courses, tutors, subscription, analytics, upload_documents
from app.database import engine, Base
from app.models import *  # This imports User, ChatMessage, etc.

app = FastAPI(title="AION Chatbots Backend")

# Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (if not already present)
Base.metadata.create_all(bind=engine)

# Mount static files (this will serve files in the "static" directory at /static)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount routers – note we include chatbot router under prefix "/api"
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(tutors.router, prefix="/tutors", tags=["Tutors"])
app.include_router(subscription.router, tags=["Subscription"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(upload_documents.router, prefix="/api", tags=["Document Upload"])


@app.get("/")
def read_root():
    return {"message": "Welcome to AION Chatbots API"}
