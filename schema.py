from typing import Optional
from pydantic import BaseModel


class SignupModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: bool = False
    is_active: bool = True

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "johndoe@gmail.com",
                "password": "1234",
                "is_staff": False,
                "is_active": True
            }
        }