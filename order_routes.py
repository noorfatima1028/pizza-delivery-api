from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from database import Session, engine
from models import Order, User
from schema import OrderModel, OrderStatusModel

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

session = Session(bind=engine)


@order_router.get("/order", status_code=status.HTTP_200_OK)
async def hello(Authorize: AuthJWT = Depends()):

    """
    ## A sample hello world route
    this returns Hello world
    """
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
    """
    ## Placing an order
    This requires the following
    -quantity: integer
    -pizza_size: str
    """
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


@order_router.get("/orders", status_code=status.HTTP_200_OK)
async def list_all_orders(
    Authorize: AuthJWT = Depends()
):
    """
    ##list all orders 
    this lists all orders made.It can be assesed by super users. """

    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    current_username = Authorize.get_jwt_subject()

    user = session.query(User).filter(
        User.username == current_username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )

    orders = session.query(Order).all()

    return jsonable_encoder(orders)


@order_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_order(
    id: int,
    Authorize: AuthJWT = Depends()
):
    """
    ## get an order by its ID
    This gets its order by an ID and is only assesed by a superuser"""

    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    current_username = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(
        User.username == current_username
    ).first()

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )

    order = session.query(Order).filter(
        Order.id == id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {id} not found"
        )

    return jsonable_encoder(order)


@order_router.get("/user/orders", status_code=status.HTTP_200_OK)
async def get_user_order(
    Authorize: AuthJWT = Depends()
):
    """
    ## get a current user's orders
    This lists the orders made by the currently logged in users
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(
        User.username == user
    ).first()

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return jsonable_encoder(current_user.orders)


@order_router.get("/user/order/{id}", status_code=status.HTTP_200_OK)
async def get_specific_order(
    id: int,
    Authorize: AuthJWT = Depends()
):
    
    """
    ## Get a specific order by a currently logged in user
    This returns an order by ID for the currently logged in user
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    subject = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(
        User.username == subject
    ).first()

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    orders = current_user.orders

    for order in orders:
        if order.id == id:
            return jsonable_encoder(order)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with such id"
    )

@order_router.put("/order/update/{id}", status_code=status.HTTP_200_OK)
async def update_order(
    id: int,
    order: OrderModel,
    Authorize: AuthJWT = Depends()
): 
    """
     ##Updating an order
      This updates an order and requires the following fields
      -quantity: integer
      -pizza_size: str
      """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    order_to_update = session.query(Order).filter(
        Order.id == id
    ).first()

    if order_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size

    session.commit()
    session.refresh(order_to_update)

    return jsonable_encoder(order_to_update)

@order_router.patch("/order/update/{id}/", status_code=status.HTTP_200_OK)
async def update_order_status(
    id: int,
    order: OrderStatusModel,
    Authorize: AuthJWT = Depends()
):
    """
    ##update an order's status
     This is for updating an orders status and requires order_status in str
     """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    username = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(
        User.username == username
    ).first()

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )

    order_to_update = session.query(Order).filter(
        Order.id == id
    ).first()

    if order_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    order_to_update.order_status = order.order_status

    session.commit()
    session.refresh(order_to_update)

    return jsonable_encoder(order_to_update)

@order_router.delete("/order/delete/{id}/", status_code=status.HTTP_200_OK)
async def delete_an_order(
    id: int,
    Authorize: AuthJWT = Depends()
):
    """
    # Delete an order
    This delets an order by its ID
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    order_to_delete = session.query(Order).filter(
        Order.id == id
    ).first()

    if order_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    session.delete(order_to_delete)
    session.commit()

    return jsonable_encoder(order_to_delete)