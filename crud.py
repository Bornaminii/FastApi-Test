from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A story of love and tragedy in the Roaring Twenties."   
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "description": "A dystopian future where the government controls all thought and information."
    },
    {
        "id": 3,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "A story of love and tragedy in the South."
    }
]


@app.get("/books")
def get_books():
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str

@app.post("/books")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book


class UpdatedBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: UpdatedBook):
    for book in books:
        if book['id'] == book_id:
            book['title'] = updated_book.title
            book['author'] = updated_book.author
            book['description'] = updated_book.description
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")