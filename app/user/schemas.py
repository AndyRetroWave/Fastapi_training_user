from pydantic import BaseModel, EmailStr


class SUsers(BaseModel):
    id: int
    first_name: str
    family_nam: str
    emai: EmailStr
    hashed_passwor: str
    is_activ: bool


class SUserReturn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
