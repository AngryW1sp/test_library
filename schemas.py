from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str
    email: str

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