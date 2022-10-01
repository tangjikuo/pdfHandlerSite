import uvicorn
from fastapi import FastAPI, Request
import aioredis
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from router.user import userRouter

app = FastAPI()


def register_redis(app: FastAPI):
    @app.on_event('startup')
    async def startup_event():
        app.state.redis = await aioredis.from_url('redis://192.168.10.166', db=0)

    @app.on_event('shutdown')
    async def shutdown_event():
        app.state.redis.close()
        await app.state.redis.wait_closed()


register_redis(app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content=jsonable_encoder({"message": exc.errors(), "code": 421})
    )


app.include_router(userRouter, prefix='/user', tags=['users'])

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8999)
