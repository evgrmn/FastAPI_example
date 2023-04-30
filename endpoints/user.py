import fastapi as _fastapi
import fastapi.security as _security
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import control.user as _control
from database.connect import session
from models.user import Token, User, User_Data, User_Delete, UserCreate

router = APIRouter()


@router.get(
    "/all",
    response_model=list[User],
    status_code=200,
    summary="A list of users",
)
async def get_users(
    db: AsyncSession = Depends(session),
):
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
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(session),
):
    """
    Create a new user using JWT authentication
    """

    return await _control.create_user(user=user, db=db)


@router.post(
    "/token",
    response_model=Token,
    status_code=200,
    summary="Generate_token",
)
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(session),
):
    """
    User authorization request form
    """
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
    summary="Get current user",
)
async def get_user(
    user: User = Depends(_control.get_current_user),
):
    """
    Get information about current user
    """

    return user


@router.delete(
    "/{menu_id}",
    response_model=User_Delete,
    status_code=200,
    summary="Delete user",
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Delete user
    """

    return await _control.delete_user(
        id=user_id,
        db=db,
    )


@router.patch(
    "/{user_id}",
    response_model=User_Data,
    status_code=200,
    summary="Update user",
)
async def update_user(
    data: User_Data,
    user_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Update a specific user.
    'user_id' - id in the 'user' table,
    'title' - menu title, 'description' - menu description.
    """

    return await _control.update_user(data=data, id=user_id, db=db)
