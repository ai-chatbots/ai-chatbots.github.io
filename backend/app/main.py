from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, chatbot, courses, tutors, subscription, analytics, upload_documents, fine_tuning
from app.database import engine, Base
from app.models import *

app = FastAPI(title="AION Chatbots Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(tutors.router, prefix="/tutors", tags=["Tutors"])
app.include_router(subscription.router, tags=["Subscription"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(upload_documents.router, prefix="/api", tags=["Document Upload"])
app.include_router(fine_tuning.router, prefix="/api", tags=["FineTuning"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AION Chatbots API"}
