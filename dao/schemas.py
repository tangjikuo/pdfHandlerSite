from pydantic import BaseModel
from typing import Union


class UserBase(BaseModel):
    """用户基础信息"""
    username: str


class UserCreate(UserBase):
    """创建用户信息"""
    password: str
    money: float


class UserLogin(BaseModel):
    username: str
    password: str


class FileQuery(BaseModel):
    """查询文件信息"""
    file_name: Union[str, None] = None
    invoice_code: Union[str, None] = None
    invoice_number: Union[str, None] = None
    invoice_date: Union[str, None] = None
    check_code: Union[str, None] = None


class Token(BaseModel):
    """token鉴权"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
