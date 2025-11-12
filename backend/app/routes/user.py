from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import models
from app.schemas.schemas import UserCreate
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    try:
        new_user = user_service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_user


@router.get("/")
def get_all_users(db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    users = user_service.get_all_users()
    if not users:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users
