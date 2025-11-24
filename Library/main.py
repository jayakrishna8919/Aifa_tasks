from fastapi import FastAPI
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database.config import Base,engine
from routers.routes import router
from dotenv import load_dotenv
load_dotenv()
from utils.logging_config import logger


app = FastAPI(title="Library Management System")
logger.info("The fastapi app started")

app.include_router(router)

@app.on_event("startup")
async def startup():
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

