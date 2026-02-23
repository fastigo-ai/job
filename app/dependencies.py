from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin
from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")


def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        admin = db.query(Admin).filter(Admin.username == username).first()
        if admin is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return admin
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")