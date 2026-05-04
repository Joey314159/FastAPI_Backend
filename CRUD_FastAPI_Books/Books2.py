from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publishedDate: int

    def __init__(self, id, title, author, description, rating, publishedDate) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publishedDate = publishedDate


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=120)
    # greater than 1, less than 6
    rating: int = Field(gt=-1, lt=6)
    publishedDate: int = Field(gt=1680, lt=2027)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New Book",
                "author": "codingWithRoby",
                "description": "A very good book",
                "rating": "",
                "publishedDate": "",
            }
        }
    }


BOOKS = [
    Book(
        1,
        "Concepts of Programming Languages",
        "Sebesta",
        "Goes over the syntax and semantics of Programming Languages",
        5,
        2000,
    ),
    Book(
        2,
        "Elementary Linear Algebra",
        "Larson Edwards",
        "The continuation of calculus",
        4,
        2010,
    ),
    Book(
        3,
        "Data Structures & Algorithms in Java",
        "Lafore",
        "Fundamental for anyone studying Computer Science",
        5,
        2003,
    ),
    Book(
        4,
        "Cracking the Coding Interview",
        "Gayle Laakmann",
        "The trick to passing the technical portion of the interview",
        5,
        2000,
    ),
    Book(
        5,
        "Differential Equations",
        "Zill",
        "The final book of the calculus studies",
        4,
        1990,
    ),
    Book(
        6,
        "Starting out with C++",
        "Tony Gaddis",
        "Goes over the syntax and semantics of the C++ Programming Language",
        5,
        2001,
    ),
]


@app.get("/Books")
async def readAllBooks():
    return BOOKS


@app.get("/Books/")
async def getByRating(bookRating: int = Query(gt=0, lt=6)):
    booksToReturn = []

    for b in BOOKS:
        if b.rating == bookRating:
            booksToReturn.append(b)
    return booksToReturn


@app.get("/Books/publishedDate/")
async def getByPublishedDate(publishedDate: int = Query(gt=1680, lt=2027)):
    publishedYearBooks = []

    for b in BOOKS:
        if b.publishedDate == publishedDate:
            publishedYearBooks.append(b)

    return publishedYearBooks


@app.get("/Books/{book_ID}")
# We are adding extra validation to path parameters to ensure that the user is inputting valid data
async def readBook(book_ID: int = Path(gt=0)):
    for b in BOOKS:
        if b.id == book_ID:
            return b


@app.post("/create_Book")
# Body() does not allow us to do any validation of data coming into our application
async def create_Book(book_Request: BookRequest):
    newBooks = Book(**book_Request.model_dump())
    BOOKS.append(findBookID(newBooks))


def findBookID(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.put("/Books/updateBook")
async def updateBook(book: BookRequest):
    for i in range(len(BOOKS)):
        if book.id == BOOKS[i].id:
            BOOKS[i] = book


@app.delete("/Books/{book_id}")
async def deleteBook(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
