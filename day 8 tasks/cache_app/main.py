from fastapi import FastAPI,Request
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
        
        
@app.middleware("http")
async def add_version_and_deprecation_header(request: Request, call_next):
    response = await call_next(request)

    path = request.url.path
    if path.startswith("/users/v2"):
        response.headers["X-API-Version"] = "v2"
    elif path.startswith("/users/v1"):
        response.headers["X-API-Version"] = "v1"

    return response
        








