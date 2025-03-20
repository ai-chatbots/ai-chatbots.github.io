from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL", "mysql+pymysql://root:dkerl2345W$E@localhost/aion_db"
)

# OpenAI API key for agent integrations
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key-here")