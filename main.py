from fastapi import FastAPI
from app.utils.init_db import create_tables
from contextlib import asynccontextmanager

# In lifespan function before yield events happen at the start of app and after yield events happen at closing time of the application

@asynccontextmanager #TODO : Learn about this
async def lifespan(app:FastAPI):
    print("created")
    create_tables()
    yield # Seperation Point

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "Running..."}
