# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/6/1 13:56
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from Shirley.abcModel import abcModel

class Node(abcModel):

    # father = fields.ForeignKeyField("Node", null=True)
    name = fields.CharField(max_length=32)
    def __str__(self):
        return self.name
User_Pydantic = pydantic_model_creator(Node, name="Node")
print(User_Pydantic)
# UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)