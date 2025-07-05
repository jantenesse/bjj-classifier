# BJJ Classifier API v1 Specification

## High-Level Objective
- API specification for the BJJ (Brazilian Jiu-Jitsu) classifier system that classifies video clips based on specific bjj actions

## Mid-Level Objectives
- Create /classify endpoint that supports POST of JSON that includes a base64 encoded video clip

## Implementation Notes
- Use the latest fastAPI
- Use lastest pydantic
- Use lastest jsonify

## Context

### Beginning Context
- `research/predict_functions.ipynb`

### Ending Context
- `server/server.py`
- `pyproject.toml`

## Low Level Tasks
> Ordered from start to finish

1. Create a function called `handle_upload` that accepts base64 encoded video and returns json 
**Request:**
```json
{
  "type": "video",
  "content": "base64_encoded_data"
}
```

**Response:**
```json
{
  "classification": {
    "specific_technique": "closed_guard",
    "confidence": 0.92,
  "metadata": {
    "processing_time_ms": 150,
    "model_version": "v1.2.3"
  }
}
```
2. Create an app route for /classify with method POST for `handle_upload`
3. Create prediction method for `handle_upload` based on `prediction06` in `research/predict_functions.ipynb`. The `specific_technique` should be either `pulling_guard` or `passing_guard` in the first version. Make `confidence` the similarity score in `prediction06`