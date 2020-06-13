# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2020/5/30 9:46
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
# 这是一个测试Shirley的工具
from typing import Optional
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from starlette import status

from Chau import register
# from Shirley.schemas import OAuth2PasswordRequestForm
from Shirley.schemas import Token, OAuth2PasswordRequestForm
from Shirley.tools import authenticate_user

app = FastAPI(debug=True, title="这是一个框架测试包")
register(app=app,  modules=["models", 'model_test.models'])

from Shirley.models import User
from Shirley.depends import get_current_user, get_any_user


@app.get("/users/me/", )
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id}


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post('/test/permission1')  # 测试不强制需要登录
async def test_permission(user: Optional[User] = Depends(get_any_user)):
    print(user)
    return {"code": 200}


@app.get('/test')
async def test():
    user_schema = User.get_schema()
    return user_schema


from Chau import managers
#注册常用的管理方法
app.include_router(managers.manager, prefix='/manage',tags=['manager'])

if __name__ == '__main__':
    uvicorn.run(app, )
