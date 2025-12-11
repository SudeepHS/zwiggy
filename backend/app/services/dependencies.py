from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.services.restaurant import RestaurantService
from app.services.user import UserService


def get_restaurant_service(session: AsyncSession = Depends(get_db)):
    return RestaurantService(session)


def get_user_service(session: AsyncSession = Depends(get_db)):
    return UserService(session)
