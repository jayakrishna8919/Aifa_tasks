# app.py (shared imports & DB setup)
from fastapi import FastAPI


from utils.dependencies import cache_key_for_user,cache
from configurations.db_config import Base,engine
from routers.routes import router
from routers.v1 import routerv1
from routers.v2 import routerv2


app = FastAPI()

app.include_router(router)
app.include_router(routerv1)
app.include_router(routerv2)


@app.on_event("startup")
async def startup():
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        








