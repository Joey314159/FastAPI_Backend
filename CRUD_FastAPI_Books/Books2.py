from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=120)
    # greater than 1, less than 6
    rating: int = Field(gt=-1, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New Book",
                "author": "codingWithRoby",
                "description": "A very good book",
                "rating": "",
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
    ),
    Book(
        2,
        "Elementary Linear Algebra",
        "Larson Edwards",
        "The continuation of calculus",
        4,
    ),
    Book(
        3,
        "Data Structures & Algorithms in Java",
        "Lafore",
        "Fundamental for anyone studying Computer Science",
        5,
    ),
    Book(
        4,
        "Cracking the Coding Interview",
        "Gayle Laakmann",
        "The trick to passing the technical portion of the interview",
        5,
    ),
    Book(
        5, "Differential Equations", "Zill", "The final book of the calculus studies", 4
    ),
    Book(
        6,
        "Starting out with C++",
        "Tony Gaddis",
        "Goes over the syntax and semantics of the C++ Programming Language",
        5,
    ),
]


@app.get("/Books")
async def readAllBooks():
    return BOOKS


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
