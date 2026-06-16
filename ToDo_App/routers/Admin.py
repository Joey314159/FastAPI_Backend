from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from ..Models import Todos
from ..Database import SessionLocal
from .Auth import getCurrentUser

router = APIRouter(prefix="/admin", tags=["admin"])


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
userDependency = Annotated[dict, Depends(getCurrentUser)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def readAll(user: userDependency, db: dbDependancy):
    if user is None or user.get("userRole") != "admin":
        raise HTTPException(
            status_code=401, detail="You are not an admin. Authenticaion Failed"
        )

    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(user: userDependency, db: dbDependancy, todo_id: int = Path(gt=0)):
    if user is None or user.get("userRole") != "admin":
        raise HTTPException(status_code=401, detail="Authenticaion Failed")

    todoModel = db.query(Todos).filter(Todos.id == todo_id).first()

    if todoModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
