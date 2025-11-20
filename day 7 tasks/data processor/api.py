from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import pandas as pd
import os
import tempfile
from core.processor import DataProcessor
from core.utils import get_file_size_mb
from models import ProcessingRequest

router = APIRouter()

# In-memory storage for processed results (in production, use Redis or database)
processed_results = {}

@router.post("/process-file")
async def process_file(
    file: UploadFile = File(...),
    sheet_name: str = None,
    background_tasks: BackgroundTasks = None
):
    
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        
        file_size_mb = get_file_size_mb(tmp_file_path)
        if file_size_mb > 100:  
            pass
        
        # Read file
        df = DataProcessor.read_file(tmp_file_path, sheet_name)
        
        # Store for later processing
        file_id = file.filename + str(hash(content))
        processed_results[file_id] = {"raw_data": df, "file_path": tmp_file_path}
        
        return {"file_id": file_id, "rows": len(df), "columns": list(df.columns)}
    
    except Exception as e:
        os.unlink(tmp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/execute-pipeline/{file_id}")
async def execute_pipeline(file_id: str, request: ProcessingRequest):
    """Execute full processing pipeline on uploaded file"""
    if file_id not in processed_results:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        df = processed_results[file_id]["raw_data"]
        
        # Execute pipeline
        result = DataProcessor.process_pipeline(
            df,
            cleaning_config=request.cleaning_config.dict(),
            aggregation_config=request.aggregation_config.dict() if request.aggregation_config else None,
            visualization_config=[viz.dict() for viz in request.visualization_config] if request.visualization_config else None
        )
        
        # Store processed result
        processed_results[file_id]["processed"] = result
        
        # Prepare response (exclude large DataFrames)
        response = {
            "report": result["report"],
            "visualizations": result["visualizations"]
        }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

@router.get("/export/{file_id}/{data_type}")
async def export_data(file_id: str, data_type: str, format: str = "json"):
    """Export processed data in specified format"""
    if file_id not in processed_results:
        raise HTTPException(status_code=404, detail="File not found")
    
    if "processed" not in processed_results[file_id]:
        raise HTTPException(status_code=400, detail="Execute pipeline first")
    
    result = processed_results[file_id]["processed"]
    
    # Select data to export
    if data_type == "cleaned":
        df = result["cleaned_data"]
    elif data_type == "aggregated" and result["aggregated_data"] is not None:
        df = result["aggregated_data"]
    else:
        raise HTTPException(status_code=400, detail="Invalid data type or not available")
    
    # Create export file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmp_file:
        export_path = tmp_file.name
    
    try:
        DataProcessor.export_data(df, export_path, format)
        return FileResponse(
            export_path,
            filename=f"export_{data_type}.{format}",
            media_type={
                "csv": "text/csv",
                "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "json": "application/json"
            }.get(format, "application/octet-stream")
        )
    except Exception as e:
        if os.path.exists(export_path):
            os.unlink(export_path)
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")