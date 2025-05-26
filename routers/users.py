from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from models import Base, User, Book
from database import engine, SessionLocal
from schemas import UserRead
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

