from fastapi import FastAPI

# Allows uvicorn understand that we are creating a new app object
app = FastAPI()


@app.get("/")
async def firstFN():
    return {"Message ": "Hello World"}
