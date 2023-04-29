import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from database.connect import Base, engine
from datetime import datetime
import passlib.hash as _hash


class Menu(Base):
    __tablename__ = "menu"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    submenus_count = _sql.Column(_sql.Integer, default=0)
    dishes_count = _sql.Column(_sql.Integer, default=0)

    children = _orm.relationship(
        "SubMenu",
        cascade="all,delete",
        backref="parent",
    )


class SubMenu(Base):
    __tablename__ = "submenu"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    menu_id = _sql.Column(_sql.Integer, _sql.ForeignKey("menu.id"))
    dishes_count = _sql.Column(_sql.Integer, default=0)

    children = _orm.relationship(
        "Dish",
        cascade="all,delete",
        backref="parent",
    )


class Dish(Base):
    __tablename__ = "dish"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    submenu_id = _sql.Column(_sql.Integer, _sql.ForeignKey("submenu.id"))
    price = _sql.Column(_sql.String, index=True)


class User(Base):
    __tablename__ = "user"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=datetime.utcnow)

    children = _orm.relationship(
        "Order",
        cascade="all,delete",
        backref="parent",
    )

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class Order(Base):
    __tablename__ = "order"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), index=True)
    dish_id = _sql.Column(_sql.Integer)
    quantity = _sql.Column(_sql.Integer)
    date_created = _sql.Column(_sql.DateTime, default=datetime.utcnow)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
