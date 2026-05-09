from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import Models
from starlette import status
from Models import Todos
from Database import SessionLocal, engine

app = FastAPI()

Models.Base.metadata.create_all(bind=engine)


def getDB():
    db = SessionLocal()
    try:
        # Pauses the function and gives the session to your route
        yield db
    finally:
        # Ensures we never leave a Database connection open by closing it immediately afterwards
        db.close()


# First dependancy injection
dbDependancy = Annotated[Session, Depends(getDB)]
#                                 ^^^^^^^^^^^^^---- Tells FastAPI 'whenever a route needs this, automatically run getDB() and inject the results'
#    This is helpful because instead of each route managing its own database session; we define it once and FastAPI
#    knows to write it in wherever you ask for it


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@app.get("/", status_code=status.HTTP_200_OK)
async def readAll(db: dbDependancy):
    return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def readTodo(db: dbDependancy, todo_id: int = Path(gt=0)):
    todoModel = db.query(Todos).filter(Todos.id == todo_id).first()

    if todoModel is not None:
        return todoModel
    raise HTTPException(status_code=404, detail="Todo ID not found")


@app.post("/todo/", status_code=status.HTTP_201_CREATED)
async def createTodo(db: dbDependancy, todoRequest: TodoRequest):
    todoModel = Todos(**todoRequest.model_dump())
    db.add(todoModel)
    db.commit()


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTodo(
    db: dbDependancy, todoRequest: TodoRequest, todo_id: int = Path(gt=0)
):
    todoModel = db.query(Todos).filter(Todos.id == todo_id).first()

    if todoModel is None:
        raise HTTPException(status_code=404, detail="To Do ID not found")

    todoModel.title = todoRequest.title
    todoModel.description = todoRequest.description
    todoModel.priority = todoRequest.priority
    todoModel.complete = todoRequest.complete

    db.add(todoModel)
    db.commit()


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(db: dbDependancy, todo_id: int = Path(gt=0)):
    todoModel = db.query(Todos).filter(Todos.id == todo_id).first()

    if todoModel is None:
        raise HTTPException(status_code=404, detail="To Do ID was not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
