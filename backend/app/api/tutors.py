from fastapi import APIRouter, HTTPException
from app.schemas import Tutor, TutorQuestion, TutorResponse

router = APIRouter()

# Dummy tutors data
tutors = [
    {"id": 1, "name": "Tutor A", "bio": "Expert in AI Chatbots."},
    {"id": 2, "name": "Tutor B", "bio": "Expert in Voice Assistants."}
]

@router.get("", response_model=list[Tutor])
def list_tutors():
    return tutors

@router.get("/{tutor_id}", response_model=Tutor)
def get_tutor(tutor_id: int):
    for tutor in tutors:
        if tutor["id"] == tutor_id:
            return tutor
    raise HTTPException(status_code=404, detail="Tutor not found")

@router.post("/ask", response_model=TutorResponse)
def ask_tutor(question: TutorQuestion):
    # Stub: Return a dummy answer.
    answer = f"Answer to your question: {question.question}"
    return TutorResponse(answer=answer)
