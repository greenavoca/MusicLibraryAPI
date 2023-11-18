from fastapi import FastAPI
from pydantic import BaseModel
import models
from database import engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
