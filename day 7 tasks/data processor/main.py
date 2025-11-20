from fastapi import FastAPI
import uvicorn
from api import router

app = FastAPI(
    title="Data Processing Pipeline API",
)



app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Data Processing Pipeline API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)