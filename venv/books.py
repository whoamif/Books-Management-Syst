from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models 
from database import engine,SessionLocal
from sqlalchemy.orm import Session
 

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally :
        db.close()




class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)


BOOKS = []


@app.get("/")
def read_api(db : Session = Depends(get_db)):
    return db.query(models.Books).all()


@app.post("/")
def create_book(book: Book,db : Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.ratings = book.ratings
    db.add(book_model)
    db.commit()

    return book


@app.put("/{book_id}")
def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} : Does not exist"
    )


@app.delete("/{book_id}")
def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"ID: {book_id} deleted"
    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} : Does not exist"
    )