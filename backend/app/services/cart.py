from pyexpat import model
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.models import models


class CartService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_cart(self, user_id: UUID):
        new_cart = models.Cart(user_id=user_id)
        self.session.add(new_cart)
        await self.session.commit()
        await self.session.refresh(new_cart)
        return new_cart

    async def update_cart(self, cart_item):
        pass

    async def add_cart_item(self, cart_item: CartItemCreate):
        new_cart_item = models.CartItem(**cart_item.model_dump())
        self.session.add(new_cart_item)
        await self.session.commit()
        await self.session.refresh(new_cart_item)
        return new_cart_item

    async def update_cart_item(self, cart_item_id: UUID, cart_item: CartItemUpdate):
        stmt = select(models.CartItem).where(models.CartItem.id == cart_item_id)
        result = await self.session.execute(stmt)
        cart_item_obj = result.scalar_one_or_none()
        if not cart_item_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
            )
        update_data = cart_item.model_dump(exclude_unset=True)
        for key, value in update_data:
            setattr(cart_item_obj, key, value)
        await self.session.commit()
        await self.session.refresh(cart_item_obj)
        return cart_item_obj

    async def delete_cart_item(self, cart_item_id: UUID):
        stmt = select(models.CartItem).where(models.CartItem.id == cart_item_id)
        result = await self.session.execute(stmt)
        cart_item_obj = result.scalar_one_or_none()
        if not cart_item_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
            )
        await self.session.delete(cart_item_obj)
        await self.session.commit()
        return {"message": f"Cart Item {id} deleted successfully"}
