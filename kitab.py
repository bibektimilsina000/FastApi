from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()


books = {
    "book1": {"name": "book1", "author": "author1"},
    "book2": {"name": "book2", "author": "author2"},
    "book3": {"name": "book3", "author": "author3"},
    "book4": {"name": "book4", "author": "author4"},
    "book5": {"name": "book5", "author": "author5"},
}


class Category(str, Enum):
    Story = "Story"
    Novel = "Novel"
    Fantasy = "Fantasy"
    Science = "Science"


@app.get("/")
async def allBooks(skip_book: Optional[str] = None):
    if skip_book:
        new_books = books.copy()
        del new_books[skip_book]
        return new_books
    return books


@app.get("/books/fav")
async def favBooks():
    return {"favBooks": "My Fav Book"}


@app.get("/books/{book_id}")
async def getBook(book_id: str):
    if book_id in books:
        return {"book": books[book_id]}
    else:
        return {"error": "Book not found"}


@app.get("/category/{category}")
async def getCategory(category: Category):
    if category == Category.Story:
        return {"category": "Story"}
    elif category == Category.Novel:
        return {"category": "Novel"}
    elif category == Category.Fantasy:
        return {"category": "Fantasy"}
    elif category == Category.Science:
        return {"category": "Science"}
    else:
        return {"error": "Invalid category"}


@app.get("/book/{book_name}")
async def readBook(book_name: str):
    return books[book_name]


@app.post("/")
async def createBook(book_name: str, author: str):
    bookslen = len(books)

    books[f"book{bookslen+1}"] = {"name": book_name, "author": author}

    return books[f"book{bookslen+1}"]


@app.put("/books/{book_name}")
async def updateBook(book_name, newame: str, author: str):
    books[book_name] = {"name": newame, "author": author}

    return books[book_name]
