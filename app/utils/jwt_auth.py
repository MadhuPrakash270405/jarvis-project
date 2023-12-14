from datetime import datetime, timedelta
import os
from pprint import pprint
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from dotenv import load_dotenv
# Load the .env file
load_dotenv()
JWT_TOKEN = os.getenv("JWT_TOKEN")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    pin: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user: User, expires_delta: Optional[timedelta] = None):
    user_data = user.dict()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    user_data.update({"exp": expire})
    encoded_jwt = jwt.encode(user_data, JWT_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    print("INTO GET CURRENT USER")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_TOKEN, algorithms=[ALGORITHM])
        pprint(payload)
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        email: str = payload.get("email")
        loginPin: int = payload.get("pin")
        user = User(username=username, email=email,pin=loginPin)
    except JWTError:
        raise credentials_exception
    return user

