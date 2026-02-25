from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from app.database import engine,SessionLocal
from app.models import Base, Admin
from app.auth import hash_password
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
    "http://localhost:8081",  # local frontend
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
@app.on_event("startup")
def create_default_admin():
    db: Session = SessionLocal()

    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    existing_admin = db.query(Admin).filter(
        Admin.username == admin_username
    ).first()

    if not existing_admin:
        new_admin = Admin(
            username=admin_username,
            password=hash_password(admin_password)
        )
        db.add(new_admin)
        db.commit()
        print("Default admin created")

    db.close()

app.include_router(admin.router)
app.include_router(jobs.router)


# ---------------------------------------------------
# HEALTH CHECK ENDPOINT (VERY IMPORTANT)
# ---------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "API is running"}