from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import models
from app.schemas import user
from app.services.user import UserService
from app.security.oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=user.UserResponse)
async def create_user(user: user.UserCreate, session: AsyncSession = Depends(get_db)):
    user_service = UserService(session)
    try:
        new_user = await user_service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_user


@router.get("/")
async def get_all_users(
    session: AsyncSession = Depends(get_db), user=Depends(get_current_user)
):
    user_service = UserService(session)
    users = await user_service.get_all_users()
    if not users:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users
