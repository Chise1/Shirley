# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/5/30 20:21
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import APIRouter, Depends, HTTPException, status
from .models import User, Permission
from .schemas import Token, OAuth2PasswordRequestForm
from .tools import authenticate_user
from .depends import get_current_user, check_permission

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    登录接口
    :param form_data:
    :return:
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = user.create_access_token()
    return Token(**{"access_token": access_token, "token_type": "bearer"})


@router.get('/api/user', tags=['admin'])
async def user_list(user: User = Depends(check_permission("can read User"))):
    return {"code": 200}


@router.post('/api/user/permission', tags=['admin'])
async def create_permission(permission_code: str, user: User = Depends(get_current_user)):
    permission = await Permission.get(code=permission_code)
    await user.permissions.add(permission)
    return {"code": 200}
