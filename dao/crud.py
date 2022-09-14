from sqlalchemy.orm import Session
from models import *
from schemas import *
from sqlalchemy import or_, and_


def get_user_by_id(db: Session, user_id: int):
    """通过id查询用户"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    """通过用户名查询用户"""
    return db.query(User).filter(User.username == name).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
