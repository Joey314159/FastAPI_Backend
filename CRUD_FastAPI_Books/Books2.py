from fastapi import FastAPI
from pydantic import BaseModel, Field

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
    id: int
    title: str = Field(min_length=3)
    author: str
    description: str
    rating: int


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
    BOOKS.append(newBooks)
