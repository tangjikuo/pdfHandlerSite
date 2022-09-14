from fastapi import APIRouter, Depends, status, Body, Form
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from commons.common_func import get_db
from dao.crud import *

userRouter = APIRouter()


@userRouter.get('/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    print(db_user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not exist'
        )
    return db_user


@userRouter.post('/create')
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_name(db, user.username)
    if db_user is None:
        db_create = create_user(db, user)
        return db_create
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='user has already exist, please input other name'
        )
