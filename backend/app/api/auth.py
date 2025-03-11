from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.schemas import User, UserCreate, UserLogin
from app.database import fake_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@router.post("/signup", response_model=User)
def signup(user: UserCreate):
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_db[user.email] = user.dict()
    return fake_db[user.email]

@router.post("/login")
def login(user: UserLogin):
    stored_user = fake_db.get(user.email)
    if not stored_user or stored_user.get("password") != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token_data = {"sub": user.email}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = fake_db.get(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
