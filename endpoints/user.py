from fastapi import APIRouter, Depends
import fastapi as _fastapi

import control.user as _control
from models.user import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import session
import fastapi.security as _security


router = APIRouter()


@router.get(
    "/all",
    response_model=list[User],
    status_code=200,
    summary="A list of users",
)
async def get_users(db: AsyncSession = Depends(session),):
    """
    Get a list of all registered users
    """

    return await _control.get_users(db=db)


@router.post(
    "/new",
    response_model=User,
    status_code=201,
    summary="Create a new user",
)
async def create_user(user: UserCreate,  db: AsyncSession = Depends(session),):
    """
    Create a new user using JWT authentication
    """

    return await _control.create_user(user=user, db=db)


@router.post("/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(session),
):
    user = await _control.authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _control.create_token(user=user)


@router.get(
    "/me", 
    response_model=User, 
    status_code=200, 
    summary="Get current user",)
async def get_user(user: User = Depends(_control.get_current_user),):
    """
    Get information about current user
    """

    return user