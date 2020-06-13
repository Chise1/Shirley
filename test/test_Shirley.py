# -*- encoding: utf-8 -*-
"""
@File    : test_Shirley.py
@Time    : 2020/6/4 8:18
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :测试Shirley
"""

# 这是一个测试Shirley的工具
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
db_url = "sqlite://db.sqlite3"
from Chau import register
from Shirley.models import User
from Shirley.depends import get_current_user, get_any_user

app = FastAPI(debug=True, title="这是一个框架测试包")


@app.get("/users/me/", )
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id}


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


from Shirley.schemas import OAuth2PasswordRequestForm


@app.post("/user")
async def create_user(user: OAuth2PasswordRequestForm = Depends()):
    print(user)
    res = await User.create(username=user.username, password=user.password, )
    return res


from Chau.forms import Form, CreateModelMixin


class TestForm(Form, CreateModelMixin):
    model = User
    pass


from typing import Optional


@app.get('/test')
async def test():
    user_schema = User.get_schema()
    return {"code": 200}


@app.post('/test/permission1')  # 测试不强制需要登录
async def test_permission(user: Optional[User] = Depends(get_any_user)):
    print(user)
    return {"code": 200}


def test_Shirley():
    # schema=User.get_schema()
    # x = TestForm(app)
    # x.register()
    with TestClient(app) as client:
        register(app=app,  modules=["models", 'model_test.models'])
