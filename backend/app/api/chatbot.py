from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ChatMessage
from app.schemas import ChatRequest, ChatResponse, ChatHistoryResponse, ChatHistoryEntry

# Import agents
from agents.guard import guard_agent_check
from agents.classification import classify_intent
from agents.details import handle_details_query
from agents.order_taking import handle_order
from agents.recommendation import handle_recommendation_query

router = APIRouter()

# Dummy function to simulate the 5-agent processing
def process_query(user_input: str) -> (str, str):
    # Guard Agent: Check for banned words.
    banned_keywords = ["spam", "inappropriate", "banned"]
    for word in banned_keywords:
        if word in user_input.lower():
            return ("GuardAgent", "Your message contains inappropriate content. Please rephrase your query.")
    
    # Classification Agent: Determine query category
    lower_input = user_input.lower()
    category = "General"
    if "order" in lower_input:
        category = "Order"
    elif "discount" in lower_input or "price" in lower_input or "offer" in lower_input:
        category = "Sales"
    elif "support" in lower_input or "help" in lower_input:
        category = "Support"
    elif "faq" in lower_input or "how" in lower_input or "what" in lower_input:
        category = "FAQ"
    
    # Route to appropriate agent based on classification
    if category == "FAQ":
        # Details Agent: Retrieve FAQ details
        response = "Here are our FAQs: We are open 9-5 Mon-Fri, and you can reach support via email."
        agent = "DetailsAgent"
    elif category == "Sales":
        # Recommendation Agent: Suggest products or offers
        response = "We recommend checking out our latest offers and discounts available now!"
        agent = "RecommendationAgent"
    elif category == "Support":
        # Details Agent (or a dedicated support agent)
        response = "Our support team is here to help. Could you please provide more details about your issue?"
        agent = "DetailsAgent"
    elif category == "Order":
        # Order-Taking Agent: Handle order placement steps
        response = "To place an order, please provide your product ID, quantity, and shipping details."
        agent = "OrderTakingAgent"
    else:
        response = "I'm sorry, I didn't understand that. Could you please clarify your query?"
        agent = "ClassificationAgent"
    
    return (agent, response)

# Existing endpoints for /api/chat and /api/voice remain here...

@router.post("/advanced-chat", response_model=ChatResponse)
def advanced_chat(request: ChatRequest, db: Session = Depends(get_db)):
    if not request.session_id or not request.user_input:
        raise HTTPException(status_code=400, detail="Missing session_id or user_input")
    
    # 1. Guard Agent: Check if input is safe.
    from agents.guard import guard_agent_check
    if not guard_agent_check(request.user_input):
        response_text = "Your message contains inappropriate content. Please rephrase."
        agent = "GuardAgent"
    else:
        # 2. Classification Agent: Classify the user input.
        from agents.classification import classify_intent
        intent = classify_intent(request.user_input)
        
        # 3. Routing based on intent
        if intent == "order":
            from agents.order_taking import handle_order
            response_text = handle_order(request.user_input, db)
            agent = "OrderTakingAgent"
        elif intent == "details":
            from agents.details import handle_details_query
            response_text = handle_details_query(request.user_input)
            agent = "DetailsAgent"
        elif intent == "recommendation":
            from agents.recommendation import handle_recommendation_query
            response_text = handle_recommendation_query(request.user_input)
            agent = "RecommendationAgent"
        else:
            response_text = "I'm sorry, could you please clarify your query?"
            agent = "FallbackAgent"
    
    # 4. Store conversation in the database.
    user_msg = ChatMessage(session_id=request.session_id, sender="user", message=request.user_input)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    
    bot_msg = ChatMessage(session_id=request.session_id, sender="bot", message=response_text)
    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)
    
    return ChatResponse(agent=agent, response=response_text)

@router.post("/voice", response_model=ChatResponse)
def process_voice(request: ChatRequest, db: Session = Depends(get_db)):
    # Use the same voice processing logic as before (using user_input)
    response_text = f"Voice Echo: {request.user_input}"
    
    user_msg = ChatMessage(session_id=request.session_id, sender="user", message=request.user_input)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    
    bot_msg = ChatMessage(session_id=request.session_id, sender="bot", message=response_text)
    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)
    
    return ChatResponse(agent="DemoAgent", response=response_text)

@router.post("/chat", response_model=ChatResponse)
def process_chat(request: ChatRequest, db: Session = Depends(get_db)):
    if not request.session_id or not request.user_input:
        raise HTTPException(status_code=400, detail="Missing session_id or user_input")
    
    user_msg = ChatMessage(session_id=request.session_id, sender="user", message=request.user_input)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    
    bot_response_text = f"Echo: {request.user_input}"
    
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
