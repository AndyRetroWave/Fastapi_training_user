from pydantic import BaseModel, EmailStr


class SUsers(BaseModel):
    id: int
    given_nam: str
    family_nam: str
    emai: EmailStr
    hashed_passwor: str
    is_activ: bool
