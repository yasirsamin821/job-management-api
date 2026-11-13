from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, Base
from app.models import User, Job
from app.routers import users, jobs

app = FastAPI(title="Job Management API")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(jobs.router)

@app.get("/")
def home():
    return {"message": "Job Management API is running!"}

@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}