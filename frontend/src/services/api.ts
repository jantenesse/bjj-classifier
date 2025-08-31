import axios from 'axios';
import type { AxiosResponse } from 'axios';
import type { ClassificationRequest, ClassificationResponse, ApiError } from '../types/api';

const API_BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const classifyVideo = async (videoFile: File): Promise<ClassificationResponse> => {
  try {
    // Convert file to base64
    const base64Video = await fileToBase64(videoFile);
    
    const request: ClassificationRequest = {
      type: 'video',
      content: base64Video,
    };

    const response: AxiosResponse<ClassificationResponse> = await apiClient.post('/classify', request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data) {
      const apiError = error.response.data as ApiError;
      throw new Error(apiError.detail || 'Classification failed');
    }
    throw new Error('Network error or server unavailable');
  }
};

const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      // Remove the data URL prefix (data:video/mp4;base64,)
      const base64 = result.split(',')[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

export const validateVideoFile = (file: File): boolean => {
  const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/quicktime'];
  const maxSize = 100 * 1024 * 1024; // 100MB

  return allowedTypes.includes(file.type) && file.size <= maxSize;
};