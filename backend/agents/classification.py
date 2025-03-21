# agents/classification.py

def classify_intent(user_input: str) -> str:
    """
    Naively classifies the user query into one of the following intents:
    "order", "details", "recommendation", or "other".
    
    Prioritizes details when the query mentions 'ingredient(s)'.
    """
    text_lower = user_input.lower()
    
    # Prioritize details if "ingredient" is mentioned
    if "ingredient" in text_lower:
        print(f"[LOG] Intent classified as 'details' for input: {user_input}")
        return "details"
    
    order_keywords = ["order", "buy", "purchase", "espresso", "latte", "coffee"]
    details_keywords = ["allergen", "menu", "open hours"]  # "ingredient" already handled
    recommendation_keywords = ["recommend", "suggest", "offer", "deal"]

    if any(kw in text_lower for kw in order_keywords):
        print(f"[LOG] Intent classified as 'order' for input: {user_input}")
        return "order"
    elif any(kw in text_lower for kw in details_keywords):
        print(f"[LOG] Intent classified as 'details' for input: {user_input}")
        return "details"
    elif any(kw in text_lower for kw in recommendation_keywords):
        print(f"[LOG] Intent classified as 'recommendation' for input: {user_input}")
        return "recommendation"
    else:
        print(f"[LOG] Intent classified as 'other' for input: {user_input}")
        return "other"
