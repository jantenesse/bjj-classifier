export interface ClassificationRequest {
  type: "video";
  content: string; // base64 encoded video
}

export interface ClassificationResult {
  specific_technique: string;
  confidence: number;
}

export interface ClassificationMetadata {
  processing_time_ms: number;
  model_version: string;
}

export interface ClassificationResponse {
  classification: ClassificationResult;
  metadata: ClassificationMetadata;
}

export interface ApiError {
  detail: string;
}