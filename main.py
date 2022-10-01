from sqlalchemy import true
import uvicorn
from fastapi import FastAPI, Request
import aioredis
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from router.user import userRouter

app = FastAPI()


async def get_redis_pool():
    redis = await aioredis.from_url(url='redis://:123456@10.0.0.5:6379', db=0)
    return redis


@app.on_event('startup')
async def startup_event():
    app.state.redis = await get_redis_pool()
    app.state.redis.set('token', '123456', expire=30)


@app.on_event('shutdown')
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content=jsonable_encoder({"message": exc.errors(), "code": 421})
    )


app.include_router(userRouter, prefix='/user', tags=['users'])

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8999, debug=true, reload=true)
