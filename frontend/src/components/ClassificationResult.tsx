import type { ClassificationResponse } from '../types/api';

interface ClassificationResultProps {
  result: ClassificationResponse;
  onReset: () => void;
}

const ClassificationResult: React.FC<ClassificationResultProps> = ({ result, onReset }) => {
  const confidencePercentage = Math.round(result.classification.confidence * 100);
  
  const getConfidenceColor = (confidence: number): string => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceBgColor = (confidence: number): string => {
    if (confidence >= 0.8) return 'bg-green-100';
    if (confidence >= 0.6) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="w-full max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Classification Result</h2>
        <div className={`inline-block px-4 py-2 rounded-full ${getConfidenceBgColor(result.classification.confidence)}`}>
          <span className="text-lg font-semibold text-gray-800">
            {result.classification.specific_technique}
          </span>
        </div>
      </div>
      
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Confidence:</span>
          <span className={`font-bold text-lg ${getConfidenceColor(result.classification.confidence)}`}>
            {confidencePercentage}%
          </span>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              result.classification.confidence >= 0.8 ? 'bg-green-600' :
              result.classification.confidence >= 0.6 ? 'bg-yellow-600' : 'bg-red-600'
            }`}
            style={{ width: `${confidencePercentage}%` }}
          ></div>
        </div>
        
        <div className="pt-4 border-t border-gray-200">
          <div className="flex justify-between text-sm text-gray-500 mb-2">
            <span>Processing time:</span>
            <span>{result.metadata.processing_time_ms}ms</span>
          </div>
          <div className="flex justify-between text-sm text-gray-500">
            <span>Model version:</span>
            <span>{result.metadata.model_version}</span>
          </div>
        </div>
      </div>
      
      <button
        onClick={onReset}
        className="w-full mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
      >
        Classify Another Video
      </button>
    </div>
  );
};

export default ClassificationResult;