# app/core/exceptions.py
from fastapi import HTTPException

class BaseAppException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)

class ExternalAPIException(BaseAppException):
    def __init__(self, detail: str = "Error fetching data from external API"):
        super().__init__(detail=detail, status_code=502)
