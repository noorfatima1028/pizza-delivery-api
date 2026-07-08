from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

from database import Session, engine
from models import Order, User
from schema import OrderModel

order_router = APIRouter(
    prefix="/orders",
    tags=["order"]
)

session = Session(bind=engine)


@order_router.get("/order", status_code=status.HTTP_200_OK)
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return {"message": "Hello, World!"}


@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def place_an_order(
    order: OrderModel,
    Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(
        User.username == current_user
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_order = Order(
        quantity=order.quantity,
        pizza_size=order.pizza_size
    )

    # Associate the order with the logged-in user
    new_order.user = user

    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    response = {
        "id": new_order.id,
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)
