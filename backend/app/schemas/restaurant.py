from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    address: str
    cuisine: str
    rating: float
