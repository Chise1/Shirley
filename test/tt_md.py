# -*- encoding: utf-8 -*-
"""
@File    : tt_md.py
@Time    : 2020/6/13 13:28
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import markdown
from typing import Callable

markdownText = """# 创建超级用户
代码
```py
print(user)
res = await User.create(username=user.username, password=user.password, is_superuser=True)
return res
```
"""


def tomd(func: Callable):
    func.__doc__ = markdown.markdown(func.__doc__, output_format='html5', extensions=['extra'])
    return func

# print(markdown.markdown(markdownText, output_format='html5', extensions=['extra']))
