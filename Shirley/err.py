# -*- encoding: utf-8 -*-
"""
@File    : err.py
@Time    : 2020/6/1 8:37
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :一些报错方法
"""
from fastapi import HTTPException, status


class PermissionError(HTTPException):
    """
    权限报错
    """

    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="你没有相关权限",
                         headers={"WWW-Authenticate": "Bearer"})
