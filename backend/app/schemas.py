from pydantic import BaseModel
from datetime import datetime

# User Schemas
class User(BaseModel):
    email: str
    full_name: str | None = None

class UserCreate(BaseModel):
    email: str
    full_name: str | None = None
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Chatbot Schemas
class ChatRequest(BaseModel):
    session_id: str
    user_input: str

class ChatResponse(BaseModel):
    agent: str
    response: str

class ChatHistoryEntry(BaseModel):
    sender: str
    message: str
    timestamp: datetime

class ChatHistoryResponse(BaseModel):
    history: list[ChatHistoryEntry]

# Course Schemas
class Course(BaseModel):
    id: int
    title: str
    description: str

class EnrollmentRequest(BaseModel):
    user_email: str
    course_id: int

# Tutor Schemas
class Tutor(BaseModel):
    id: int
    name: str
    bio: str

class TutorQuestion(BaseModel):
    tutor_id: int
    user_email: str
    question: str

class TutorResponse(BaseModel):
    answer: str

# Subscription Schemas
class Plan(BaseModel):
    id: int
    name: str
    price: int

class SubscriptionRequest(BaseModel):
    user_email: str
    plan_id: int
