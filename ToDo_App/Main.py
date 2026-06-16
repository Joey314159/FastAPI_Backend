from fastapi import FastAPI
from .Models import Base
from .Database import engine
from .routers import Auth, todos, Admin, Users

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Health Check API which checks to see if the application is up and running
@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


# We don't want to create the API endpoints in our Main file, we will instead create them from our routers\
# which are Auth and todos
app.include_router(Auth.router)
app.include_router(todos.router)
app.include_router(Admin.router)
app.include_router(Users.router)
