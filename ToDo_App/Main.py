from fastapi import FastAPI, Request
from .Models import Base
from .Database import engine
from .routers import Auth, todos, Admin, Users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="ToDo_App/templates")

app.mount("/static", StaticFiles(directory="ToDo_App/static"), name="static")


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse(request, "home.html")


# This is the old convention down here that will eventually depricate
# return templates.TemplateResponse("home.html", {"request": request})


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
