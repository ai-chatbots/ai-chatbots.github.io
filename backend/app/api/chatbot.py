from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ChatMessage
from app.schemas import ChatRequest, ChatResponse, ChatHistoryResponse, ChatHistoryEntry

router = APIRouter()

@router.post("/voice", response_model=ChatResponse)
def process_voice(request: ChatRequest, db: Session = Depends(get_db)):
    # Process voice input (simulated as text) using the correct attribute
    response_text = f"Voice Echo: {request.user_input}"
    
    # Store user's voice message
    user_msg = ChatMessage(session_id=request.session_id, sender="user", message=request.user_input)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    
    # Store bot's response message
    bot_msg = ChatMessage(session_id=request.session_id, sender="bot", message=response_text)
    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)
    
    return ChatResponse(agent="DemoAgent", response=response_text)

@router.post("/chat", response_model=ChatResponse)
def process_chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Check required fields
    if not request.session_id or not request.user_input:
        raise HTTPException(status_code=400, detail="Missing session_id or user_input")

    # Store user's message
    user_msg = ChatMessage(session_id=request.session_id, sender="user", message=request.user_input)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # Process the message (dummy echo bot)
    bot_response_text = f"Echo: {request.user_input}"
    
    # Store bot's message
    bot_msg = ChatMessage(session_id=request.session_id, sender="bot", message=bot_response_text)
    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)

    return ChatResponse(agent="DemoAgent", response=bot_response_text)

@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
def get_history(session_id: str, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.timestamp).all()
    history = [
        ChatHistoryEntry(sender=msg.sender, message=msg.message, timestamp=msg.timestamp)
        for msg in messages
    ]
    return ChatHistoryResponse(history=history)
