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


class Settings(BaseModel):
    authjwt_secret_key: str = "0186fc50a2516f84b5c0b13650b38882480fcdfdf3fac091b09badb8fd25243a"


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    quantity: int
    order_status: Optional[str] = "pending"
    pizza_size: Optional[str] = "small"
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "large"
            }
        }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "PENDING"
            }
        }