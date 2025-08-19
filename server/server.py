import base64
import os
import sys
import tempfile
import time
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model.model import BJJClassifier
classifier = BJJClassifier()

class ClassificationRequest(BaseModel):
    type: str
    content: str


class ClassificationResponse(BaseModel):
    classification: Dict[str, Any]
    metadata: Dict[str, Any]


app = FastAPI(title="BJJ Classifier API", version="1.0.0")


def handle_upload(request: ClassificationRequest) -> ClassificationResponse:
    """Handle video upload and classification"""
    start_time = time.time()
    
    if request.type != "video":
        raise HTTPException(status_code=400, detail="Only video type is supported")
    
    try:
        # Decode base64 video
        video_data = base64.b64decode(request.content)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
            temp_file.write(video_data)
            temp_path = temp_file.name
        
        try:
            # Extract embedding from video
            input_embedding = classifier.extract_slowfast_embedding(temp_path)
            
            # Make prediction
            technique, confidence = classifier.prediction(input_embedding)
            
            # Calculate processing time
            processing_time = int((time.time() - start_time) * 1000)
            
            return ClassificationResponse(
                classification={
                    "specific_technique": technique,
                    "confidence": round(confidence, 2)
                },
                metadata={
                    "processing_time_ms": processing_time,
                    "model_version": "v1.2.3"
                }
            )
            
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Initialize model and training data on startup"""
    classifier.build_training_data()


@app.post("/classify", response_model=ClassificationResponse)
async def classify_endpoint(request: ClassificationRequest):
    """POST endpoint for video classification"""
    return handle_upload(request)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "BJJ Classifier API v1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)