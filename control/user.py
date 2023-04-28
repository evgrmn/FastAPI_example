import fastapi as _fastapi

import fastapi.security as _security
import database.models as table
from caching import functions as cache
from models.user import User, UserCreate, User_Delete, User_Data
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import session
import sqlalchemy as _sql
import email_validator as _email_check
import passlib.hash as _hash
import jwt as _jwt


_JWT_SECRET = "donotthinkaboutit"
oath2schema = _security.OAuth2PasswordBearer("/api/v1/user/token")


async def get_users(db: AsyncSession):
    key_name = f"User_list"
    user_list = await cache.get(key_name)
    if user_list:
        user_list = list(map(lambda x: x, user_list.values()))
        return user_list
    user_list = await db.execute(_sql.select(table.User))
    user_list = list(map(User.from_orm, user_list.scalars().all()))
    user_dict = {}
    for n, user in enumerate(user_list):
        user_dict[n] = user.dict()
        user_dict[n]['date_created'] = user_dict[n]['date_created'].strftime("%Y-%m-%dT%H:%M:%S.%f")
    await cache.set(key_name, user_dict)

    return user_list


async def create_user(user: UserCreate, db: AsyncSession):
    try:
        db_user = await db.execute(_sql.select(table.User).filter_by(email=user.email))
        db_user = db_user.scalars().one()
    except Exception:
        # check that email is valid
        try:            
            valid = _email_check.validate_email(email=user.email)
            email = valid.email
        except _email_check.EmailNotValidError:
            raise _fastapi.HTTPException(
                status_code=404, detail="Please enter a valid email"
            )        
        hashed_password = _hash.bcrypt.hash(user.password)        
        user = table.User(email=email, hashed_password=hashed_password)
        db.add(user)
        await db.commit()
        await cache.delete("User_list")
        user_dict = user.__dict__
        user_dict['date_created'] = user_dict['date_created'].strftime("%Y-%m-%dT%H:%M:%S.%f")
        del user_dict['_sa_instance_state']
        await cache.set(f"User_{user.id}", user_dict)

        return user
    else:
        raise _fastapi.HTTPException(
            status_code=400, detail="User with that email already exists"
        )


async def get_current_user(
    db: AsyncSession = _fastapi.Depends(session),
    token: str = _fastapi.Depends(oath2schema),
):
    payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
    current_user = await cache.get(f"User_{payload['id']}")
    if current_user:
        return current_user
    try:
        current_user = await db.execute(_sql.select(table.User).filter_by(id=payload["id"]))
        current_user = current_user.scalars().one()
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid email or password"
        )
    user_dict = current_user.__dict__
    user_dict['date_created'] = user_dict['date_created'].strftime("%Y-%m-%dT%H:%M:%S.%f")
    del user_dict['_sa_instance_state']
    await cache.set(f"User_{current_user.id}", user_dict)

    return User.from_orm(current_user)


async def get_user_by_email(email: str, db: AsyncSession):
    try:
        user = await db.execute(_sql.select(table.User).filter_by(email=email))
        user = user.scalars().one()
    except:
        raise _fastapi.HTTPException(
            status_code=404, detail="User not fount"
        )

    return user


async def authenticate_user(email: str, password: str, db: AsyncSession):
    user = await get_user_by_email(email=email, db=db)
    if not user:
        return False
    if not user.verify_password(password=password):
        return False

    return user


async def create_token(user: table.User):
    user_schema_obj = User.from_orm(user)
    user_dict = user_schema_obj.dict()
    del user_dict["date_created"]
    token = _jwt.encode(user_dict, _JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def delete_user(
    id: int,
    db: AsyncSession,
):
    try:
        user = await db.execute(_sql.select(table.User).filter_by(id=id))
        await db.delete(user.scalars().one())
        await db.commit()
    except Exception:
        raise _fastapi.HTTPException(status_code=404, detail="user not found")
    await cache.delete_cascade(f"*User_{id}*")
    response = User_Delete
    response.status = True
    response.message = "The user has been deleted"
    await cache.delete("User_list")

    return User_Delete.from_orm(response)



async def update_user(
    data: User_Data,
    id: int,
    db: AsyncSession,
): 
    try:
        user = await db.execute(_sql.select(table.User).filter_by(id=id))
        user = user.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"user {id} not found",
        )
    # check that email is valid
    try:            
        _email_check.validate_email(email=data.email)
    except _email_check.EmailNotValidError:
        raise _fastapi.HTTPException(
            status_code=404, detail="Please enter a valid email"
        )   
    data = data.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(user, key, value)
    await db.commit()
    user_dict = user.__dict__
    user_dict['date_created'] = user_dict['date_created'].strftime("%Y-%m-%dT%H:%M:%S.%f")
    del user_dict['_sa_instance_state']
    await cache.set(f"User_{id}", user_dict)
    await cache.delete("User_list")

    return data
