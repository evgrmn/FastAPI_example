# FastAPI_example

![](https://img.shields.io/badge/python-3.10-blue?style=flat-square) ![](https://img.shields.io/badge/fastapi-0.89.1-critical?style=flat-square) ![](https://img.shields.io/badge/SQLAlchemy-2.0.0-orange?style=flat-square)

![](https://badgen.net/badge/:subject/:status/:blue?icon=github)

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
