from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import admin, jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Career Connect Backend")

app.include_router(admin.router)
app.include_router(jobs.router)from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.database import engine
from app.models import Base
from app.routers import admin, jobs
import os


# ---------------------------------------------------
# CREATE TABLES (Keep for now, remove if using Alembic)
# ---------------------------------------------------
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Career Connect Backend",
    docs_url="/docs",
    redoc_url=None
)


# ---------------------------------------------------
# CORS CONFIGURATION (IMPORTANT FOR PRODUCTION)
# ---------------------------------------------------

origins = [
    "http://localhost:3000",  # local frontend
    "https://your-frontend.vercel.app",  # production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# TRUSTED HOSTS (SECURITY)
# ---------------------------------------------------

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # replace with your render domain in production
)


# ---------------------------------------------------
# INCLUDE ROUTERS
# ---------------------------------------------------

app.include_router(admin.router)
app.include_router(jobs.router)


# ---------------------------------------------------
# HEALTH CHECK ENDPOINT (VERY IMPORTANT)
# ---------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "API is running"}