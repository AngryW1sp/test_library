from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Base, Librarian, User, Book
from database import engine, SessionLocal, get_db
from routers.auth import create_access_token, hash_password
from schemas import LibrarianCreate, Token, UserCreate, UserRead, BookCreate, BookRead

app = FastAPI()


Base.metadata.create_all(bind=engine)


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

@app.get("/books/{book_id}")
async def get_book(id, db = Depends(get_db)):
    return db.query(Book).filter(Book.id == id).first()


@app.get("/books/")
async def get_books(db = Depends(get_db)):
    return db.query(Book).all()

@app.post("/books/", response_model=BookRead)
async def create_book(  db_book: BookCreate, db = Depends(get_db)):
        if db_book.published_year or db_book.published_year==0:
            book = db.query(Book).filter_by(
                title=db_book.title, 
                author=db_book.author, 
                published_year=db_book.published_year).first()
        else:
            book = db.query(Book).filter_by(
                title=db_book.title, 
                author=db_book.author, 
                published_year=None).first()
        
        if book:
            book.count += db_book.count
            
        else:
            book = Book(
                title=db_book.title, 
                author=db_book.author, 
                published_year=db_book.published_year,
                isbn=db_book.isbn,
                count=db_book.count
                )
            db.add(book)
        
        db.commit()
        db.refresh(book)
        return book

@app.post("/register", response_model=Token)
async def register(libr: LibrarianCreate, db = Depends(get_db)):
    reg_lib = db.query(Librarian).filter(Librarian.email == libr.email).first()
    if reg_lib:
        raise HTTPException(status_code=400, detail="Библиотекарь уже существует")
    hashed_pw = hash_password(libr.password)
    user = User(email=libr.email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
