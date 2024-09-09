from fastapi import HTTPException


class UserExceptions(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserErrorAdd(UserExceptions):
    status_code = 401
    detail = "Такой пользователь уже зарегестрирован!"


class PasswordErrorDataException(UserExceptions):
    statues_code = 401
    detail = "Пароль должен быть не менее 8 цифр, содержать заглавную и стручную будку, цыфру и специальный симвл!"


class UserNotFound(UserExceptions):
    status_code = 404
    detail = "Пользователь не найден!"


class UserPasswordError(UserExceptions):
    status_code = 401
    detail = "Пароль не верный!"
