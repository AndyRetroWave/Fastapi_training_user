from app.dao.basedao import BaseDao
from app.depends.password import check_password, hash_password
from app.user.dao import UserDAO
from app.user.model import Users
from app.user.schemas import SUserReturn, SUsers


class ServiceUser:
    """
    Класс по регистрации и авторизации пользователя
    """

    @classmethod
    async def register_user(cls, user: Users) -> bool:
        if await BaseDao.find_one_or_none(email=user.email) is None:
            password: str = await hash_password(user.hashed_password)
            if password:
                await UserDAO.set_user(
                    user.first_name, user.last_name, user.email, password
                )
                return True
        return False

    @classmethod
    async def changing_user_data(
        cls, old_email: str, old_password: str, update_user: SUsers
    ) -> SUserReturn | None:
        data_user_result: Users = await BaseDao.find_one_or_none(email=old_email)
        if (
            data_user_result is None
            or await check_password(old_password, data_user_result.hashed_password)
            is False
            or await hash_password(update_user.hashed_password) is None
        ):
            return None
        await UserDAO.updata_user_data(
            old_email=old_email,
            email=update_user.email,
            hashed_password=await hash_password(update_user.hashed_password),
            first_name=update_user.first_name,
            last_name=update_user.last_name,
        )
        return SUserReturn(
            first_name=update_user.first_name,
            last_name=update_user.last_name,
            email=update_user.email,
        )
