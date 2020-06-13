# -*- encoding: utf-8 -*-
"""
@File    : tt.py
@Time    : 2020/6/13 11:43
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
for i in range(5):
    for j in range(4):
        if i==j:
            print("i==j:",i)
            break
        else:
            print("i:",i," j:",j)

