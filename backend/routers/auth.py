from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
import logging

from backend import crud, schemas
from backend.database import get_db
from backend.config import settings

# Suprimir el warning de passlib/bcrypt
logging.getLogger("passlib").setLevel(logging.ERROR)

router = APIRouter()

# Usar la misma configuración que en crud.py
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Usar un valor explícito para bcrypt rounds
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # Por defecto 15 minutos
    to_encode.update({"exp": expire})
    # Asegúrate de que settings.SECRET_KEY y settings.ALGORITHM estén disponibles y correctos
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Cambiado a get_usuario_by_email y usando form_data.username que OAuth2PasswordRequestForm provee como "username"
    user = crud.get_usuario_by_email(db, email=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password_hash): # Asumiendo que el campo es password_hash
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires # Usar user.email para el subject del token
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: Optional[str] = payload.get("sub") # El subject del token es el email
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email) # Usar email para TokenData
    except JWTError:
        raise credentials_exception
    user = crud.get_usuario_by_email(db, email=token_data.email) # Cambiado a get_usuario_by_email
    if user is None:
        raise credentials_exception
    return user

@router.get("/users/me/", response_model=schemas.Usuario)
async def read_users_me(current_user: schemas.Usuario = Depends(get_current_user)):
    return current_user
