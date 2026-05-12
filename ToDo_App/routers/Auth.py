from fastapi import APIRouter, Depends
from starlette import status
from pydantic import BaseModel
from Models import Users
from passlib.context import CryptContext
from Database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str
    role: str


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


def authenticateUser(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashedPWD):
        return False
    return True


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def createUser(db: dbDependancy, createUserRequest: CreateUserRequest):
    createUserModel = Users(
        email=createUserRequest.email,
        username=createUserRequest.username,
        firstName=createUserRequest.firstName,
        lastName=createUserRequest.lastName,
        role=createUserRequest.role,
        # We never store the raw password from the user instead we transform into a hash string
        # This means that even if someone got access into our database they would only see the hash
        hashedPWD=bcrypt_context.hash(createUserRequest.password),
        isActive=True,
    )

    db.add(createUserModel)
    db.commit()


@router.post("/token")
async def loginForAcessToken(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDependancy
):
    user = authenticateUser(formData.username, formData.password, db)

    if not user:
        return "Failed Authentication"
    return "Successful Authentication"
