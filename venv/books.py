from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models 
from database import SessionLocal,engine
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    ratings: int = Field(gt=-1, lt=101)

BOOKS=[] 

@app.get("/")
def read_books(db: Session = Depends(get_db)):
    return db.query(models.Books).all()

@app.post("/create")
def create_book(book: Book,db : Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.ratings = book.ratings
    db.add(book_model)
    db.commit()

    return book

# Update a book by ID
@app.put("/{book_id}")
def update_book(book_id: UUID, book: Book, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        for attr, value in book.dict().items():
            setattr(db_book, attr, value)
        db.commit()
        return db_book
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {book_id} not found"
        )

# Delete a book by ID
@app.delete("/{book_id}")
def delete_book(book_id: UUID, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return {"message": f"Book with id {book_id} deleted"}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {book_id} not found"
        )
