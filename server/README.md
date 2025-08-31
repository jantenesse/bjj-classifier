# BJJ Technique Classifier - Backend API

A FastAPI-based REST API for classifying Brazilian Jiu-Jitsu techniques from video uploads using machine learning models.

## Features

- **Video Classification**: Classify BJJ techniques from uploaded video files
- **Base64 Video Processing**: Accept base64-encoded video content
- **Real-time Processing**: Fast video analysis and technique prediction
- **CORS Support**: Configured for frontend integration
- **Error Handling**: Comprehensive error responses with detailed messages
- **Metadata Tracking**: Processing time and model version information

## Prerequisites

- **Python** (version 3.8 or higher)
- **Poetry** (for dependency management)
- **BJJ Classifier Model** (in the `model/` directory)
- **Training Data** (in the `data/` directory)

## Quick Start

1. **Install dependencies**
   ```bash
   poetry install
   ```

2. **Activate virtual environment**
   ```bash
   poetry shell
   ```

3. **Start the server**
   ```bash
   python server.py
   ```

4. **Access the API**
   - API runs on `http://localhost:8000`
   - Interactive docs at `http://localhost:8000/docs`
   - OpenAPI spec at `http://localhost:8000/openapi.json`

## API Endpoints

### GET /
**Root endpoint** - Returns API information and version.

**Response:**
```json
{
  "message": "BJJ Classifier API v1.0.0"
}
```

### POST /classify
**Video classification endpoint** - Analyzes uploaded video and returns technique classification.

**Request Body:**
```json
{
  "type": "video",
  "content": "base64_encoded_video_data"
}
```

**Response:**
```json
{
  "classification": {
    "specific_technique": "double_leg",
    "confidence": 0.87
  },
  "metadata": {
    "processing_time_ms": 1250,
    "model_version": "v1.2.3"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid request format or unsupported file type
- `500 Internal Server Error` - Classification processing failed

## Configuration

### CORS Settings
The API is configured to accept requests from:
- `http://localhost:5173` (frontend development server)
- `http://127.0.0.1:5173` (alternative localhost)

To modify CORS settings, update the middleware configuration in `server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Server Settings
- **Host**: `0.0.0.0` (accepts connections from any IP)
- **Port**: `8000`
- **Auto-reload**: Disabled in production

## Model Integration

The server integrates with the BJJ Classifier model located in `../model/model.py`:

### Model Methods Used:
- `extract_slowfast_embedding(video_path)` - Extract features from video
- `prediction(embedding)` - Classify technique from embedding
- `build_training_data()` - Initialize model with training data

### Supported Techniques:
The model can classify the following BJJ techniques:
- Double leg takedown
- Single leg takedown  
- Hip throw
- Guard pulling
- Guard passing

## File Processing

### Video Handling:
1. **Input**: Base64-encoded video content
2. **Temporary Storage**: Video saved to temp file for processing
3. **Feature Extraction**: SlowFast model extracts video embeddings
4. **Classification**: ML model predicts technique and confidence
5. **Cleanup**: Temporary files automatically deleted

### Supported Formats:
- MP4 (recommended)
- AVI
- MOV
- Any format supported by the underlying ML model

## Development

### Project Structure
```
server/
├── server.py          # Main FastAPI application
├── server1.py         # Alternative server implementation
└── README.md          # This file
```

### Adding New Endpoints
1. Define request/response models using Pydantic
2. Create endpoint handler functions
3. Register routes with FastAPI decorators
4. Update CORS settings if needed

### Error Handling
The server implements comprehensive error handling:
- Input validation errors (400)
- Processing failures (500)
- Detailed error messages for debugging

## Logging and Monitoring

### Processing Metrics:
- **Processing Time**: Measured in milliseconds
- **Model Version**: Tracked in response metadata
- **Error Tracking**: Exceptions logged with full stack traces

### Performance Monitoring:
Monitor these key metrics:
- Response times for `/classify` endpoint
- Memory usage during video processing
- Error rates and types

## Production Deployment

### Environment Setup:
1. **Install production dependencies**
   ```bash
   poetry install --no-dev
   ```

2. **Configure production settings**
   ```bash
   # Set environment variables
   export PYTHONPATH=/path/to/bjj_classifier
   ```

3. **Run with production WSGI server**
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Production Considerations:
- Use a reverse proxy (nginx) for static files and SSL
- Configure proper logging levels
- Set up health check endpoints
- Implement rate limiting for the `/classify` endpoint
- Monitor disk space for temporary file processing

## Troubleshooting

### Common Issues:

**Model Loading Errors:**
- Ensure the `model/` directory contains required model files
- Check that training data is available in `data/training/`
- Verify Python path includes the project root

**CORS Issues:**
- Check that frontend URL is in `allow_origins` list
- Ensure both frontend and backend are running
- Verify browser is not caching CORS preflight responses

**Video Processing Errors:**
- Check video file format compatibility
- Monitor available disk space for temporary files
- Verify base64 encoding is valid

**Memory Issues:**
- Large video files may consume significant memory
- Consider implementing file size limits
- Monitor system memory during processing

### Debug Mode:
Run with debug logging:
```bash
python server.py --log-level debug
```

## API Testing

### Using cURL:
```bash
# Test root endpoint
curl http://localhost:8000/

# Test classification (with base64 video)
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"type": "video", "content": "base64_video_data_here"}'
```

### Using Python requests:
```python
import requests
import base64

# Load and encode video
with open("video.mp4", "rb") as f:
    video_data = base64.b64encode(f.read()).decode()

# Make classification request
response = requests.post(
    "http://localhost:8000/classify",
    json={"type": "video", "content": video_data}
)
print(response.json())
```

## Contributing

1. Follow FastAPI best practices for endpoint design
2. Add proper type hints and Pydantic models
3. Include error handling for new endpoints
4. Update CORS settings when adding new routes
5. Test with both valid and invalid inputs