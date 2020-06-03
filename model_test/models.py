# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/6/1 14:14
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from Shirley.abcModel import abcModel


class Project(abcModel):
    name=fields.CharField(max_length=32)

ProjectIn = pydantic_model_creator(Project, name="ProjectIn", )
print(ProjectIn)