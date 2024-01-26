from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str 
    author: str
    description: str 
    rating: int 
    published_year: int

    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year

Books = [
    Book(1, 'title1', 'author1', 'description1', 1, 2019),
    Book(2, 'title2', 'author2', 'description2', 2, 2023),
    Book(3, 'title3', 'author3', 'description3', 3, 2001),
    Book(4, 'title4', 'author4', 'description4', 4, 2005),
    Book(5, 'title5', 'author5', 'description5', 5, 2021)
]

class BookRequest(BaseModel):
    id: Optional[int] = Field(title='Id is not Required', default=None)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_year: int = Field(lt=2025)

    class Config:
        json_schema_extra = {
            'example': {
                'id': None ,
                'title' : 'Book Name',
                'author': 'Author Name',
                'description': 'Book Description',
                'rating': 5,
                'published_year': 2021                           
            }
        }

@app.get("/")
async def welcome():
    return {"Message": "Welcome to the Bookstore!"}

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return Books

@app.post("/create_new_book", status_code=status.HTTP_201_CREATED)
async def create_new_book(new_book: BookRequest):
    new_book = Book(new_book.id, new_book.title, new_book.author, new_book.description, new_book.rating, new_book.published_year)
    book = add_id(new_book)
    Books.append(book)
    return Books

def add_id(book):
    book.id = 1 if len(Books) == 0 else Books[-1].id +1
    return book

@app.put('/update_books', status_code=status.HTTP_202_ACCEPTED)
async def update_book_entry(update_book: BookRequest):
    for i in range(len(Books)):
        if Books[i].id == update_book.id:
            Books[i] = update_book
            return Books
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete('/delete_book/{book_id}', status_code=status.HTTP_200_OK)
async def delete_book_by_id(book_id: int = Path(gt=0, lt=len(Books)+1)):
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            return Books
    raise HTTPException(status_code=404, detail="Book not found")

@app.get('/filter_by_published_year/{published_year}', status_code=status.HTTP_200_OK)
async def filter_by_year(published_year: int = Path(gt=0, lt=2025)):
    filtered_books = []
    for book in Books:
        if book.published_year == published_year:
            filtered_books.append(book)
    if len(filtered_books) == 0:
        raise HTTPException(status_code=404, detail="No books found in the provided year")
    return filtered_books

@app.get('/filter_by_rating/', status_code=status.HTTP_200_OK)
async def filter_by_rating(rating: int = Query(gt=0, lt=6)):
    filtered_books = []
    for book in Books:
        if book.rating == rating:
            filtered_books.append(book)
    if len(filtered_books) == 0:
        raise HTTPException(status_code=404, detail="No books found with the provided rating")
    return filtered_books

'''
assignment: 
Create a new field called published_year and filter the books based on the published date
'''
#look above for the updated code 



