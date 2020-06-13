# -*- encoding: utf-8 -*-
"""
@File    : tt.py
@Time    : 2020/6/13 13:26
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""


def add(x: int, y: int) -> int:
    """
    这是一个加法
    """
    return x + y
print(add.__annotations__)
print(add.__doc__)
x=add