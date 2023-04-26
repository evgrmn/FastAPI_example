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
    res = await db.execute(_sql.select(table.User))

    return list(map(User.from_orm, res.scalars().all()))


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
