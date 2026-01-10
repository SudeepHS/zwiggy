from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class AddCartItem(BaseModel):
    menu_id: UUID
    quantity: int


class CartUpdate(BaseModel):
    total_amount: float


class CartItemCreate(BaseModel):
    cart_id: UUID
    menu_id: UUID
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int
