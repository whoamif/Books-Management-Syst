from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models 
from database import SessionLocal, engine
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

@app.get("/")
def read_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@app.post("/create")
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Book(**book.dict())
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model

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

@app.delete("/{book_id}")
def delete_book(book_id: int , db: Session = Depends(get_db)):
    book_model = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {book_id} not found"
        )
    db.delete(book_model)
    db.commit()
    return {"message": "Book deleted successfully"}
