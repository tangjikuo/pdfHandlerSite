from datetime import date
import re
import traceback
from typing import Optional

from fastapi import APIRouter, Depends, status, Body, Form, Request, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from commons.common_func import get_db, get_config
from dao.crud import *
from commons.logs import MyLog
from commons.jsontools import response, resp_400

log = MyLog('user-info.log').get_loger()
secret_key = get_config('secret.SECRET_KEY')
algorithm = get_config('secret.ALGORITHM')
expire_time = get_config('secret.ACCESS_TOKEN_EXPIRE_MINUTES')

userRouter = APIRouter()

pwd_content = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_passwd(plain_passwd, hashed_passwd):
    """校验密码"""
    return pwd_content.verify(plain_passwd, hashed_passwd)


def get_passwd_hash(passwd):
    """
    获取密码哈希值
    :param passwd:
    :return:
    """
    return pwd_content.hash(passwd)


@userRouter.post('/create', tags=['users'])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    log.info("创建用户")
    if len(user.username) < 8 or len(user.username) > 16:
        return response(code=100106, message="用户名长度应该是8-16位", data="")
    db_crest = get_user_by_name(db, user.username)
    if db_crest:
        return response(code=100104, message="用户名重复", data="")
    try:
        password = get_passwd_hash(user.password)
        user.password = password
    except Exception as e:
        log.exception(e)
        return response(code=100105, data="", message="密码加密失败")
    try:
        user = db_create_user(db=db, user=user)
        log.info("创建用户成功")
        return response(code=200, data={'user': user.username}, message="success")
    except Exception as e:
        log.exception(e)
        return response(code=100101, data="", message="注册失败")


def create_access_token(data: dict):
    """
    jwt加密
    :param data:
    :return:
    """
    to_encode = data.copy()
    encode_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encode_jwt


async def get_curr_user(request: Request, token: Optional[str] = Header(...), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="验证失败"
    )
    credentials_for_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="用户未登录或者登陆token已经失效"
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user_is = await request.app.state.redis.get(username)
        if not user_is and user_is != token:
            raise credentials_for_exception
        user = get_user_by_name(db, username)
        return user
    except JWTError:
        log.error(traceback.format_exc())
        raise credentials_exception


@userRouter.post('/login')
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_name(db, user.username)
    if not db_user:
        log.info("login:" + user.username + "不存在")
        return response(code=100205, message='用户不存在', data='')
    varify_passwd = verify_passwd(user.password, db_user.password)
    if varify_passwd:
        user_is = await request.app.state.redis.get(user.username)
        if not user_is:
            try:
                token = create_access_token(data={'sub': user.username})
            except Exception as e:
                log.exception(e)
                return response(code=100203, message='产生token失败', data='')
            request.app.state.redis.set(user.username, token, expire=expire_time * 10)
            return response(code=200, message='成功', data={'token': token})
        return response(code=200, message='成功', data={'token': user_is})
    else:
        result = await request.app.state.redis.hgetall(user.username + "_password", encodeing='utf8')
        if not result:
            times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            request.app.state.redis.hmset_dict(user.username + '_password', num=0, time=times)
            return response(code=100206, message="密码错误", data='')
        else:
            errornum = int(result['num'])
            numtime = (datetime.now() - datetime.strptime(result['time'], "%Y-%m-%d %H:%M:%S")).seconds / 60
            if errornum < 10 and numtime < 30:
                # 输入错误10次可以重试 错误次数加一
                errornum += 1
                request.app.state.redis.hmset_dict(user.username + '_password', num=errornum)
                return response(code=100206, message='密码错误')
            elif errornum < 10 and numtime > 30:
                errornum = 1
                times = datetime.strftime(datetime.now(), '"%Y-%m-%d %H:%M:%S')
                request.app.state.redis.hmset_dict(user.username + '_password', num=errornum, time=times)
                return response(code=100206, message='密码错误')
            elif errornum > 10 and numtime < 30:
                # 次数超过10次就锁账号
                errornum += 1
                request.app.state.redis.hmset_dict(user.username + '_password', num=errornum)
                return response(code=100204, message='输入密码次数过多，账号暂时锁定，请30分钟后在重试', data='')
            else:
                errornum = 1
                times = datetime.strftime(datetime.now(), '"%Y-%m-%d %H:%M:%S')
                request.app.state.redis.hmset_dict(user.username + '_password', num=errornum, time=times)
                return response(code=200, message='密码错误', data='')


@userRouter.get('/getcuruser', response_model=UserBase)
async def getcuruser(user=Depends(get_curr_user)):
    return response(code=200, message='success', data=user)

# @userRouter.get('/{user_id}')
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = get_user_by_id(db, user_id)
#     print(db_user)
#     if db_user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='user not exist'
#         )
#     return db_user

# @userRouter.post('/create')
# def create_users(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = get_user_by_name(db, user.username)
#     if db_user is None:
#         db_create = create_user(db, user)
#         return db_create
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='user has already exist, please input other name'
#         )
