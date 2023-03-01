# FastAPI_example

![](https://badgen.net/badge/Python/3.10/blue) ![](https://badgen.net/badge/FastAPI/0.89.1/gray) ![](https://badgen.net/badge/SQLAlchemy/2.0.0/red) ![](https://badgen.net/badge/Pytest/7.2.1/blue) ![](https://badgen.net/badge/Redis/4.4.2/green)

## Ресторанное меню

Описание:

- Три таблицы: меню, подменю, блюдо
- У меню есть подменю, у подменю есть блюда
- У каждого блюда может быть только одно подменю, у каждого подменю может быть только одно меню
- Меню удаляется вместе со всеми подменю и блюдами
- Подменю удаляется вместе со всеми блюдами
- В таблице "меню" считается количество подменю и блюд
- В таблице "подменю" считается количество блюд

Особенности:

- Используется контейнеризация Docker
- Кеширование Redis
- ORM SQLAlchemy
- Валидация данных Pydantic
- Тестирование Pytest

## Установка

- Скачать файлы
- Желательно создать виртуальное окружение venv
- Скачать образы из Docker Hub:

    docker pull python:3.10-slim

    docker pull postgres:15.1-alpine

    docker pull redis:latest

    docker pull rabbitmq:3.10.7-management

## Запуск приложения

Создание контейнеров и запуск приложения:

- docker-compose up

После запуска API доступно по адресу http://localhost:8000/docs

## Запуск Pytest

Создание контейнеров для тестирования и запуск Pytest:

- docker-compose -f docker-compose.tests.yml up --build

Перезапуск тестового сценария:

- docker start -ai test_ylab

## Celery

Для работы с Excel-файлом ресторанного меню реализованы три эндпоинта:

1. /api/v1/task - заполняет базу данных тестовыми данными и отправляет задачу в очередь
2. /api/v1/result - проверяет готовность задачи. Excel-файл записывается в контейнер 'ylab', папка 'app'
3. /api/v1/task/download-file - скачивает готовый файл
