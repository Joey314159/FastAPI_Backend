from fastapi import APIRouter
from pydantic import BaseModel
from Models import Users

router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str
    role: str


@router.post("/auth")
async def createUser(createUserRequest: CreateUserRequest):
    createUserModel = Users(
        email=createUserRequest.email,
        username=createUserRequest.username,
        firstName=createUserRequest.firstName,
        lastName=createUserRequest.lastName,
        role=createUserRequest.role,
        hashedPWD=createUserRequest.password,
        isActive=True,
    )

    return createUserModel
