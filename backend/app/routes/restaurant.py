from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED
from app.db import get_db
from app.security.oauth2 import get_current_user
from app.models.models import RestaurantAdmin, User
from app.schemas import restaurant
from app.services.restaurant import RestaurantService
from app.services.dependencies import get_restaurant_service

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.post("/")
async def create_restaurant(
    restaurant: restaurant.RestaurantCreate,
    session: AsyncSession = Depends(get_db),
    logged_in_user=Depends(get_current_user),
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    stmt = select(User).where(User.id == logged_in_user.id)
    user = (await session.execute(stmt)).scalar_one_or_none()
    if user.role != "restaurant":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please user restaurant account to create restaurnt",
        )

    new_restaurant = await restaurant_service.create_restaurant(restaurant)
    await restaurant_service.add_restaurant_admin(
        restaurant.RestaurantAdminAdd(
            restaurant_id=new_restaurant.id,
            user_id=logged_in_user.id,
        )
    )
    return new_restaurant


@router.get("/{id}")
async def get_restaurant_by_id(
    id: UUID,
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    return await restaurant_service.get_restaurant_by_id(id)


@router.get("/")
async def get_all_restaurants(
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    return await restaurant_service.get_all_restaurants()


@router.patch("/{id}")
async def update_restaurant(
    id: UUID,
    restaurant: restaurant.RestaurantUpdate,
    logged_in_user=Depends(get_current_user),
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    return await restaurant_service.update_restaurant(id, restaurant)


@router.delete("/{id}")
async def delete_restaurant(
    id: UUID,
    logged_in_user=Depends(get_current_user),
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    return await restaurant_service.delete_restaurant(id)


@router.post("/admins")
async def add_restaurant_admin(
    admin_data: restaurant.RestaurantAdminAdd,
    session: AsyncSession = Depends(get_db),
    logged_in_user=Depends(get_current_user),
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    stmt = select(RestaurantAdmin.user_id).where(
        RestaurantAdmin.restaurant_id == admin_data.restaurant_id
    )
    restaurant_admins = (await session.execute(stmt)).scalars().all()
    if UUID(logged_in_user.id) not in restaurant_admins:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to do this",
        )
    return await restaurant_service.add_restaurant_admin(admin_data)
