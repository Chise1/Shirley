# -*- encoding: utf-8 -*-
"""
@File    : managers.py
@Time    : 2020/6/13 13:00
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :用于初期创建各种账户的路由
"""
from fastapi import APIRouter, Depends

from Shirley.models import User, Permission
from Shirley.schemas import OAuth2PasswordRequestForm
from tortoise.contrib.pydantic import pydantic_model_creator

manager = APIRouter()


@manager.post('/superuser', summary="创建超级用户")
async def create_superuser(user: OAuth2PasswordRequestForm = Depends()):
    """
    创建超级用户
    """
    print(user)
    res = await User.create(username=user.username, password=user.password, is_superuser=True)
    return res


@manager.delete('/superuser', summary="删除用户")
async def delete_superuser(user_id):
    user = await User.get(id=user_id)
    res = await user.delete()  # 注意，这里的删除用了两次，这是不合适的，在未来tortoise更新之后记得修改
    return {"message": res}


permission_schema = pydantic_model_creator(Permission)

@manager.post('/user/permission',summary="给用户增加权限",)
async def user_add_permission(permission_code:str):
    pass

@manager.post('/permission', summary="增加自定义权限", response_model=permission_schema)
async def add_permission(permission: permission_schema):
    """
    创建自定义的权限，在之后可以用来进行判定
    :param permission:
    :return:
    """
    res = await Permission.create(**permission.dict(exclude={'id', }))
    permission.id = res
    return permission
