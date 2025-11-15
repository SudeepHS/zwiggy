from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import models
from app.security.utils import verify
from app.security.oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    stmt = select(models.User).where(models.User.email == user_credentials.username)
    user = (await session.execute(stmt)).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = create_access_token(
        data={"user_id": str(user.id), "user_role": user.role}
    )

    return {"token": access_token, "type": "bearer"}
