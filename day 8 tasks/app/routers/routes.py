from fastapi import APIRouter,BackgroundTasks,UploadFile,File,HTTPException

from models.models import EmailRequest,UploadResponse
from services.mail_sender_service import send_email_sync
from datetime import datetime

import os

from services.process_file_service import UPLOAD_DIR,PROCESSED_DIR,process_csv_file,get_extension,ALLOWED_EXTENSIONS,MAX_FILE_SIZE
import json

router = APIRouter()
@router.post("/send-email")
async def send_email(req: EmailRequest, background_tasks: BackgroundTasks):
    
    background_tasks.add_task(send_email_sync, req.to, req.subject, req.body)
    
    return {"status": "queued"}

@router.post("/upload-csv", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    
    # basic checking of csv file or not
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    ext = get_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file extension '{ext}'. Only CSV files allowed.")

    data = await file.read()
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large!")
    
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_name = f"{timestamp}_{os.path.basename(file.filename)}"
    print(safe_name)
    saved_path = os.path.join(UPLOAD_DIR, safe_name)

   
    try:
        with open(saved_path, "wb") as buffer:                                   # Save uploaded file
            content = await file.read()  
            buffer.write(content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save file: {exc}")

   
    summary_filename = f"{safe_name}.summary.json"
    summary_path = os.path.join(PROCESSED_DIR, summary_filename)
    background_tasks.add_task(process_csv_file, saved_path, summary_path)

    return UploadResponse(
        filename=safe_name,
        uploaded_at=datetime.utcnow().isoformat() + "Z",
        summary_path=summary_path,
        status="processing"
    )


@router.get("/summary/{summary_filename}")
def get_summary(summary_filename: str):
    path = os.path.join(PROCESSED_DIR, summary_filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Summary not ready")
    with open(path, encoding='utf-8') as f:
        return json.load(f)





