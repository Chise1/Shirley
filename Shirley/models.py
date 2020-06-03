# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/5/30 9:13
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from tortoise.contrib.pydantic import pydantic_model_creator
from .abcModel import abcModel
from tortoise import fields, BaseDBAsyncClient
from .settings import SECRET_KEY, ALGORITHM
import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Permission(abcModel):
    code = fields.CharField(max_length=16, unique=True, description="权限码")
    description = fields.CharField(max_length=32, description="权限注释")
    model = fields.CharField(max_length=64, description="对应model", null=True)
    created_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    users: fields.ManyToManyRelation['User']
    groups: fields.ManyToManyRelation['Group']


class User(abcModel):
    username = fields.CharField(max_length=32, description="用户名")
    password = fields.CharField(max_length=32, description="密码")  # 用户密码拼接key之后MD5多重加密
    email = fields.CharField(max_length=32, description="邮箱", null=True)
    is_staff = fields.BooleanField(default=False, description="是否为职员")
    is_superuser = fields.BooleanField(default=False, description="是否为超级用户")
    is_del = fields.BooleanField(default=False, description="是否被删除")
    created_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    permissions: fields.ManyToManyRelation[Permission] = fields.ManyToManyField("models.Permission",
                                                                                related_name="users")
    groups: fields.ManyToManyRelation['Group']



    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        将密码进行加密
        :param password:
        :return:
        """
        return pwd_context.hash(password)

    def verify_password(self, password, hashed_password) -> bool:
        """
        检测密码是否正确
        :param password:原始密码
        :param hashed_password: hash加密的密码
        :return:
        """
        return pwd_context.verify(password, hashed_password)

    def check_password(self, password) -> bool:
        """
        检查该密码是否为用户的密码
        :param password:
        :return:
        """
        return pwd_context.verify(password, self.password)

    def create_access_token(self, data: Optional[Dict[str, str]] = None, expires_delta: timedelta = None) -> str:
        """
        根据data生成jwt
        :param data:
        :param expires_delta:
        :return:
        """
        if data:
            to_encode = data.copy()
        else:
            to_encode = {}
        to_encode.update({"sub": self.username})
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def save(
            self,
            using_db: Optional[BaseDBAsyncClient] = None,
            update_fields: Optional[List[str]] = None,
    ) -> None:
        """
        将密码字段加密保存
        """
        if len(self.password) != 32:  # 这里需要优化，以后考虑其他的方式进行保存

            self.password = self.hash_password(self.password)
        return await super().save(using_db, update_fields)

    @classmethod
    async def create_user(cls, username: str, password: str, email: Optional[EmailStr] = None) -> "User":
        return await cls(username=username, password=cls.hash_password(password), email=email)


class Group(abcModel):
    name = fields.CharField(max_length=32, description="组名")
    description = fields.CharField(max_length=255, description="组描述")
    users: fields.ManyToManyRelation['User'] = fields.ManyToManyField('models.User',
                                                                                     related_name="groups")
    permissions: fields.ManyToManyRelation[Permission] = fields.ManyToManyField('models.Permission',
                                                                                related_name="groups")
    created_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
