from typing import Optional
from uuid import UUID
from fastapi import FastAPI, Form, HTTPException, Request
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    imageUrl: str
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(
        max_length=100, min_length=1, title="Title of description"
    )
    rating: int = Field(gt=-1, lt=6)

    class Config:
        schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "imageUrl": "book.png",
                "title": "The subtitle art of not giving the fuck",
                "author": "I dont know the Auther",
                "description": "Lets not write any description ",
                "rating": 5,
            }
        }


books = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception(
    request: Request, exception: NegativeNumberException
):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"you enter{exception.books_to_return}  number.Which is not valid"
        },
    )


@app.get("/")
async def get_books(limit: Optional[int] = None):
    if limit and limit < 0:
        raise NegativeNumberException(books_to_return=limit)
    # if len(books) < 1:
    #     books = add_dummy_book()
    if limit and len(books) > limit:
        return books[0:limit]
    return books


@app.post("/book/login")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username, "passsword": password}


@app.get("/book/{uuid}")
async def get_book(uuid: UUID):
    for book in books:
        if book.id == uuid:
            return book
        not_found_exception()


@app.post("/")
async def create_book(book: Book):
    books.append(book)
    return book


@app.put("/book/{uuid}")
async def edit_book(uuid):
    return {"response": "logic lekhna nai alxi laghayooo"}


@app.delete("/book/{uuid}")
async def delete_book(uuid):
    return {"response": "logic lekhna nai alxi laghayooo"}


def add_dummy_book():
    dummy_books = [
        Book(
            id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            imageUrl="book.png",
            title="The subtitle art of not giving the fuck",
            author="I dont know the Auther",
            description="Lets not write any description ",
            rating=5,
        ),
        Book(
            id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
            imageUrl="book.png",
            title="The subtitle art of not giving the fuck",
            author="I dont know the Auther",
            description="Lets not write any description ",
            rating=5,
        ),
        Book(
            id="3fa85f64-5717-4562-b3fc-2c963f66afa3",
            imageUrl="book.png",
            title="The subtitle art of not giving the fuck",
            author="I dont know the Auther",
            description="Lets not write any description ",
            rating=5,
        ),
        Book(
            id="3fa85f64-5717-4562-b3fc-2c963f66afa2",
            imageUrl="book.png",
            title="The subtitle art of not giving the fuck",
            author="I dont know the Auther",
            description="Lets not write any description ",
            rating=5,
        ),
    ]

    return dummy_books


def not_found_exception():
    return HTTPException(
        detail="Books Not Founnd",
        headers={"X-Header_error": "Nothing is to be found at this uuid"},
        status_code=404,
    )
