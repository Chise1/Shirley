# -*- encoding: utf-8 -*-
"""
@File    : err.py
@Time    : 2020/6/1 8:37
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :一些报错方法
"""
from typing import Dict, Optional
from fastapi import HTTPException, status


class PermissionError(HTTPException):
    """
    权限报错
    """

    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="你没有相关权限",
                         headers={"WWW-Authenticate": "Bearer"})


class ForcedRet(HTTPException):
    """
    通过raise的方式强制返回相关结果
    """

    def __init__(self, status_code: int, res: dict, headers: Optional[Dict[str, str]]):
        self.res = res
        if not headers:
            headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code=status_code, detail="",
                         headers=headers)

    def __repr__(self) -> str:
        return str(self.res)
