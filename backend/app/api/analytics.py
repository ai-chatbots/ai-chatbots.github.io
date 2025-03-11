from fastapi import APIRouter

router = APIRouter()

@router.get("/chatbot")
def chatbot_analytics():
    # Stub: Return dummy chatbot analytics.
    return {"analytics": {"messages_processed": 1000, "active_users": 150}}

@router.get("/user")
def user_analytics():
    # Stub: Return dummy user analytics.
    return {"user_analytics": {"total_users": 500, "new_signups": 25}}
