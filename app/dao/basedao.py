from enum import Enum

from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker
from app.user.model import Users


class CollectionModelDao(Enum):
    users = Users


class BaseDao:
    model = Users

    @classmethod
    async def find_by_id(
        cls,
        model_id: int,
        model: CollectionModelDao = Users,
    ):
        cls.model = model
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, model: CollectionModelDao = Users, **filter_by):
        cls.model = model
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, model: CollectionModelDao = Users, **filter_by):
        cls.model = model
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def add(cls, model: CollectionModelDao = Users, **data):
        cls.model = model
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_one(cls, model: CollectionModelDao = Users, **data):
        cls.model = model
        async with async_session_maker() as session:
            query = update(cls.model).values(**data)  # noqa: F821
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_one(cls, model: CollectionModelDao = Users, **filter_by):
        cls.model = model
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
