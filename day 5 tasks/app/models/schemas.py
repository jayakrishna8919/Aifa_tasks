from pydantic import BaseModel
from typing import List

class APIDataItem(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool

class APIDataResponse(BaseModel):
    success: bool
    data: List[APIDataItem]

