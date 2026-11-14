from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, Base
from app.models import User, Job
from app.routers import users, jobs, files
app = FastAPI(title="Job Management API")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(files.router)

print("\nFiles router endpoints:")

for route in files.router.routes:
    print(route.path, route.methods)

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


print("\nRegistered routes:")

for route in app.routes:
    print(route)