from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from app.dao.basedao import BaseDao
from app.depends.password import check_password, hash_password
from app.exceptions.user_exceptions import (
    PasswordErrorDataException,
    UserErrorAdd,
    UserNotFound,
    UserPasswordError,
)
from app.user.dao import UserDAO
from app.user.model import Users
from app.user.schemas import SUserReturn

router = APIRouter(prefix="/auth", tags=["Пользователи и регистрация"])


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


@router.post("/regiter", response_model=SUserReturn)
async def register_user(
    first_name: str, last_name: str, email: EmailStr, password: str
) -> SUserReturn:
    if await BaseDao.find_one_or_none(email=email) is None:
        password: str = await hash_password(password)
        if password:
            await UserDAO.set_user(first_name, last_name, email, password)
        else:
            raise PasswordErrorDataException()
        return SUserReturn(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
    else:
        raise UserErrorAdd()


@router.get("/me_info", response_model=SUserReturn)
async def get_user_email(email: EmailStr) -> SUserReturn:
    user: Users = await BaseDao.get_all(email=email)
    if user is None:
        raise UserNotFound()
    else:
        return SUserReturn(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )


@router.patch("/substitute-data_user", response_model=SUserReturn)
async def substitute_data_user(
    email: EmailStr, password: str, user_update: UserUpdate
) -> SUserReturn:
    data_user_result: Users = await BaseDao.find_one_or_none(email=email)
    if data_user_result is None:
        raise UserNotFound()
    elif await check_password(password, data_user_result.hashed_password) is False:
        raise UserPasswordError()
    else:
        if await hash_password(user_update.password) is None:
            raise PasswordErrorDataException()
        else:
            await BaseDao.update_one(
                first_name=user_update.first_name,
                last_name=user_update.last_name,
                email=user_update.email,
                hashed_password=await hash_password(user_update.password),
            )
            return SUserReturn(
                first_name=user_update.first_name,
                last_name=user_update.last_name,
                email=user_update.email,
            )
