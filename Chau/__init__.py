# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/5/30 9:20
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import List, Optional, Dict
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from .tools import init
__all__ = ['register']


def register(app: FastAPI, db_url: str, modules: Optional[List[str]] = None, generate_schemas: bool = True,
             add_exception_handlers: bool = True):
    """
    注册数据库models，并在注释的时候，将权限控制写入
    :param app:
    :param db_url:
    :param models:model的路径
    :param generate_schemas:
    :param add_exception_handlers:
    :return:
    """
    # 先检查权限字段是否被添加，如果没有被添加则自动添加，然后再注册app
    if not modules:
        modules = []
    all_modules = {"models": ['Shirley.models'] + modules}
    init(db_url,all_modules)
    register_tortoise(  # 这里是启动app的，之后会考虑和使用uvicorn启动的性能差别
        app,
        db_url=db_url,  # 数据库信息
        modules=all_modules,  # models列表
        generate_schemas=generate_schemas,  # 如果数据库为空，则自动生成对应表单,生产环境不要开
        add_exception_handlers=add_exception_handlers,  # 生产环境不要开，会泄露调试信息
    )
