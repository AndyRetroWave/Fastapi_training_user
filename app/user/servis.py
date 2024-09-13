from app.dao.basedao import BaseDao
from app.depends.password import hash_password
from app.user.dao import UserDAO
from app.user.model import Users


class ServiceUser:
    """
    Класс по регистрации и авторизации пользователя
    """

    @classmethod
    async def register_user(cls, user: Users):
        if await BaseDao.find_one_or_none(email=user.email) is None:
            password: str = await hash_password(user.hashed_password)
            if password:
                await UserDAO.set_user(
                    user.first_name, user.last_name, user.email, password
                )
                return True
        return False
