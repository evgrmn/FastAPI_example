from datetime import datetime


class Variables:
    id: str
    title: str
    description: str
    submenu_id: str
    submenu_title: str
    submenu_description: str
    dish_id: str
    dish_title: str
    dish_description: str
    dish_price: str
    submenu_count: int = 0
    dish_count: int = 0
    menu_dish_count: int = 0
    user_id: str = ""
    email: str = "email"
    created: datetime = datetime.utcnow()
    superuser: bool = True
