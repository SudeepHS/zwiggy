from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.restaurant import RestaurantCreate
from app.models import models
from app.security import utils


class RestaurantService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_restaurant(self, restaurant: RestaurantCreate):
        new_restaurant = models.Restaurant(**restaurant.model_dump())
        self.db.add(new_restaurant)
        await self.db.commit()
        await self.db.refresh(new_restaurant)
        return new_restaurant
