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
import uvicorn
from fastapi import FastAPI, Depends
db_url = "sqlite://db.sqlite3"
from Chau import register

app = FastAPI(debug=True, title="这是一个框架测试包")
register(app=app, db_url=db_url, modules=["models",'model_test.models'])

from Shirley import router

app.include_router(router, tags=['admin'])

from Shirley.models import User
from Shirley.depends import get_current_user


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


@app.get('/test')
async def test():
    user_schema = User.get_schema()
    return {"code": 200}


# schema=User.get_schema()
x=TestForm(app)
x.register()
if __name__ == '__main__':
    uvicorn.run(app, )
