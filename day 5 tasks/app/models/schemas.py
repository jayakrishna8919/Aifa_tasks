# # app/models/schema.py
# from typing import List, Optional
# from pydantic import BaseModel, HttpUrl, Field

# # -----------------------------
# # Response schemas
# # -----------------------------

# class APIDataItem(BaseModel):
#     id: int
#     name: str
#     description: Optional[str] = None
#     url: Optional[HttpUrl] = None

# class DataResponse(BaseModel):
#     success: bool
#     data: List[APIDataItem] = []
#     message: Optional[str] = None

# # -----------------------------
# # Request schemas
# # -----------------------------

# class FetchDataRequest(BaseModel):
#     urls: List[HttpUrl] = Field(..., description="List of URLs to fetch concurrently")

# # -----------------------------
# # Error schema
# # -----------------------------

# class APIErrorResponse(BaseModel):
#     success: bool = False
#     error: str


# app/models/schema.py
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

