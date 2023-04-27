# FastAPI_example

![](https://badgen.net/badge/Python/3.10/blue) ![](https://badgen.net/badge/FastAPI/0.89.1/gray) ![](https://badgen.net/badge/SQLAlchemy/2.0.8/red) ![](https://badgen.net/badge/Pytest/7.2.1/blue) ![](https://badgen.net/badge/Redis/latest/green) ![](https://badgen.net/badge/Postgresql/15.1/blue?icon=postgresql) ![](https://badgen.net/badge/Pydantic/1.10.4/gray) ![](https://badgen.net/badge/RabbitMQ/3.10.7/orange) ![](https://badgen.net/badge/PyJWT/2.6.0/blue)

## Restaurant menu

Description:

- Three tables: menu, submenu, dish
- The menu has a submenu, the submenu has dishes
- Each dish can only have one submenu, each submenu can only have one menu
- The menu is deleted along with all submenus and dishes
- The submenu is deleted along with all dishes
- In the "menu" table, the number of submenus and dishes is counted
- In the "submenu" table, the number of dishes is counted

Peculiarities:

- Uses Docker containerization
- Redis caching
- ORM SQLAlchemy
- Pydantic data validation
- Pytest testing
- Celery background tasks
- Sending emails using gmail.com
- JSON Web Tokens (JWT)

## Creating containers and running the application:

- docker-compose up --build

Once launched, the API is available at http://localhost:8000/docs

RabbitMQ is available at http://localhost:15672 *Username: guest, Password: guest*

PostgreSQL can be conncted:

- *Host: localhost*
- *Port: 5433*
- *Username: postgres*
- *Password: password*
- *Database: fastapi_database*


## Run Pytest

Creating containers for testing and running Pytest:

- docker-compose -f docker-compose.tests.yml up --build

Restarting the test script while test_redis and test_postgr containers are running:

- docker start -ai test_ylab
