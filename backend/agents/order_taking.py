# agents/order_taking.py

import uuid
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI()  # Initialize OpenAI client

def handle_order(user_input: str, db, session_id: str = None, user_id: int = None) -> str:
    """
    Processes an order query by simulating order detection, confirmation, and storage.
    Supports both guest orders (using session_id) and registered orders (using user_id).
    
    Note: In a real SAAS application, integrate with your database models (e.g., Order, CartItem, MenuItem).
    """
    print(f"[LOG] Order Processing Started for input: {user_input}")
    try:
        # Ensure we have an identifier for guest orders
        if not user_id and not session_id:
            session_id = str(uuid.uuid4())
        identifier = session_id if session_id else f"user_{user_id}"
        print(f"[LOG] Processing Order for: {identifier}")

        # Dummy behavior: if the cart is empty, detect an item using AI.
        print("[LOG] Cart is empty! Trying to detect an item.")
        prompt = f"Extract the product name from this order: \"{user_input}\"."
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract only the product name."},
                {"role": "user", "content": prompt}
            ]
        )
        extracted_product = completion.choices[0].message.content.strip()
        print(f"[LOG] AI Extracted Product: {extracted_product}")

        # Dummy lookup: Assume the product is found
        product_name = extracted_product
        if product_name:
            print(f"[LOG] Adding {product_name} to cart.")
            # In a real implementation, insert a CartItem record into the database.
        else:
            return f"Sorry, we couldn't find '{extracted_product}' in our menu. Please try again!"

        # Dummy total price calculation
        total_price = 10.0

        prompt = f"Confirm the order for {product_name} with total price ${total_price:.2f}."
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Confirm the order details."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_response = completion.choices[0].message.content.strip()
        print(f"[LOG] AI Order Confirmation: {ai_response}")

        # Here, store the order in the database and clear the cart.
        print(f"[LOG] Order Stored for {identifier}, Total: ${total_price:.2f}")

        return f"{ai_response} Your total is ${total_price:.2f}. Your order has been confirmed!"
    except Exception as e:
        print(f"[ERROR] Order Processing Error: {str(e)}")
        return f"Error processing order: {str(e)}"
