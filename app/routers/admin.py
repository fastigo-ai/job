from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin
from app.auth import verify_password, create_access_token

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(
        Admin.username == form_data.username
    ).first()

    if not admin or not verify_password(form_data.password, admin.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": admin.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }