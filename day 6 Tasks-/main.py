from fastapi import FastAPI
from api.endpoints import auth, protected

app = FastAPI(title="Secure FastAPI App")

app.include_router(auth.router)
app.include_router(protected.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Secure FastAPI App!"}