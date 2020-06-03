# -*- encoding: utf-8 -*-
"""
@File    : depends.py
@Time    : 2020/5/30 17:02
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :相关的依赖
"""
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from .models import User, Permission
from .settings import SECRET_KEY, ALGORITHM
from .tools import get_user
from typing import Callable, List, Optional
from .err import PermissionError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    根据token获取用户
    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception
    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_any_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[User]:
    """
    根据token获取用户，如果没有则返回None
    :param token:
    :return:
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise None
    except PyJWTError:
        raise None
    user = await get_user(username)
    if user is None:
        raise None
    return user


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


async def staff_user(user: User = Depends(get_current_user)) -> User:
    """
    职员权限依赖
    :param user:
    :return:
    """
    if user.is_superuser or user.is_staff:
        raise PermissionError()
    else:
        return user


def check_permission(permission_code: str) -> Callable:
    """
    确认是否有权限
    :param permission_code:
    :return:
    """

    async def has_permission(user: User = Depends(get_current_user)) -> User:
        """
        返回的依赖
        :param user:
        :return:
        """
        if user.is_superuser:
            return user
        if await user.permissions.filter(code=permission_code):  # 这里需要测试一下
            return user
        raise PermissionError()

    return has_permission


async def check_permissions(permission_codes: List[str]) -> Callable:
    """
    确认是否有权限组
    :param permission_code:
    :return:
    """

    async def has_permission(user: User = Depends(get_current_user)) -> User:
        """
        返回的依赖
        :param user:
        :return:
        """
        if user.is_superuser:
            return user
        permissions = await user.permissions.all()  # 这里需要测试一下
        for permission in permissions:
            if not permission_codes.count(permission.code):
                raise PermissionError()

    return has_permission
