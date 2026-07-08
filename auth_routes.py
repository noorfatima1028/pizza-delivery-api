from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from database import Session, engine
from models import User
from schema import SignupModel, LoginModel
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session = Session(bind=engine)


@auth_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return {"message": "Hello, World!"}


@auth_router.post(
    "/signup",
    response_model=SignupModel,
    status_code=status.HTTP_201_CREATED
)
async def signup(user: SignupModel):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists"
        )

    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username {user.username} already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@auth_router.post("/login")
async def login(
    user: LoginModel,
    Authorize: AuthJWT = Depends()
):
    db_user = session.query(User).filter(
        User.username == user.username
    ).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(
            subject=db_user.username
        )
        refresh_token = Authorize.create_refresh_token(
            subject=db_user.username
        )

        return jsonable_encoder({
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid username or password"
    )


@auth_router.get("/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    current_user = Authorize.get_jwt_subject()

    new_access_token = Authorize.create_access_token(
        subject=current_user
    )

    return jsonable_encoder({
        "access_token": new_access_token
    })