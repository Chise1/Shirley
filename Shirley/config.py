# -*- encoding: utf-8 -*-
"""
@File    : settings.py
@Time    : 2020/5/30 16:16
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :配置文件
"""

from pydantic import BaseSettings


class __Settings(BaseSettings):
    DB_URL: str="sqlite://db.sqlite3"
    LOGIN_URL = "/admin"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"  # 加密算法
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # jwt有效期
    DEBUG: bool = True

    class Config:
        env_file = '.env'


settings = __Settings()
