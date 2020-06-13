# -*- encoding: utf-8 -*-
"""
@File    : setup.py.py
@Time    : 2020/5/30 9:12
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from setuptools import setup, find_packages

setup(
    name="Shirley",
    version="0.3.0",
    description="基于fastapi的web框架",
    author="Chise",
    author_email="chise123@live.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    python_requires=">=3.7",  # Python版本依赖
    install_requires=[
        'fastapi',
        'tortoise-orm',
        'uvicorn',
        'pyjwt',
        'passlib[bcrypt]',
        'python-multipart',
        'bcrypt',
        'python-dotenv'
    ],  # 第三方库依赖
    url="https://shirley.readthedocs.io/en/latest/"
)