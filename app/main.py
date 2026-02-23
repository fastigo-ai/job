from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import admin, jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Career Connect Backend")

app.include_router(admin.router)
app.include_router(jobs.router)