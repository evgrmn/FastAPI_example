# FastAPI_example

![](https://badgen.net/badge/Python/3.10/blue) ![](https://badgen.net/badge/FastAPI/0.89.1/gray) ![](https://badgen.net/badge/SQLAlchemy/2.0.0/red) ![](https://badgen.net/badge/Pytest/7.2.1/blue) ![](https://badgen.net/badge/Redis/latest/green) ![](https://badgen.net/badge/Postgresql/15.1/blue?icon=postgresql) ![](https://badgen.net/badge/Pydantic/1.10.4/gray) ![](https://badgen.net/badge/RabbitMQ/3.10.7/orange)

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

- Uses Docker containerization.
- Redis caching
- ORM SQLAlchemy
- Pydantic data validation
- Pytest testing

## Creating containers and running the application:

- docker-compose up --build

Once launched, the API is available at http://localhost:8000/docs

## Run Pytest

Creating containers for testing and running Pytest:

- docker-compose -f docker-compose.tests.yml up --build

Restarting the test script:

- docker start -ai test_ylab

## Celery

Для работы с Excel-файлом ресторанного меню реализованы три эндпоинта:

1. /api/v1/task - заполняет базу данных тестовыми данными и отправляет задачу в очередь
2. /api/v1/result - проверяет готовность задачи. Excel-файл записывается в контейнер 'ylab', папка 'app'
3. /api/v1/task/download-file - скачивает готовый файл
