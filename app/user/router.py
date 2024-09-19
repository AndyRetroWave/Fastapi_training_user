from fastapi import APIRouter, HTTPException
from pydantic import EmailStr
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.dao.basedao import BaseDao
from app.user.model import Users
from app.user.schemas import SUserReturn, SUsers
from app.user.servis import ServiceUser

router = APIRouter(prefix="/auth", tags=["Пользователи и регистрация"])


@router.post("/register")
async def register_user(user: SUsers):
    if await ServiceUser.register_user(user=user):
        return {"message": "User registered successfully"}, HTTP_200_OK
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Ошибка регистрации!")


@router.get("/me_info")
async def get_user_email(email: EmailStr) -> SUserReturn:
    user: Users = await BaseDao.get_all(email=email)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Пользователь не найден!"
        )
    return SUserReturn(user.first_name, user.last_name, user.email)


@router.patch("/substitute-data_user")
async def substitute_data_user(
    email: EmailStr,
    password: str,
    user_update: SUsers,
) -> SUserReturn:
    if not await ServiceUser.changing_user_data(email, password, user_update):
        raise HTTPException(HTTP_401_UNAUTHORIZED, "Ошибка введенных данных!")
    return SUserReturn(
        first_name=user_update.first_name,
        last_name=user_update.last_name,
        email=user_update.email,
    )
