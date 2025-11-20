# ---- Request model ----
from pydantic import BaseModel,EmailStr
class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str


class UploadResponse(BaseModel):
    filename: str
    uploaded_at: str
    summary_path: str
    status: str