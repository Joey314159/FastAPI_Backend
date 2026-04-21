from fastapi import FastAPI

# Allows uvicorn understand that we are creating a new app object
app = FastAPI()

BOOKS = [
    {"Title: ": "Title One", "Author: ": "Author One", "Category: ": "Science"},
    {"Title: ": "Title Two", "Author: ": "Author Two", "Category: ": "Science"},
    {"Title: ": "Title Three", "Author: ": "Author Three", "Category: ": "Science"},
    {"Title: ": "Title Four", "Author: ": "Author Four", "Category: ": "Science"},
    {"Title: ": "Title Five", "Author: ": "Author Five", "Category: ": "Science"},
    {"Title: ": "Title Six", "Author: ": "Author Six", "Category: ": "Science"},
]


@app.get("/")
async def firstFN():
    return {"Message ": "Hello World"}
