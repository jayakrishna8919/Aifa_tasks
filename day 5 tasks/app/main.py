# app/main.py
from fastapi import FastAPI
from api import endpoints

app = FastAPI(title="Advanced FastAPI Project")
app.include_router(endpoints.router)
