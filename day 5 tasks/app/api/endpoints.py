# app/api/endpoints.py
from fastapi import APIRouter
from services.external_apis import fetch_data_concurrently
from models.schemas import APIDataResponse

router = APIRouter()

@router.get("/data", response_model=APIDataResponse)
async def get_data():
   
    #here we are Fetching data from multiple external APIs concurrently
    data = await fetch_data_concurrently()
    return {"data": data,"success":True}
