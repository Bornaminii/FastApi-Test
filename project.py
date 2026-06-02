from fastapi import Depends, FastAPI
from pydantic import BaseModel
from db import get_db, SessionLocal
from sqlalchemy.orm import Session
import model


app = FastAPI()


class Bookstore(BaseModel):
    title: str
    author: str
    description: str


@app.post("/books")
def create_book(book: Bookstore, db: Session = Depends(get_db)):
    new_book = model.Book(
        title=book.title, author=book.author, description=book.description)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books
