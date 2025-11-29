from typing import Dict
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantAdminAdd,
)
from app.models import models


class RestaurantService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_restaurant_by_id(self, id: UUID):
        stmt = select(models.Restaurant).where(models.Restaurant.id == id)
        restaurant = (await self.session.execute(stmt)).scalar_one_or_none()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
            )
        return restaurant

    async def get_all_restaurants(self):
        restaurants = (
            (await self.session.execute(select(models.Restaurant))).scalars().all()
        )
        return restaurants

    async def create_restaurant(self, restaurant: RestaurantCreate):
        new_restaurant = models.Restaurant(**restaurant.model_dump())
        self.session.add(new_restaurant)
        await self.session.commit()
        await self.session.refresh(new_restaurant)
        return new_restaurant

    async def update_restaurant(self, id: UUID, restaurant: RestaurantUpdate):
        stmt = select(models.Restaurant).where(models.Restaurant.id == id)
        restaurant_obj = (await self.session.execute(stmt)).scalar_one_or_none()
        if not restaurant_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
            )
        update_data: Dict = restaurant.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(restaurant_obj, key, value)
        await self.session.commit()
        await self.session.refresh(restaurant_obj)
        return restaurant_obj

    async def delete_restaurant(self, id: UUID):
        stmt = select(models.Restaurant).where(models.Restaurant.id == id)
        restaurant = (await self.session.execute(stmt)).scalar_one_or_none()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
            )
        await self.session.delete(restaurant)
        await self.session.commit()
        return {"message": f"Restaurant {id} deleted successfully"}

    async def add_restaurant_admin(self, admin_data: RestaurantAdminAdd):
        new_admin = models.RestaurantAdmin(
            user_id=admin_data.user_id, restaurant_id=admin_data.restaurant_id
        )
        self.session.add(new_admin)
        await self.session.commit()
        await self.session.refresh(new_admin)
        return {"msg": "Admin added successfully"}
