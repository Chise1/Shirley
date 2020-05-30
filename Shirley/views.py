# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/5/30 20:21
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import APIRouter,Depends,HTTPException,status
from .schemas import Token,OAuth2PasswordRequestForm
from .tools import authenticate_user
router=APIRouter()

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
    return {"access_token": access_token, "token_type": "bearer"}