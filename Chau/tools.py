# -*- encoding: utf-8 -*-
"""
@File    : tools.py
@Time    : 2020/5/30 10:14
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import asyncio
from tortoise import Tortoise
from Shirley.models import Permission
from tortoise.exceptions import DoesNotExist

__all__ = ['init']


async def __init(db_url, models):
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url=db_url,
        modules=models
    )
    await Tortoise.generate_schemas()
    x = Tortoise.apps.get('models')
    for model in x:
        try:
            await Permission.get(code="can read " + model)
        except DoesNotExist:
            await Permission.create(code="can read " + model, description="can read " + model, model=model)
        try:
            await Permission.get(code="can create " + model)
        except DoesNotExist:
            await Permission.create(code="can create " + model, description="can create " + model, model=model)
        try:
            await Permission.get(code="can update " + model)
        except DoesNotExist:
            await Permission.create(code="can update " + model, description="can update " + model, model=model)
        try:
            await Permission.get(code="can delete " + model)
        except DoesNotExist:
            await Permission.create(code="can delete " + model, description="can delete " + model, model=model)

    await Tortoise.close_connections()  # 关闭连接
    print("OK")


def init(db_url, models):
    """
    初始化权限
    :param db_url:
    :param models:
    :return:
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__init(db_url, models))


if __name__ == '__main__':
    init(db_url="sqlite://db.sqlite3", models={"models": ['Shirley.models']})
