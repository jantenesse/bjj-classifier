import os
import torch
import torch.nn.functional as F
import cv2
import numpy as np
from torch import nn
from pytorchvideo.models.hub import slowfast_r50
from torchvision.transforms import Compose
import torchvision.transforms._transforms_video as transforms

class BJJClassifier():
    def __init__(self):
          self.model = None
          self.data_dict = None

    def load_slowfast_model(self):
        """Load pretrained SlowFast model and strip classifier head"""
        self.model = slowfast_r50(pretrained=True)
        self.model.blocks[-1].proj = nn.Identity()  # remove classification head
        self.model.eval()
        return self.model

    def get_transform(self):
        """Video transform: normalize pixel values"""
        return Compose([
            transforms.NormalizeVideo(
                mean=[0.45, 0.45, 0.45],
                std=[0.225, 0.225, 0.225]
            )
        ])

    def load_video_frames(self, path, num_frames=32, slowfast_alpha=4):
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

    def pack_pathway(self, video, alpha=4):
        """Prepare video for SlowFast input (two pathways)"""
        fast_pathway = video
        slow_pathway = video[:, :, ::alpha, :, :]
        return [slow_pathway, fast_pathway]

    def extract_slowfast_embedding(self, video_path):
        """Extract embedding from video path"""
        if self.model is None:
            self.model = self.load_slowfast_model()
        
        transform = self.get_transform()
        video = self.load_video_frames(video_path)
        video = transform(video.squeeze(0)).unsqueeze(0)
        inputs = self.pack_pathway(video)

        with torch.no_grad():
            embedding = self.model(inputs)
        return embedding.squeeze(0)  # shape: (2304,)

    def build_training_data(self):
        """Build training embeddings dictionary"""
        if self.data_dict is not None:
            return self.data_dict
            
        self.data_dict = {"training": {}}
        base_path = "/Users/j/code/bjj_classifier/data/training"
        
        for category in os.listdir(base_path):
            if category.startswith("."):
                continue
            category_path = os.path.join(base_path, category)
            self.data_dict["training"][category] = {}
            
            if os.path.exists(category_path):
                for file_name in os.listdir(category_path):
                    if not file_name.startswith("."):
                        video_path = os.path.join(category_path, file_name)
                        try:
                            embedding = self.extract_slowfast_embedding(video_path)
                            self.data_dict["training"][category][file_name] = embedding
                        except Exception as e:
                            print(f"Error processing {video_path}: {e}")

        
        return self.data_dict

    def make_embedding_list(self, dir_name, base_path="/Users/j/code/bjj_classifier/data/training"):
        """Create embedding list for a specific directory"""
        embedding_list = []
        dir_path = os.path.join(base_path, dir_name)

        if not os.path.exists(dir_path):
            return embedding_list

        for file_name in os.listdir(dir_path):
            if file_name.startswith("."):
                continue  # skip hidden files like .DS_Store
            embedding = self.data_dict["training"].get(dir_name, {}).get(file_name)
            if embedding is not None:
                embedding_list.append(embedding)
        print(dir_name)
        return embedding_list
    
    def max_similarity(self, input_embedding, embedding_list):
        """Calculate maximum similarity between input and embedding list"""
        max_percentage = 0.0

        for embedding in embedding_list:
            similarity = F.cosine_similarity(input_embedding.unsqueeze(0), embedding.unsqueeze(0), dim=1).item()
            similarity_percentage = (similarity + 1) * 50  # normalize to 0-100
            max_percentage = max(max_percentage, similarity_percentage)

        print(max_percentage)
        return max_percentage
    
    def prediction(self, input_embedding):
        """Main prediction function based on research notebook"""
        # Build training embeddings dictionary
        base_path = "/Users/j/code/bjj_classifier/data/training"

        embedding_sim_dict = {
            dir_name: self.max_similarity(input_embedding, self.make_embedding_list(dir_name, base_path))
            for dir_name in self.data_dict["training"].keys()
        }

        # Find best match
        if not embedding_sim_dict:
            return "pulling_guard", 0.5  # default fallback
        
        best_match = max(embedding_sim_dict, key=embedding_sim_dict.get)
        confidence = embedding_sim_dict[best_match] / 100.0  # convert back to 0-1 scale
        
        return best_match, confidence