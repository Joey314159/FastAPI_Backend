from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel, Field
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


class UserVerification(BaseModel):
    password: str
    newPassword: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def getUser(user: userDependency, db: dbDependancy):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def changePassword(
    user: userDependency, db: dbDependancy, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    userModel = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(user_verification.password, userModel.hashedPWD):
        raise HTTPException(status_code=401, detail="Authentication failed")

    userModel.hashedPWD = bcrypt_context.hash(user_verification.newPassword)

    db.add(userModel)
    db.commit()


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def changePhoneNumber(user: userDependency, db: dbDependancy, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    userModel = db.query(Users).filter(Users.id == user.get("id")).first()
    userModel.phone_number = phone_number

    db.add(userModel)
    db.commit()
