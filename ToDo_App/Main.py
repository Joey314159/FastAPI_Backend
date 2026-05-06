from fastapi import FastAPI
import Models
from Database import engine

app = FastAPI()

Models.Base.metadata.create_all(bind=engine)
