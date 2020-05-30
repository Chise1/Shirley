# -*- encoding: utf-8 -*-
"""
@File    : tools.py
@Time    : 2020/5/30 20:25
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Optional
from .models import User
async def get_user(username) -> Optional[User]:
    return await User.filter(username=username, is_del=False).first()

async def authenticate_user(username: str, password: str):
    """
    获取登录的用户
    :param fake_db:
    :param username:
    :param password:
    :return:
    """
    user = await get_user(username)
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user
