# -*- encoding: utf-8 -*-
"""
@File    : settings.py
@Time    : 2020/5/30 16:16
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :配置文件
"""
# SECURITY WARNING: keep the secret key used in production secret!
import os

SECRET_KEY = os.getenv('SECRET_KEY') or 'fjwyy#qht#nvoy%h4&m6hvbs-9s&##sh4710*f(ir(019!r3)c'
ALGORITHM = "HS256"  # 加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # jwt有效期

if os.getenv('DEBUG'):
    DEBUG=eval(os.getenv('DEBUG'))
else:
    DEBUG = True