# agents/guard.py

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

def guard_agent_check(user_input: str) -> bool:
    """
    Checks if the user input is safe using a multi-layered approach:
      1. Keyword-based filtering.
      2. A LangChain LLMChain to evaluate content safety.
      3. For long inputs, splits text into chunks and evaluates each.
    
    Returns True if safe, False if any content is flagged as harmful or inappropriate.
    """
    # --- Step 1: Basic Keyword Filter ---
    blocked_keywords = ["badword1", "badword2", "hack", "spam"]
    for kw in blocked_keywords:
        if kw in user_input.lower():
            print(f"[LOG] Blocked input: '{user_input}' due to keyword: {kw}")
            return False

    # --- Step 2: LangChain LLMChain for Content Moderation ---
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template=(
            "Evaluate the following text for harmful, inappropriate, or offensive language. "
            "Respond with 'Yes' if it contains such content, or 'No' if it is safe.\n\n"
            "Text: {user_input}\n\nAnswer:"
        )
    )
    # Initialize the ChatOpenAI LLM (adjust model and temperature as needed)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    # --- Step 3: Split long inputs into chunks if necessary ---
    if len(user_input) > 200:
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
        chunks = splitter.split_text(user_input)
    else:
        chunks = [user_input]
    
    # Evaluate each chunk with the LLMChain.
    for chunk in chunks:
        result = chain.run(user_input=chunk)
        # If the LLM indicates harm (contains "yes"), flag as unsafe.
        if "yes" in result.lower():
            print(f"[LOG] LLM flagged chunk as unsafe: '{chunk}' with response: '{result.strip()}'")
            return False

    print(f"[LOG] Input passed guard check: '{user_input}'")
    return True
