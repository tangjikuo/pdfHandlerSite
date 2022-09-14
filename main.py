import uvicorn
from fastapi import FastAPI
import aioredis

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


app.include_router(userRouter, prefix='/user')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8999)
