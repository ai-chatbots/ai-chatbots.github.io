from fastapi import FastAPI
from app.api import auth, chatbot, courses, tutors, subscription, analytics

app = FastAPI(title="AION Agents SaaS Backend")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(tutors.router, prefix="/tutors", tags=["Tutors"])
app.include_router(subscription.router, tags=["Subscription"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AION Chatbots API"}
