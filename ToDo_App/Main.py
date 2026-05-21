from fastapi import FastAPI
import Models
from Database import engine
from routers import Auth, todos, Admin, Users

app = FastAPI()

Models.Base.metadata.create_all(bind=engine)

# We don't want to create the API endpoints in our Main file, we will instead create them from our routers\
# which are Auth and todos
app.include_router(Auth.router)
app.include_router(todos.router)
app.include_router(Admin.router)
app.include_router(Users.router)
