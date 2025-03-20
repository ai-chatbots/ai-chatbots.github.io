# agents/guard.py

def guard_agent_check(user_input: str) -> bool:
    """
    Checks if the user input is safe by looking for blocked keywords.
    Returns True if safe, False if it contains inappropriate content.
    """
    blocked_keywords = ["badword1", "badword2", "hack", "spam"]
    for kw in blocked_keywords:
        if kw in user_input.lower():
            print(f"[LOG] Blocked input: {user_input} due to keyword: {kw}")
            return False
    print(f"[LOG] Input passed guard check: {user_input}")
    return True
