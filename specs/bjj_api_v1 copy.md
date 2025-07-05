# BJJ Classifier API v1 Specification

## Overview
API specification for the BJJ (Brazilian Jiu-Jitsu) classifier system that categorizes techniques, positions, and movements.

## Base URL
```
https://api.bjjclassifier.com/v1
```

## Authentication
```
Authorization: Bearer <token>
```

## Endpoints

### Classifications

#### GET /classifications
Get all available classification categories.

**Response:**
```json
{
  "categories": [
    {
      "id": "positions",
      "name": "Positions",
      "subcategories": ["guard", "mount", "side_control", "back_control"]
    },
    {
      "id": "techniques",
      "name": "Techniques", 
      "subcategories": ["submissions", "sweeps", "escapes", "transitions"]
    }
  ]
}
```

#### POST /classify
Classify BJJ content (image, video, or text description).

**Request:**
```json
{
  "type": "image|video|text",
  "content": "base64_encoded_data|url|text_description",
  "context": {
    "gi": true,
    "level": "beginner|intermediate|advanced"
  }
}
```

**Response:**
```json
{
  "classification": {
    "primary_category": "positions",
    "subcategory": "guard",
    "specific_technique": "closed_guard",
    "confidence": 0.92,
    "alternative_classifications": [
      {
        "technique": "full_guard",
        "confidence": 0.78
      }
    ]
  },
  "metadata": {
    "processing_time_ms": 150,
    "model_version": "v1.2.3"
  }
}
```

### Techniques

#### GET /techniques
List all techniques in the database.

**Query Parameters:**
- `category`: Filter by category (optional)
- `level`: Filter by difficulty level (optional)
- `gi`: Filter by gi/no-gi (optional)
- `limit`: Results per page (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "techniques": [
    {
      "id": "armbar_from_guard",
      "name": "Armbar from Guard",
      "category": "submissions",
      "subcategory": "arm_attacks",
      "level": "beginner",
      "gi_applicable": true,
      "nogi_applicable": true,
      "description": "Classic armbar submission from closed guard position",
      "key_points": [
        "Control opponent's posture",
        "Pivot underneath",
        "Isolate the arm"
      ]
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

#### GET /techniques/{id}
Get detailed information about a specific technique.

**Response:**
```json
{
  "technique": {
    "id": "armbar_from_guard",
    "name": "Armbar from Guard",
    "category": "submissions",
    "subcategory": "arm_attacks",
    "level": "beginner",
    "gi_applicable": true,
    "nogi_applicable": true,
    "description": "Classic armbar submission from closed guard position",
    "setup_positions": ["closed_guard", "high_guard"],
    "key_points": [
      "Control opponent's posture",
      "Pivot underneath", 
      "Isolate the arm"
    ],
    "common_mistakes": [
      "Not controlling posture first",
      "Telegraphing the movement"
    ],
    "variations": [
      "armbar_from_high_guard",
      "armbar_with_cross_grip"
    ],
    "counters": [
      "posture_and_stack",
      "hitchhiker_escape"
    ]
  }
}
```

### Training Data

#### POST /training/feedback
Submit feedback on classification accuracy.

**Request:**
```json
{
  "classification_id": "uuid",
  "correct_classification": {
    "category": "positions",
    "subcategory": "mount",
    "specific_technique": "high_mount"
  },
  "user_rating": 1-5,
  "comments": "Optional feedback text"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Feedback recorded"
}
```

## Error Responses

All endpoints return errors in this format:
```json
{
  "error": {
    "code": "CLASSIFICATION_FAILED",
    "message": "Unable to classify the provided content",
    "details": "Content format not supported"
  }
}
```

### Error Codes
- `INVALID_REQUEST`: Malformed request
- `AUTHENTICATION_FAILED`: Invalid or missing auth token  
- `CLASSIFICATION_FAILED`: Unable to process classification
- `TECHNIQUE_NOT_FOUND`: Requested technique doesn't exist
- `RATE_LIMIT_EXCEEDED`: Too many requests

## Rate Limits
- Classification endpoints: 100 requests/minute
- Read-only endpoints: 1000 requests/minute

## Webhooks (Future)
Support for real-time classification updates and training notifications.

## SDK Support
- Python SDK: `pip install bjj-classifier-sdk`
- JavaScript SDK: `npm install bjj-classifier-js`