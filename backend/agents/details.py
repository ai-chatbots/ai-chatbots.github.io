import os
import pickle  # (Optional: remove if not needed elsewhere)
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import OPENAI_API_KEY

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Default business data as fallback
default_menu_data = [
    {"name": "Latte", "description": "A creamy coffee with steamed milk."},
    {"name": "Cappuccino", "description": "Espresso with frothy milk."},
    {"name": "Espresso", "description": "A strong, concentrated coffee shot."},
    {"name": "Mocha", "description": "Chocolate-flavored espresso with milk."}
]
default_documents = [Document(page_content=f"{item['name']}: {item['description']}") for item in default_menu_data]
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
default_docs = text_splitter.split_documents(default_documents)

# Try to load the FAISS index from disk; otherwise, build one from default data.
if os.path.exists("faiss_index"):
    try:
        vector_store = FAISS.load_local("faiss_index", embeddings)
    except Exception as e:
        print(f"[ERROR] Failed to load FAISS index: {e}. Using default data.")
        vector_store = FAISS.from_documents(default_docs, embeddings)
else:
    vector_store = FAISS.from_documents(default_docs, embeddings)

llm = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY)
retriever = vector_store.as_retriever()

def handle_details_query(user_query: str) -> str:
    relevant_docs = retriever.get_relevant_documents(user_query)
    if not relevant_docs:
        return "Sorry, I couldn't find relevant details. Could you please provide more context?"
    context = "\n".join([doc.page_content for doc in relevant_docs])
    prompt = (
        f"User asked: {user_query}\n\n"
        f"Relevant details:\n{context}\n\n"
        "Provide a concise, friendly answer:"
    )
    response = llm.invoke(prompt)
    return response.content
