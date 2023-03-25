from __future__ import annotations

import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

from config.config import Env

DATABASE_URL = Env.DB_URL
engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base: _declarative = _declarative.declarative_base()


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


def drop_tables():
    Base.metadata.drop_all(bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


db = SessionLocal()
db.close()


create_tables()
