from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import schemas
from app.models import models
from app.security import utils


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def create_user(self, user: schemas.UserCreate):
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.model_dump())
        self.db.add(new_user)
        print(new_user.role)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_all_users(self):
        return self.db.query(models.User).all()
