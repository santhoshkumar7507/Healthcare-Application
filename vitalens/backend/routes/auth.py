"""VitaLens — routes/auth.py"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt, datetime, os
from sqlalchemy.orm import Session
from database import get_db, User

router = APIRouter()
SECRET = os.getenv("JWT_SECRET", "vitalens-dev-secret")

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Registered successfully", "email": new_user.email}

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or user.password != form.password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    token = jwt.encode(
        {"sub": user.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
        SECRET, algorithm="HS256"
    )
    return {"access_token": token, "token_type": "bearer", "name": user.name}
