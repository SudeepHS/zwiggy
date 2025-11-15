from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import user
from app.models import models
from app.security import utils


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user: user.UserCreate):
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_all_users(self):
        return (await self.session.execute(select(models.User))).scalars().all()
