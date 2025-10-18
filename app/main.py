from fastapi import FastAPI
from .models import URL
from .database import engine , create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database and tables...")
    create_db_and_tables()
    yield
    


app = FastAPI(lifespan=lifespan)

@app.get('/')
def root():
    return {"msg":"Hello world!"}

