from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from Models import Users
from Database import SessionLocal
from .Auth import getCurrentUser

# Will be used to create a new hash since we are dealing with passwords
from passlib.context import CryptContext

router = APIRouter(prefix="/user", tags=["user"])


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
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def getUser(user: userDependency, db: dbDependancy):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Users).filter(Users.id == user.get("id")).first()
