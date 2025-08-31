import React, { useState, useRef } from 'react';
import type { DragEvent } from 'react';
import { validateVideoFile } from '../services/api';

interface VideoUploaderProps {
  onVideoSelect: (file: File) => void;
  isLoading?: boolean;
}

const VideoUploader: React.FC<VideoUploaderProps> = ({ onVideoSelect, isLoading = false }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  };

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleFileSelect = (file: File) => {
    setError(null);

    if (!validateVideoFile(file)) {
      if (file.size > 100 * 1024 * 1024) {
        setError('File size must be less than 100MB');
      } else {
        setError('Please select a valid video file (MP4, AVI, MOV)');
      }
      return;
    }

    onVideoSelect(file);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const openFileDialog = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div
        className={`
          border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 cursor-pointer
          ${isDragOver 
            ? 'border-blue-500 bg-blue-50' 
            : isLoading 
              ? 'border-gray-300 bg-gray-50 cursor-not-allowed' 
              : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
          }
        `}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={!isLoading ? openFileDialog : undefined}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="video/*"
          onChange={handleFileInputChange}
          className="hidden"
          disabled={isLoading}
        />
        
        <div className="space-y-4">
          <div className="mx-auto w-16 h-16 flex items-center justify-center bg-gray-100 rounded-full">
            <svg
              className="w-8 h-8 text-gray-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
              />
            </svg>
          </div>
          
          {isLoading ? (
            <p className="text-gray-500">Processing video...</p>
          ) : (
            <>
              <h3 className="text-lg font-medium text-gray-900">
                Upload BJJ Video
              </h3>
              <div className="text-sm text-gray-600">
                <p>Drag and drop your video here, or click to browse</p>
                <p className="mt-1">Supports MP4, AVI, MOV (max 100MB)</p>
              </div>
            </>
          )}
        </div>
      </div>
      
      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
    </div>
  );
};

export default VideoUploader;