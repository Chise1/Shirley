# Shirley使用说明
### 概述
一个基于fastapi的裸后端，主要是为了减少web相关的一些基础crud。orm基于tortoise-orm。
目标：
- User、Group、Permission创建 √
- 权限管理 √
- 配置setting模块
- model自定义权限 
- 分页依赖
- 根据model的简单crud自动生成
- 邮件和用户密码找回功能
- 创建超级用户、创建数据库等的自动执行指令


### 安装
```shell script
pip install Shirley
```
### 引入
```python
from fastapi import FastAPI
from Chau import register #引入注册

app = FastAPI(debug=True, title="这是一个框架测试包")
...

register(app=app, modules=["models", 'model_test.models'])
```
权限列表会自动将所有注册的model创建相关的crud权限。

### 使用Shirley

#### 使用User
```python

from Shirley.schemas import OAuth2PasswordRequestForm
from fastapi import Depends
from Shirley.models import User
@app.post("/user")
async def create_user(user: OAuth2PasswordRequestForm = Depends()):
    print(user)
    res = await User.create(username=user.username, password=user.password, )
    return res
```
#### 权限判断
```python
from fastapi import Depends
from Shirley.depends import check_permission
from Shirley.models import User

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(check_permission("can read Item"))):
    return [{"item_id": "Foo", "owner": current_user.username}]
```
当然你也可以这样自己手写用户是否有相关权限：
```python
from fastapi import Depends
from Shirley.err import PermissionError
from Shirley.depends import get_current_user
from Shirley.models import User
async def super_user(user: User = Depends(get_current_user)) -> User:
    """
    超级管理员权限依赖
    :param user:
    :return:
    """
    if not user.is_superuser:
        raise PermissionError()
    else:
        return user
```
#### 配置

系统启动需要进行一些配置，这些配置都在.env环境变量里面获取，所以每个项目的根目录必须有一个文件.env，在里面配置相关的环境变量内容，例如：
大多数环境变量都有默认值，但是这个SECRET_KEY不能默认，在之后考虑脚本生成的时候会自动生成默认值。
```python
SECRET_KEY='fjwyy#qht#nvoy%h4&m6hvbs-9s&##sh4710*f(ir(019!r3)c'
```
目前的环境变量有：
```python
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
```