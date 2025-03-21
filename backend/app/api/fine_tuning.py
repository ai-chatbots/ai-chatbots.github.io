# app/api/fine_tuning.py

from fastapi import APIRouter, HTTPException, UploadFile, File
import openai
import os
from app.config import OPENAI_API_KEY

router = APIRouter()

openai.api_key = OPENAI_API_KEY

@router.post("/fine-tune")
async def fine_tune(file: UploadFile = File(...)):
    """
    Fine-tune a model using a client-provided JSONL training file.
    The file must be in JSONL format with training examples.
    """
    filename = file.filename
    if not filename.endswith(".jsonl"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .jsonl files are accepted.")
    
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, filename)
    
    try:
        contents = await file.read()
        with open(temp_file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {str(e)}")
    
    try:
        # Use the new file upload method for openai>=1.0.0:
        upload_response = openai.File.upload(file=temp_file_path, purpose="fine-tune")
        file_id = upload_response.get("id")
        if not file_id:
            raise Exception("File upload failed; no file ID returned.")
        
        fine_tune_response = openai.FineTune.create(
            training_file=file_id,
            model="davinci"  # Change this to your desired base model if needed
        )
        
        os.remove(temp_file_path)
        
        return {"detail": "Fine-tuning job started", "job_id": fine_tune_response.get("id")}
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Fine-tuning failed: {str(e)}. If you are using openai>=1.0.0, ensure your code uses the new file upload interface."
        )
