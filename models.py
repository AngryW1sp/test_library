from sqlalchemy import Column, Integer, String, CheckConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    book_on_hand = Column(Integer, default=0)

    
    __table_args__ = (
        CheckConstraint('book_on_hand >= 0', name = 'check_book_on_hand_positive'),
    )

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    published_year = Column(Integer, nullable=True)
    isbn = Column(String, nullable=True)
    count = Column(Integer, default=1, nullable=True)

    __table_args__ = (
        CheckConstraint('published_year >= 0', name = 'check_year_positive'), #Не думаю, что у нас будет продаваться книга, написанная до нашей эры
        CheckConstraint('count >= 0', name = 'check_count_positive'),
        #UniqueConstraint('author', 'title', 'published_year', name = 'uq_author_title_pubdate')
    )

class Librarian(Base):
    __tablename__ = "librarians"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)