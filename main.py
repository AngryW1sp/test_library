from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Base, User, Book
from database import engine, SessionLocal, get_db
from schemas import UserCreate, UserRead, BookCreate, BookRead

app = FastAPI()

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Зависимость

@app.get("/users/") 
async def get_users(db = Depends(get_db)):
    return db.query(User).all()


@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
        db_user = User(**user.model_dump())
        if db.query(User).filter(User.email == db_user.email).first():
             raise HTTPException(status_code=500, detail="Данный юзер уже существует")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


@app.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id, db=Depends(get_db)):
        user = db.query(User).filter(User.id == id).first()
        if user == None:
            raise HTTPException(status_code=404, detail='Пользователь не найден')
        db.delete(user)  # удаляем объект
        db.commit()     # сохраняем изменения
        return user

@app.post("/books/", response_model=BookRead)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
        db_book = Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
