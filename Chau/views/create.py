# -*- encoding: utf-8 -*-
"""
@File    : create.py
@Time    : 2020/6/13 11:50
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Optional, List, Dict, Callable, Type, Tuple
from pydantic import BaseModel
from fastapi import Depends
from tortoise.contrib.pydantic import pydantic_model_creator
from Shirley.depends import check_permissions, get_current_user, get_permissions_user
from Shirley.models import User, Permission, Group
from tortoise.models import Model


def model_post_func(model: Type[Model], schema_name=None, schema: Optional[Type[BaseModel]] = None,
                    permission_codes: Tuple[str] = (),
                    exclude: Tuple[str, ...] = (),
                    include: Tuple[str, ...] = (), computed: Tuple[str, ...] = (), allow_cycles: Optional[bool] = None,
                    sort_alphabetically: Optional[bool] = None,
                    _stack: tuple = (),
                    exclude_readonly: bool = False, ) -> Callable:
    """
    根据model生成post创建接口
    :param model:
    :param schema_name:
    :param permission_codes:权限组,为None则不需要User，默认需要User，为Tuple[str]则需要权限
    :param exclude:
    :param include:
    :param computed:
    :param allow_cycles:
    :param sort_alphabetically:
    :param _stack:
    :param exclude_readonly:
    :return:
    """
    if not schema:
        schema: Type[BaseModel] = pydantic_model_creator(model, name=schema_name, exclude=exclude, include=include,
                                                         computed=computed, allow_cycles=allow_cycles,
                                                         sort_alphabetically=sort_alphabetically, _stack=_stack,
                                                         exclude_readonly=exclude_readonly)

    async def model_post(post_dict: schema, user: User = Depends(get_permissions_user(permission_codes)), ):
        user_obj = await model.create(**post_dict.dict(exclude_unset=True))
        return user_obj

    return model_post
