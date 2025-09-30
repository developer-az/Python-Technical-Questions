# Vercel Deployment Guide

This Flask application is configured for deployment on Vercel using serverless functions.

## Configuration Files

- `vercel.json` - Main Vercel configuration
- `api/index.py` - Entry point for Vercel serverless functions
- `.vercelignore` - Files to exclude from deployment

## Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel
   ```

3. **Follow the prompts**:
   - Set up and deploy project
   - Choose Python as the framework
   - Use default settings

## Key Features

- ✅ Full Flask application support
- ✅ Static files (CSS, JS) served correctly
- ✅ Templates rendered properly
- ✅ All API endpoints functional
- ✅ Progressive learning system working
- ✅ Flashcard functionality operational

## Environment Variables

The application uses Python 3.12.3 as specified in `vercel.json`. No additional environment variables are required for basic functionality.

## Testing

After deployment, test these endpoints:
- `/` - Main interface
- `/health` - Health check
- `/flashcard` - Traditional flashcards
- `/flashcard/progressive` - Progressive learning system
- `/api` - API documentation

## Troubleshooting

If you encounter issues:

1. **404 NOT_FOUND**: Ensure `api/index.py` exists and properly imports the Flask app
2. **Import errors**: Check that all dependencies are in `requirements.txt`
3. **Template errors**: Verify templates are in the correct relative path
4. **Static files**: Ensure static assets are properly referenced

## Local Development

For local development, use:
```bash
python app.py
```

The app will run on `http://localhost:5000`