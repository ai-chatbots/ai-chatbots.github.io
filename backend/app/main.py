from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, chatbot, courses, tutors, subscription, analytics
from app.database import engine
from app.models import *  # Import models so they are registered
from app.database import Base

app = FastAPI(title="AION Agents SaaS Backend")

# Add CORSMiddleware to allow preflight OPTIONS requests and set CORS policies
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Allow all origins for testing; replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],            # Allow all headers
)

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(tutors.router, prefix="/tutors", tags=["Tutors"])
app.include_router(subscription.router, tags=["Subscription"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AION Chatbots API"}
