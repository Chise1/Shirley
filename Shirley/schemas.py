# -*- encoding: utf-8 -*-
"""
@File    : schemas.py
@Time    : 2020/5/30 20:23
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import Form
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class OAuth2PasswordRequestForm:
    """
    获取用户username和密码的form表单
    """

    def __init__(
            self,
            grant_type: str = Form(None, regex="password"),
            username: str = Form(...),
            password: str = Form(...),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password