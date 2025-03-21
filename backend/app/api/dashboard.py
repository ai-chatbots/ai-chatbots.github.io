from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os

from app.config import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# For simplicity, use an in‑memory store for dashboard settings.
# In production, you would persist these in a database.
dashboard_settings_store = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/settings")
def get_dashboard_settings(current_user_email: str = Depends(get_current_user_email)):
    settings = dashboard_settings_store.get(current_user_email, {
        "business_strategy": "",
        "agent_configuration": []
    })
    return settings

@router.post("/settings")
def save_dashboard_settings(data: dict, current_user_email: str = Depends(get_current_user_email)):
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Invalid data format")
    dashboard_settings_store[current_user_email] = data
    return {"detail": "Dashboard settings saved successfully"}

@router.get("/insights")
def get_dashboard_insights(current_user_email: str = Depends(get_current_user_email)):
    # Retrieve settings for the current user
    settings = dashboard_settings_store.get(current_user_email, {
        "business_strategy": "",
        "agent_configuration": []
    })
    insights = []

    # Analyze business strategy
    if not settings["business_strategy"]:
        insights.append("Your business strategy is empty. Outline your business goals and target market to drive better chatbot engagement.")
    else:
        insights.append("Your strategy is defined. Consider refining it to match evolving market trends and user needs.")

    # Analyze agent configuration
    agents = settings.get("agent_configuration", [])
    if not agents:
        insights.append("No agent configurations found. Add agents to cover diverse user intents (e.g., ordering, FAQs, recommendations).")
    else:
        insights.append(f"You have configured {len(agents)} agent(s). Ensure that each agent targets a specific function—such as order processing, details retrieval, or recommendations.")
    
    # Add additional generic insights
    insights.append("Monitor your chatbot’s conversation analytics to further optimize response quality and user satisfaction.")

    return {"insights": insights}
