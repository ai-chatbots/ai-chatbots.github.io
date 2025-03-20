# agents/details.py

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from app.config import OPENAI_API_KEY

# Load OpenAI API Key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize embeddings
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# Load sample business/menu data (adapt as needed)
menu_data = [
    {"name": "Latte", "description": "A creamy coffee with steamed milk."},
    {"name": "Cappuccino", "description": "Espresso with frothy milk."},
    {"name": "Espresso", "description": "A strong, concentrated coffee shot."},
    {"name": "Mocha", "description": "Chocolate-flavored espresso with milk."}
]

# Convert items to Documents
documents = [Document(page_content=f"{item['name']}: {item['description']}") for item in menu_data]

# Split text into chunks for retrieval
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
split_documents = text_splitter.split_documents(documents)

# Create a FAISS vector store from documents
vector_store = FAISS.from_documents(split_documents, embeddings)

# Initialize the chat model
llm = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY)

# Create a retriever from the vector store
retriever = vector_store.as_retriever()

def handle_details_query(user_query: str) -> str:
    """
    Uses retrieval-augmented generation (RAG) to answer user queries with business-specific details.
    """
    relevant_docs = retriever.get_relevant_documents(user_query)
    
    if not relevant_docs:
        return "Sorry, I couldn't find that information. Can you specify more details?"
    
    # Combine the relevant document contents
    context = "\n".join([doc.page_content for doc in relevant_docs])
    prompt = f"User asked: {user_query}\n\nRelevant information:\n{context}\n\nProvide a friendly, concise answer:"
    response = llm.invoke(prompt)
    return response.content
