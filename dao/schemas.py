from pydantic import BaseModel
from typing import Union


class UserBase(BaseModel):
    """用户基础信息"""
    username: str
    status: int


class UserCreate(UserBase):
    """创建用户信息"""
    password: str
    money: float


class FileQuery(BaseModel):
    """查询文件信息"""
    file_name: Union[str, None] = None
    invoice_code: Union[str, None] = None
    invoice_number: Union[str, None] = None
    invoice_date: Union[str, None] = None
    check_code:  Union[str, None] = None
