from fastapi import APIRouter, HTTPException, UploadFile, File
import openai
import os
from app.config import OPENAI_API_KEY

router = APIRouter()

# Set the OpenAI API key from your configuration
openai.api_key = OPENAI_API_KEY

@router.post("/fine-tune")
async def fine_tune(file: UploadFile = File(...)):
    """
    Fine-tune a model using a client-provided JSONL training file.
    The file must be in JSONL format with training examples.
    """
    # Validate that the file is a JSONL file
    filename = file.filename
    if not filename.endswith(".jsonl"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .jsonl files are accepted.")
    
    # Save the uploaded file to a temporary directory
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
        # Upload the file to OpenAI to obtain a file ID for fine-tuning
        with open(temp_file_path, "rb") as f:
            upload_response = openai.File.create(
                file=f,
                purpose="fine-tune"
            )
        file_id = upload_response.get("id")
        if not file_id:
            raise Exception("File upload failed; no file ID returned.")
        
        # Create a fine-tuning job using the uploaded file and a base model (e.g., "davinci")
        fine_tune_response = openai.FineTune.create(
            training_file=file_id,
            model="davinci"  # Change this to your desired base model if needed
        )
        
        # Clean up: Remove the temporary file
        os.remove(temp_file_path)
        
        return {"detail": "Fine-tuning job started", "job_id": fine_tune_response.get("id")}
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Fine-tuning failed: {str(e)}")
