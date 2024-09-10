from sqlalchemy import insert, update
from sqlalchemy.exc import SQLAlchemyError

from app.dao.basedao import BaseDao
from app.database import async_session_maker
from app.logger import logger
from app.user.model import Users


class UserDAO(BaseDao):
    model = Users

    @classmethod
    async def set_user(
        cls, first_name: str, last_name: str, email: str, password: str
    ) -> None:
        try:
            async with async_session_maker() as session:
                user = insert(cls.model).values(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    hashed_password=password,
                    is_active=True,
                )
                await session.execute(user)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "SQLAlchemyError"
            elif isinstance(e, Exception):
                msg = "Unknown error"
            msg += ": Cannot add user"
            extra = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
            }
            logger.error(msg, extra=extra)

    @classmethod
    async def updata_user_data(cls, old_email: str, **kwargs) -> None:
        async with async_session_maker() as session:
            query = (
                update(cls.model).where(cls.model.email == old_email).values(**kwargs)
            )
            await session.execute(query)
            await session.commit()
