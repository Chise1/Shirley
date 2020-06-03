# -*- encoding: utf-8 -*-
"""
@File    : forms.py
@Time    : 2020/6/1 9:22
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :根据model生成crud的路由
"""
from typing import Optional, Callable
from abc import abstractmethod, ABCMeta
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Type

from Shirley.abcModel import abcModel
from Shirley.depends import get_any_user
from Shirley.models import User


class View():
    def __init__(self, app: APIRouter):
        """
        注册app
        :param app:
        """
        self.app = app


class BaseForm(metaclass=ABCMeta):
    app: Optional[APIRouter] = None
    schema: Optional[Type[BaseModel]] = None
    model: Optional[Type[abcModel]] = None

    @abstractmethod
    def create(self) -> Callable:
        pass

    @abstractmethod
    def get_schema(self):
        return self.schema


class Form(BaseForm):
    schema: Optional[BaseModel] = None
    def __new__(cls, *args, **kwargs):
        cls = super().__new__(*args, **kwargs)
        if not cls.schema:
            cls.schema = cls.model.get_schema()
        return cls

    def __init__(self, app: APIRouter):
        self.app = app
        super().__init__()

    def get_schema(self):
        """
        自定义返回的schema
        :return:
        """
        return self.schema

    def register(self):
        name = self.__class__.__name__
        self.app.post('/' + name, response_model=self.schema)(self.create())


class CreateModelMixin(BaseForm):
    """
    创建数据
    """

    def create(self, ) -> Callable:
        """
        创建数据
        :return:
        """
        schema = self.get_schema()

        async def create_model(schema: schema, user: Optional[User] = Depends(get_any_user)):
            return schema

        return create_model
