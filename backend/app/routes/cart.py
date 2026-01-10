from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.services.cart import CartService
from app.services.dependencies import get_cart_service
from app.security.oauth2 import get_current_user
from app.schemas.cart import AddCartItem


router = APIRouter(prefix="/carts", tags=["carts"])


@router.post("/")
async def add_cart_item(
    add_cart_item: AddCartItem,
    cart_service: Annotated[CartService, Depends(get_cart_service)],
    logged_in_user=Depends(get_current_user),
):
    user_id = logged_in_user.id
    cart = await cart_service.get_cart(user_id)
    if not cart:
        cart = await cart_service.create_cart(user_id)
    try:
        cart_item = await cart_service.add_cart_item(
            cart_id=cart.id,
            menu_id=add_cart_item.menu_id,
            quantity=add_cart_item.quantity,
        )
    except:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add cart item"
        )

    return cart_item
