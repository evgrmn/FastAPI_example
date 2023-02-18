import asyncio

from celery import Celery

import models as _models


celery_app = Celery(
    "worker",
    broker_url="amqp://guest:guest@rabbit:5672//",
    result_backend="rpc://",
)
celery_app.conf.task_routes = {"celery_worker.task_celery": "test-queue"}
celery_app.conf.update(task_track_started=True)



@celery_app.task(name="celery_worker.task_celery")
def task_celery(file_name):
    for el in _models.delete_model_dict:
        asyncio.run(_models.delete_table_data(el[1], el[0]))
    menu_data = [
        {"model": "menu", "data": {"title": "Меню", "description": "Основное меню"}},
        {
            "model": "submenu",
            "data": {
                "title": "Холодные закуски",
                "description": "К пиву",
                "menu_id": 1,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Сельдь Бисмарк",
                "description": "Традиционное немецкое блюдо из маринованной\
                     сельди",
                "submenu_id": 1,
                "price": 182.99,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Мясная тарелка",
                "description": "Нарезка из ветчины, колбасных колечек,\
                     нескольких сортов сыра, фруктов и фокаччи",
                "submenu_id": 1,
                "price": 215.36,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Рыбная тарелка",
                "description": "Нарезка из креветок, кальмаров, раковых шеек,\
                     гребешков, лосося, скумбрии и красной икры",
                "submenu_id": 1,
                "price": 265.57,
            },
        },
        {
            "model": "submenu",
            "data": {"title": "Рамен", "description": "Горячий рамен", "menu_id": 1},
        },
        {
            "model": "dish",
            "data": {
                "title": "Дайзу рамен",
                "description": "Рамен на курином бульоне с куриными подушками\
                     и яйцом аджитама, яично-пшеничной лапшой, ростки зелени,\
                         грибами муэр и зеленым луком",
                "submenu_id": 2,
                "price": 166.47,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Унаги рамен",
                "description": "Рамен на нежном сливочном рыбном бульоне, с\
                     добавлением маринованного угря, грибов муэр, кунжута,\
                         зеленого лука",
                "submenu_id": 2,
                "price": 168.25,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Чиизу Рамен",
                "description": "Рамен на насыщенном сырном бульоне на основе\
                     кокосового молока, с добавлением куриной грудинки, яично\
                         - пшеничной лапши, мисо-матадоре, ростков зелени,\
                             листьев вакамэ",
                "submenu_id": 2,
                "price": 132.88,
            },
        },
        {
            "model": "menu",
            "data": {
                "title": "Алкогольное меню",
                "description": "Алкогольные\
                 напитки",
            },
        },
        {
            "model": "submenu",
            "data": {
                "title": "Красные вина",
                "description": "Для романтичного вечера",
                "menu_id": 2,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Шемен де Пап ля Ноблесс",
                "description": "Вино красное — фруктовое, среднетелое,\
                     выдержанное в дубе",
                "submenu_id": 3,
                "price": 2700.79,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Рипароссо Монтепульчано",
                "description": "Вино красное, сухое",
                "submenu_id": 3,
                "price": 3100.33,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Кьянти, Серристори",
                "description": "Вино красное — элегантное, комплексное, не\
                     выдержанное в дубе",
                "submenu_id": 3,
                "price": 1850.42,
            },
        },
        {
            "model": "submenu",
            "data": {
                "title": "Виски",
                "description": "Для интересных бесед",
                "menu_id": 2,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Джемисон",
                "description": "Классический купажированный виски, проходящий\
                     4-хлетнюю выдержку в дубовых бочках",
                "submenu_id": 4,
                "price": 420.78,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Джек Дэниелс",
                "description": "Характерен мягкий вкус, сочетает в себе\
                     карамельно-ванильные и древесные нотки. Легкий привкус\
                         дыма.",
                "submenu_id": 4,
                "price": 440.11,
            },
        },
        {
            "model": "dish",
            "data": {
                "title": "Чивас Ригал",
                "description": "Это купаж высококачественных солодовых и\
                     зерновых виски, выдержанных как минимум в течение 12\
                         лет, что придает напитку роскошные нотки меда,\
                             ванили и спелых яблок.",
                "submenu_id": 4,
                "price": 520.08,
            },
        },
    ]
    for el in menu_data:
        par = _models.model_dict[el["model"]](**el["data"])
        asyncio.run(_models.add_instance(par))
    # for el in _models.delete_model_dict:
    #    asyncio.run(_models.delete_table_data(el[1], el[0]))

    return file_name