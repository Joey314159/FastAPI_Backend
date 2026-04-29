from fastapi import FastAPI, Body

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
async def create_Book(bookRequest=Body()):
    BOOKS.append(bookRequest)
