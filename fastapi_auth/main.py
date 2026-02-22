from fastapi import FastAPI, Depends
from app.utils.init_db import create_tables
from contextlib import asynccontextmanager
from app.router.auth import authRouter
from app.db.schemas.user import UserOutput
from app.utils.protectedRoute import get_current_user

# In lifespan function before yield events happen at the start of app and after yield events happen at closing time of the application

@asynccontextmanager #TODO : Learn about this
async def lifespan(app:FastAPI):
    print("created")
    create_tables()
    yield # Seperation Point

app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=['auth'], prefix='/auth')

@app.get("/health")
def health_check():
    return {"status": "Running..."}

@app.get("/protected")
def read_protected(user: UserOutput = Depends(get_current_user)) -> UserOutput:
    return {"data": user}
