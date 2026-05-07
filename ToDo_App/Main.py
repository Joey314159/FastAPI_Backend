from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import Models
from Models import Todos
from Database import SessionLocal, engine

app = FastAPI()

Models.Base.metadata.create_all(bind=engine)


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def readAll(db: Annotated[Session, Depends(getDB)]):
    return db.query(Todos).all()
