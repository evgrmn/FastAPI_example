import fastapi as _fastapi

import fastapi.security as _security
import database.models as table
from caching import functions as cache
from models.user import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import session
import sqlalchemy as _sql
import email_validator as _email_check
import passlib.hash as _hash
import jwt as _jwt


_JWT_SECRET = "donotthinkaboutit7"
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
        user_obj = table.User(email=email, hashed_password=hashed_password)
        db.add(user_obj)
        await db.commit()
        await cache.delete("User_list")
        user_dict = user_obj.__dict__
        user_dict['date_created'] = user_dict['date_created'].strftime("%Y-%m-%dT%H:%M:%S.%f")
        del user_dict['_sa_instance_state']
        await cache.set(f"User_{user_obj.id}", user_obj.__dict__)
        return user_obj
    else:
        raise _fastapi.HTTPException(
            status_code=400, detail="User with that email already exists"
        )


async def get_current_user(
    db: AsyncSession = _fastapi.Depends(session),
    token: str = _fastapi.Depends(oath2schema),
):
    try:        
        payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        print(payload)
        current_user = await cache.get(f"User_{payload['id']}")
        if current_user:
            print('------- current_user --------', current_user)
            return current_user
        user = await db.execute(_sql.select(table.User).filter_by(id=payload["id"]))
        user = user.scalars().one()
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid email or password"
        )
    return User.from_orm(user)


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
