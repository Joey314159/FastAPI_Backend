from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from ..Models import Todos
from ..Database import SessionLocal
from .Auth import getCurrentUser

router = APIRouter()


def getDB():
    db = SessionLocal()
    try:
        # Pauses the function and gives the session to your route
        yield db
    finally:
        # Ensures we never leave a Database connection open by closing it immediately afterwards
        db.close()


dbDependancy = Annotated[Session, Depends(getDB)]
userDependency = Annotated[dict, Depends(getCurrentUser)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def readAll(user: userDependency, db: dbDependancy):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner == user.get("id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def readTodo(user: userDependency, db: dbDependancy, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todoModel = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner == user.get("id"))
        .first()
    )

    if todoModel is not None:
        return todoModel
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def createTodo(user: userDependency, db: dbDependancy, todoRequest: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todoModel = Todos(**todoRequest.model_dump(), owner=user.get("id"))
    db.add(todoModel)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTodo(
    user: userDependency,
    db: dbDependancy,
    todoRequest: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todoModel = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner == user.get("id"))
        .first()
    )

    if todoModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todoModel.title = todoRequest.title
    todoModel.description = todoRequest.description
    todoModel.priority = todoRequest.priority
    todoModel.complete = todoRequest.complete

    db.add(todoModel)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(user: userDependency, db: dbDependancy, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todoModel = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner == user.get("id"))
        .first()
    )

    if todoModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner == user.get("id")
    ).delete()

    db.commit()
