from fastapi import Body, FastAPI

# Allows uvicorn understand that we are creating a new app object
app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/Books")
async def readBooks():
    return BOOKS


@app.get("/Books/{book_Title}")
async def readBook(book_Title: str):
    for b in BOOKS:
        if b.get("title").casefold() == book_Title.casefold():
            return b


@app.get("/Books/")
async def readCategory(category):
    booksToReturn = []

    for b in BOOKS:
        if b.get("category").casefold() == category.casefold():
            booksToReturn.append(b)

    return booksToReturn


# Path parameter needed to find the location of where the data you want is at
@app.get("/Books/{book_Author}/")
# Then you will have to use query parameter to filter the data we want to return
async def readAuthor(book_Author: str, category: str):
    books2Return = []

    for b in BOOKS:
        if (
            b.get("author").casefold() == book_Author.casefold()
            and b.get("category") == category.casefold()
        ):
            books2Return.append(b)

    return books2Return


# Only the post request uses the Body() not the get request
@app.post("/books/createBook")
async def createBook(newBook=Body()):
    BOOKS.append(newBook)


@app.put("/books/updateBook")
async def update(updatedBook=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updatedBook.get("title").casefold():
            BOOKS[i] = updatedBook


@app.delete("/books/deleteBook/{bookTitle}")
async def deleteBook(bookTitle: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == bookTitle.casefold():
            BOOKS.pop(i)
            break
