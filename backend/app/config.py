import os

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL", "mysql+pymysql://root:dkerl2345W$E@localhost/aion_db"
)
