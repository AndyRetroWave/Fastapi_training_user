from typing import Annotated

from fastapi import APIRouter, Form, Path, Query
from pydantic import BaseModel, EmailStr
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.dao.basedao import BaseDao
from app.depends.password import check_password, hash_password
from app.exceptions.user_exceptions import (
    PasswordErrorDataException,
    UserNotFound,
    UserPasswordError,
)
from app.user.dao import UserDAO
from app.user.model import Users
from app.user.schemas import SUserReturn, SUsers
from app.user.servis import ServiceUser

router = APIRouter(prefix="/auth", tags=["Пользователи и регистрация"])


@router.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


@router.post("/register")
async def register_user(user: SUsers):
    if await ServiceUser.register_user(user=user):
        return {"message": "User registered successfully"}, HTTP_200_OK
    return {"message": "Registration failed"}, HTTP_401_UNAUTHORIZED


@router.get("/me_info", response_model=SUserReturn)
async def get_user_email(email: EmailStr = Query(...)) -> SUserReturn:
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
    email: EmailStr = Query(...),
    password: str = Query(...),
    user_update: UserUpdate = Form(),
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
            await UserDAO.updata_user_data(
                old_email=email,
                email=user_update.email,
                hashed_password=await hash_password(user_update.password),
                first_name=user_update.first_name,
                last_name=user_update.last_name,
            )
            return SUserReturn(
                first_name=user_update.first_name,
                last_name=user_update.last_name,
                email=user_update.email,
            )
