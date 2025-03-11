from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/text", response_model=ChatResponse)
def process_text(request: ChatRequest):
    # Stub: Process the text input and return a dummy response.
    response_text = f"Echo: {request.message}"
    return ChatResponse(response=response_text)

@router.post("/voice", response_model=ChatResponse)
def process_voice(request: ChatRequest):
    # Stub: Process voice input (simulated as text) and return a dummy response.
    response_text = f"Voice Echo: {request.message}"
    return ChatResponse(response=response_text)

@router.get("/history")
def get_history():
    # Stub: Return dummy chat history.
    return {"history": ["Hello", "Hi there!", "How can I help?"]}
