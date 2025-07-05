import base64
import io
import os
import tempfile
import time
from typing import Dict, Any
import string

import torch
import torch.nn.functional as F
import cv2
import numpy as np
from torch import nn
from pytorchvideo.models.hub import slowfast_r50
from torchvision.transforms import Compose
import torchvision.transforms._transforms_video as transforms
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# this is temporary
import sys
sys.path.append("model")
print(sys.path)
import model


model.classify()


class ClassificationRequest(BaseModel):
    type: str
    content: str


class ClassificationResponse(BaseModel):
    classification: Dict[str, Any]
    metadata: Dict[str, Any]


app = FastAPI(title="BJJ Classifier API", version="1.0.0")

# Global model and data storage
model = None
data_dict = None


def load_slowfast_model():
    """Load pretrained SlowFast model and strip classifier head"""
    model = slowfast_r50(pretrained=True)
    model.blocks[-1].proj = nn.Identity()  # remove classification head
    model.eval()
    return model


def get_transform():
    """Video transform: normalize pixel values"""
    return Compose([
        transforms.NormalizeVideo(
            mean=[0.45, 0.45, 0.45],
            std=[0.225, 0.225, 0.225]
        )
    ])


def load_video_frames(path, num_frames=32, slowfast_alpha=4):
    """Load video frames and format for SlowFast"""
    cap = cv2.VideoCapture(path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    sample_rate = max(total_frames // num_frames, 1)

    frames = []
    for i in range(num_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * sample_rate)
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (224, 224))
        frames.append(frame)

    cap.release()

    if len(frames) < num_frames:
        raise ValueError(f"Only {len(frames)} frames could be read. Expected {num_frames}.")

    video = np.stack(frames)  # (T, H, W, C)
    video = torch.from_numpy(video).float() / 255.0  # Normalize to [0, 1]
    video = video.permute(3, 0, 1, 2)  # (C, T, H, W)
    video = video.unsqueeze(0)  # (B, C, T, H, W)
    return video


def pack_pathway(video, alpha=4):
    """Prepare video for SlowFast input (two pathways)"""
    fast_pathway = video
    slow_pathway = video[:, :, ::alpha, :, :]
    return [slow_pathway, fast_pathway]


def extract_slowfast_embedding(video_path):
    """Extract embedding from video path"""
    global model
    if model is None:
        model = load_slowfast_model()
    
    transform = get_transform()
    video = load_video_frames(video_path)
    video = transform(video.squeeze(0)).unsqueeze(0)
    inputs = pack_pathway(video)

    with torch.no_grad():
        embedding = model(inputs)
    return embedding.squeeze(0)  # shape: (2304,)


def build_training_data():
    """Build training embeddings dictionary"""
    global data_dict
    if data_dict is not None:
        return data_dict
        
    data_dict = {"training": {}}
    base_path = "/Users/j/code/bjj_classifier/data/training"
    
    for category in ["pulling_guard", "passing_guard"]:
        category_path = os.path.join(base_path, category)
        data_dict["training"][category] = {}
        
        if os.path.exists(category_path):
            for file_name in os.listdir(category_path):
                if not file_name.startswith("."):
                    video_path = os.path.join(category_path, file_name)
                    try:
                        embedding = extract_slowfast_embedding(video_path)
                        data_dict["training"][category][file_name] = embedding
                    except Exception as e:
                        print(f"Error processing {video_path}: {e}")
    
    return data_dict


def make_embedding_list(dir_name, base_path="/Users/j/code/bjj_classifier/data/training"):
    """Create embedding list for a specific directory"""
    embedding_list = []
    dir_path = os.path.join(base_path, dir_name)

    if not os.path.exists(dir_path):
        return embedding_list

    for file_name in os.listdir(dir_path):
        if file_name.startswith("."):
            continue  # skip hidden files like .DS_Store
        embedding = data_dict["training"].get(dir_name, {}).get(file_name)
        if embedding is not None:
            embedding_list.append(embedding)

    return embedding_list


def max_similarity(input_embedding, embedding_list):
    """Calculate maximum similarity between input and embedding list"""
    max_percentage = 0.0

    for embedding in embedding_list:
        similarity = F.cosine_similarity(input_embedding.unsqueeze(0), embedding.unsqueeze(0), dim=1).item()
        similarity_percentage = (similarity + 1) * 50  # normalize to 0-100
        max_percentage = max(max_percentage, similarity_percentage)

    return max_percentage


def prediction06(input_embedding):
    """Main prediction function based on research notebook"""
    # Build training embeddings dictionary
    base_path = "/Users/j/code/bjj_classifier/data/training"
    dir_dict = {
        dir_name: make_embedding_list(dir_name, base_path)
        for dir_name in os.listdir(base_path)
        if not dir_name.startswith(".")
    }
    
    # Compute similarity scores
    embedding_sim_dict = {
        dir_name: max_similarity(input_embedding, embeddings)
        for dir_name, embeddings in dir_dict.items()
        if embeddings
    }

    # Find best match
    if not embedding_sim_dict:
        return "pulling_guard", 0.5  # default fallback
    
    best_match = max(embedding_sim_dict, key=embedding_sim_dict.get)
    confidence = embedding_sim_dict[best_match] / 100.0  # convert back to 0-1 scale
    
    return best_match, confidence


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
            print(f"this is the temp path {temp_path}")
        
        try:
            # Extract embedding from video
            input_embedding = extract_slowfast_embedding(temp_path)
            
            # Make prediction
            technique, confidence = prediction06(input_embedding)
            
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
    build_training_data()


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