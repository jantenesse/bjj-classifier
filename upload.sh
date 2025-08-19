#!/bin/bash

base64 -i /Users/j/code/bjj_classifier/data/test/double_leg/double_leg06.mp4 > /tmp/video_b64.txt

# Create JSON payload file
echo '{"type": "video", "content": "' > /tmp/payload.json
cat /tmp/video_b64.txt >> /tmp/payload.json
echo '"}' >> /tmp/payload.json

# Send the request
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d @/tmp/payload.json

# Clean up
rm /tmp/video_b64.txt /tmp/payload.json