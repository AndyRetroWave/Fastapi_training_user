import pytest
from httpx import AsyncClient

from main import app


@pytest.fixture
async def ac():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "first_name, last_name, email, password,   status_code",
    [("Andrey", "Killer", "dinocowww@gmail.com", "Andreykiller566576!", 200)],
)
async def test_register(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    status_code: int,
    ac: AsyncClient,
):
    response = await ac.post(
        url="/auth/register",
        data={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize("email, status_code", [("dinocowww@gmail.com", 200)])
async def test_me_info(email: str, status_code: int, ac: AsyncClient):
    response = await ac.get(url="/auth/me_info", params=dict(email=email))
    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "old_email, old_password, first_name, last_name, email, password, status_code",
    [
        (
            "dinocowww@gmail.com",
            "Andreykiller566576!",
            "Andrey2",
            "Killer2",
            "dinocowww2@gmail.com",
            "Andreykiller566576!",
            200,
        )
    ],
)
async def test_substutute_data_user(
    old_email: str,
    old_password: str,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    status_code: int,
    ac: AsyncClient,
):
    response = await ac.patch(
        url="/auth/substitute-data_user",
        params=dict(email=old_email, password=old_password),
        data=dict(
            first_name=first_name, last_name=last_name, email=email, password=password
        ),
    )
    assert response.status_code == status_code
