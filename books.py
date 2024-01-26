from fastapi import Body, FastAPI

app = FastAPI()
Books = [
    {"title": "Title 1", "author": "Author 1", "category": "Science"},
    {"title": "Title 2", "author": "Author 2", "category": "Science"},
    {"title": "Title 3", "author": "Author 3", "category": "Maths"},
    {"title": "Title 4", "author": "Author 4", "category": "History"},
    {"title": "Title 5", "author": "Author 5", "category": "Science"},
    {"title": "Title 6", "author": "Author 6", "category": "Computer"}
]

@app.get("/")
async def welcome():
    return {"Message":"Welcome to Fastapi"}

@app.get("/books")
async def read_all_books():
    return Books

@app.get("/filter/{author_name}")
async def filter_by_author_and_category(author_name: str, category: str):
    books_to_return = []
    for i in Books:
        if i.get("author").casefold() == author_name.casefold() and i.get("category").casefold() == category.casefold():
            books_to_return.append(i)
    if len(books_to_return) == 0:
        return {"Message": "No books matches the author name and category combination",
                "Filter Output": books_to_return}
    else:
        return books_to_return

@app.get("/books/{book_title}")
async def read_book_by_title(book_title: str):
    for i in Books:
        if i.get("title").casefold() == book_title.casefold():
            return i
    return {"Message": "Choose title from the book list",
            "Book List": Books}

@app.post("/create_new_book")
async def create_new_book_entry(new_book = Body()):
    Books.append(new_book)
    return Books

@app.post("/create_new_book/")
async def create_new_book_entry(title: str, author: str, category: str):
    new_book = {"title": title, "author": author, "category": category}
    Books.append(new_book)
    return Books
        
@app.put("/update_books")
async def update_book_details(update_books = Body()):
    for i in range(len(Books)):
        if Books[i].get("title").casefold() == update_books.get("title").casefold():
            Books[i] = update_books
            return Books
        
@app.delete("/delete_books/{book_title}")
async def delete_book_by_title(book_title: str):
    for i in range(len(Books)):
        if Books[i].get("title").casefold() == book_title.casefold():
            del Books[i]
            return Books
    return {"Message": "Choose title from the book list",
            "Book List": Books}

'''
    Assignment: Create a new API end point to fetch books of a specific author.
'''
#Solution:
@app.get('/fetch_by_author')
async def get_books_by_author(author: str):
    books_to_return = []
    for i in Books:
        if i.get('author').casefold() == author.casefold():
            books_to_return.append(i)
    if len(books_to_return) == 0:
        return {"Message": "No books matches the author name",
                "Filter Output": books_to_return}
    else:
        return books_to_return
