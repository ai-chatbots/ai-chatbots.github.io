from fastapi import APIRouter
from app.schemas import Plan, SubscriptionRequest

router = APIRouter()

# Dummy subscription plans
plans = [
    {"id": 1, "name": "Basic", "price": 29},
    {"id": 2, "name": "Pro", "price": 59},
    {"id": 3, "name": "Enterprise", "price": 0}  # Contact for Enterprise
]

@router.get("/plans", response_model=list[Plan])
def get_plans():
    return plans

@router.post("/subscribe")
def subscribe(request: SubscriptionRequest):
    # Stub: Process the subscription.
    return {"message": f"User {request.user_email} subscribed to plan {request.plan_id}"}

@router.get("/billing/history")
def billing_history(user_email: str):
    # Stub: Return dummy billing history.
    return {"billing_history": [{"date": "2025-01-01", "amount": 29}, {"date": "2025-02-01", "amount": 29}]}
