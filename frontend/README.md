# BJJ Technique Classifier - Frontend

A React TypeScript single-page application for uploading and classifying Brazilian Jiu-Jitsu technique videos.

## Features

- **Drag & Drop Upload**: Intuitive video file upload with drag and drop support
- **Real-time Classification**: Get instant technique classification with confidence scores
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **File Validation**: Client-side validation for video formats and file sizes
- **Modern UI**: Clean, professional interface using Tailwind CSS

## Prerequisites

- **Node.js** (version 18 or higher)
- **npm** (comes with Node.js)
- **Backend API** running on `http://localhost:8000`

## Quick Start

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Open in browser**
   - Navigate to `http://localhost:5173`
   - The app will automatically reload when you make changes

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint to check code quality

## Project Structure

```
src/
├── components/          # Reusable React components
│   ├── VideoUploader.tsx    # Drag & drop video upload component
│   ├── ClassificationResult.tsx  # Display classification results
│   └── LoadingSpinner.tsx   # Loading state component
├── services/           # API service layer
│   └── api.ts             # HTTP client and video classification API
├── types/              # TypeScript type definitions
│   └── api.ts             # API request/response types
├── App.tsx             # Main application component
├── main.tsx            # Application entry point
└── index.css           # Tailwind CSS imports
```

## Configuration

### API Endpoint
The frontend is configured to communicate with the backend API at:
```
http://localhost:8000
```

To change the API URL, update the `API_BASE_URL` in `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000';
```

### File Upload Limits
Current file validation settings:
- **Supported formats**: MP4, AVI, MOV, QuickTime
- **Maximum file size**: 100MB
- **File validation**: Client-side validation before upload

## Development

### Code Style
- Uses **TypeScript** for type safety
- **ESLint** for code linting
- **Prettier** formatting (if configured in your editor)
- **Tailwind CSS** for styling

### Component Guidelines
- Use functional components with React hooks
- Implement proper TypeScript interfaces for props
- Follow the existing component structure and naming conventions
- Use Tailwind CSS classes for styling

### Adding New Features
1. Create components in `src/components/`
2. Add API functions in `src/services/api.ts`
3. Define types in `src/types/api.ts`
4. Update the main `App.tsx` to integrate new features

## Building for Production

1. **Build the project**
   ```bash
   npm run build
   ```

2. **Preview production build**
   ```bash
   npm run preview
   ```

The build outputs to the `dist/` directory and is optimized for production.

## API Integration

The frontend communicates with the BJJ Classifier API using these endpoints:

### POST /classify
Uploads and classifies video files.

**Request Format:**
```typescript
{
  type: "video",
  content: string // base64 encoded video
}
```

**Response Format:**
```typescript
{
  classification: {
    specific_technique: string,
    confidence: number
  },
  metadata: {
    processing_time_ms: number,
    model_version: string
  }
}
```

## Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure:
1. The backend server includes CORS middleware
2. The backend allows requests from `http://localhost:5173`
3. Both frontend and backend are running

### File Upload Issues
- Ensure files are under 100MB
- Use supported video formats (MP4, AVI, MOV)
- Check browser console for specific error messages

### Build Errors
- Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
- Check TypeScript errors: `npm run build`
- Verify all imports use correct paths

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

Modern browsers with ES6+ support are required.

## Contributing

1. Follow the existing code style and structure
2. Add TypeScript types for new features
3. Test your changes in both development and production builds
4. Ensure the app works with drag & drop and click-to-upload flows