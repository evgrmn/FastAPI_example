# FastAPI_example
Description:

- API task: Restaurant menu
- Three tables: menu, submenu, dish
- The menu consists of submenus, there are dishes in the submenu
- Dish has only one submenu, submenu has only one menu
- Deleting a menu deletes its submenus and dishes.
- Deleting a submenu also deletes its dishes
- Count the number of submenus and dishes in the menu table
- Count the number of dishes in the submenu table

## Installation
- download files 

*Create venv:*
- python3 -m venv venv
> sudo apt install python3-venv *if 'venv' is not installed*
- source venv/bin/activate

*Install requirements:*
- pip install -r requirements.txt
> or pip install "fastapi[all]" sqlalchemy

## Start

*Start server:*
- uvicorn main:app --reload

*Start testing:*
http://localhost:8000/docs

Works great, e.g., with Debian 11 and Python 3.9, Ubuntu 22.04 and Python 3.10

Check the "database.db" file by typing:

- sqlite3 database.db
> sudo apt install sqlite3 *if 'SQLite' is not installed*


