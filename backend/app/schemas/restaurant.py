from typing import Optional
from pydantic import BaseModel


class Restaurant(BaseModel):
    name: str
    address: str
    cuisine: str


class RestaurantCreate(Restaurant):
    pass


class RestaurantUpdate(Restaurant):
    name: Optional[str] = None
    address: Optional[str] = None
    cuisine: Optional[str] = None
