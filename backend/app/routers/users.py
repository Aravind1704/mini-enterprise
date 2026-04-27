from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserOut
from app.core.dependencies import require_role, get_current_user
from fastapi import HTTPException

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    return db.query(User).all()

@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user