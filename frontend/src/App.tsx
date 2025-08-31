import { useState } from 'react';
import VideoUploader from './components/VideoUploader';
import ClassificationResult from './components/ClassificationResult';
import LoadingSpinner from './components/LoadingSpinner';
import { classifyVideo } from './services/api';
import type { ClassificationResponse } from './types/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ClassificationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleVideoSelect = async (file: File) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const classificationResult = await classifyVideo(file);
      setResult(classificationResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Classification failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            BJJ Technique Classifier
          </h1>
          <p className="text-gray-600">
            Upload a video to classify Brazilian Jiu-Jitsu techniques
          </p>
        </div>

        <div className="flex justify-center">
          {isLoading ? (
            <LoadingSpinner message="Analyzing your video..." />
          ) : result ? (
            <ClassificationResult result={result} onReset={handleReset} />
          ) : (
            <VideoUploader onVideoSelect={handleVideoSelect} isLoading={isLoading} />
          )}
        </div>

        {error && (
          <div className="max-w-md mx-auto mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="mt-1 text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
