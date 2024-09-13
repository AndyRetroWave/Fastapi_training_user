from pydantic import BaseModel, EmailStr


class SUsers(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str


class SUserReturn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
