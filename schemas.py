import pydantic as _pydantic


class Id(_pydantic.BaseModel):
    id: str
    title: str
    description: str

    class Config:
        orm_mode = True


class Common(_pydantic.BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Menu(Id):
    submenus_count: int
    dishes_count: int


class SubMenu(Id):
    dishes_count: int


class Dish(Id):
    price: str


class HandleDish(Common):
    price: str


class Delete(_pydantic.BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True
