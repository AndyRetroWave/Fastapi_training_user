import asyncio
import json

import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.user.model import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def open_mock_json(model: str):
        with open("app/tests/mock_data_user.json") as f:
            return json.load(f)

    user_mock = await open_mock_json("user")

    async with async_session_maker() as session:
        for user in user_mock:
            add_users = insert(Users).values(user)
            await session.execute(add_users)
            await session.commit()
    yield


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
