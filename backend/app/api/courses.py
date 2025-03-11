from fastapi import APIRouter, HTTPException
from app.schemas import Course, EnrollmentRequest

router = APIRouter()

# Dummy courses data
courses = [
    {"id": 1, "title": "AI Chatbot Fundamentals", "description": "Learn the basics of AI chatbot development."},
    {"id": 2, "title": "Voice Assistant Integration", "description": "Explore integration of voice assistants."},
    {"id": 3, "title": "Advanced Chatbot Analytics", "description": "Master advanced analytics techniques."}
]

@router.get("", response_model=list[Course])
def list_courses():
    return courses

@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")

@router.post("/enroll")
def enroll_course(enrollment: EnrollmentRequest):
    # Stub: Process enrollment.
    return {"message": f"User {enrollment.user_email} enrolled in course {enrollment.course_id}"}
