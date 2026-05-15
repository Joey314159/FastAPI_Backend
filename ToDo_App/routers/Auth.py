from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from pydantic import BaseModel
from Models import Users
from passlib.context import CryptContext
from Database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


router = APIRouter(prefix="/auth", tags=["auth"])

# Obtained this string by typing in the terminal the following command:  openssl rand -hex 32
SECRET_KEY = "2ee739d3cd6b1d67debe8011b8ff68538766d78685778f4cb45b74af287fc273"

ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2Bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str
    role: str


"""
    Here the field names 'access_token' and 'token_type' are REQUIRED by the OAuth2 specification. When Swagger's 
    "Authorize" button calls /auth/token, it parses the JSON response and looks for a key LITERALLY named "access_token". 
    If it finds "accessToken" instead, it doesn't  recognize it, stores nothing, and every subsequent request goes 
    out with no token — causing a 401 Unauthorized.

    Rule of thumb:
        - Your own internal variables → name them whatever you want
        - Fields that get serialized into JSON for an external system/spec → names are non-negotiable
"""


class Token(BaseModel):
    access_token: str
    token_type: str


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
    return user


def createAccessToken(username: str, userID: int, expiresDelta: timedelta):
    encode = {"sub": username, "id": userID}
    expires = datetime.now(timezone.utc) + expiresDelta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def getCurrentUser(token: Annotated[str, Depends(oauth2Bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        userID: int = payload.get("id")

        if username is None or userID is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return {"username": username, "userID": userID}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.post("/token", response_model=Token)
async def loginForAcessToken(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDependancy
):
    user = authenticateUser(formData.username, formData.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    token = createAccessToken(user.username, user.id, timedelta(minutes=20))

    # Here like we mentioned above 'access_token' and token_type are non-negotiable returns
    return {"access_token": token, "token_type": "bearer"}
