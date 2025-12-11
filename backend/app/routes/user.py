from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import user
from app.services.user import UserService
from app.security.oauth2 import get_current_user
from app.services.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=user.UserResponse)
async def create_user(
    user: user.UserCreate,
    user_service: UserService = Depends(get_user_service),
    logged_in_user=Depends(get_current_user),
):
    try:
        new_user = await user_service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_user


@router.get("/")
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
    logged_in_user=Depends(get_current_user),
):
    users = await user_service.get_all_users()
    if not users:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users
