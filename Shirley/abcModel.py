# -*- encoding: utf-8 -*-
"""
@File    : abcModel.py
@Time    : 2020/5/30 9:29
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :数据库和相关的抽象组件
"""
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields


class abcModel(Model):
    id = fields.IntField(pk=True)

    @classmethod
    def get_schema(cls):
        schema = cls.__class__.__name__ + "Schema"
        if not hasattr(cls, schema):
            setattr(cls, schema, pydantic_model_creator(cls, name=schema))
        else:
            return getattr(cls, schema)

    class Meta:
        abstract = True


class ModelAndTime(abcModel):
    created_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True
