# agents/recommendation.py

from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI()  # Initialize OpenAI client

def handle_recommendation_query(user_input: str) -> str:
    """
    Provides a product or service recommendation based on the user query.
    In a real system, you'd incorporate user data or a recommendation engine.
    """
    print(f"[LOG] Recommendation Query Received: {user_input}")
    prompt = f"""
    You are a Recommendation Agent for a chatbot SAAS.
    The user asked: '{user_input}'
    Based on typical preferences, suggest a product or service they might enjoy.
    """
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful recommendation agent."},
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content.strip()
    print(f"[LOG] Recommendation Response: {response}")
    return response
