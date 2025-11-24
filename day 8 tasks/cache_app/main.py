# app.py (shared imports & DB setup)
from fastapi import FastAPI


from utils.dependencies import cache_key_for_user,cache
from configurations.db_config import Base,engine
from routers.routes import router


app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup():
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        








