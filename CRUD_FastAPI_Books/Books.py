from fastapi import FastAPI

# Allows uvicorn understand that we are creating a new app object
app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "Science"},
    {"title": "Title Two", "author": "Author Two", "category": "Science"},
    {"title": "Title Three", "author": "Author Three", "category": "Science"},
    {"title": "Title Four", "author": "Author Four", "category": "Science"},
    {"title": "Title Five", "author": "Author Five", "category": "Science"},
    {"title": "Title Six", "author": "Author Six", "category": "Science"},
]


@app.get("/Books")
async def readBooks():
    return BOOKS


@app.get("/Books/{book_Title}")
async def readBook(book_Title: str):
    for b in BOOKS:
        if b.get("title").casefold() == book_Title.casefold():
            return b
