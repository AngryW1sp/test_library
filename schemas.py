from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserRead(UserCreate):
    id: int
    book_on_hand: int = Field(0, ge=0)
    
    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int | None = None
    isbn: str | None = None
    count: int = Field(1, ge=0)

class BookRead(BookCreate):
    id: int

    class Config:
        orm_mode = True

class LibrarianCreate(BaseModel):
    email: EmailStr
    password: str

class LibrarianRead(LibrarianCreate):
    id: int
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    