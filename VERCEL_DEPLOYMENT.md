# Vercel Deployment Guide

This Flask application is configured for deployment on Vercel using serverless functions.

## Configuration Files

- `vercel.json` - Main Vercel configuration
- `api/app.py` - Primary entry point for Vercel serverless functions  
- `api/index.py` - Alternative entry point (backup)
- `.vercelignore` - Files to exclude from deployment

## Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel --prod
   ```

3. **Follow the prompts**:
   - Set up and deploy project
   - Choose "Other" as the framework (don't select Python/Flask preset)
   - Use default build settings

## Key Features

- ✅ Full Flask application support
- ✅ Static files (CSS, JS) served correctly
- ✅ Templates rendered properly
- ✅ All API endpoints functional
- ✅ Progressive learning system working
- ✅ Flashcard functionality operational

## Updated Configuration

The configuration has been optimized for better Vercel compatibility:

- **Entry Point**: `api/app.py` (simplified import structure)
- **Python Version**: Uses Vercel's default Python runtime
- **Static Files**: Proper routing for CSS/JS assets
- **Function Timeout**: 30 seconds for complex operations

## Environment Variables

No additional environment variables are required for basic functionality.

## Testing

After deployment, test these endpoints:
- `/` - Main interface
- `/health` - Health check
- `/flashcard` - Traditional flashcards
- `/flashcard/progressive` - Progressive learning system
- `/api` - API documentation

## Common Issues & Solutions

### 1. **Import Errors**
- **Issue**: Module not found errors
- **Solution**: Ensure all dependencies are in `requirements.txt`
- **Check**: Verify Python path configuration in `api/app.py`

### 2. **404 NOT_FOUND Errors**
- **Issue**: Routes not working
- **Solution**: Check `vercel.json` routing configuration
- **Verify**: Ensure `api/app.py` exists and imports correctly

### 3. **Function Timeouts**
- **Issue**: Complex operations timing out
- **Solution**: Already configured with 30-second timeout
- **Alternative**: Break down complex operations

### 4. **Static Files Not Loading**
- **Issue**: CSS/JS files not found
- **Solution**: Static files are routed separately in `vercel.json`
- **Check**: Verify files exist in `/static` directory

## Local Development

For local development, use:
```bash
python app.py
```

The app will run on `http://localhost:5000`

## Deployment Verification

After deployment, verify these work:

1. **Main page loads**: `https://your-app.vercel.app/`
2. **API responds**: `https://your-app.vercel.app/health`
3. **Progressive learning**: `https://your-app.vercel.app/flashcard/progressive`
4. **Static files**: Check if styles are applied correctly

## Troubleshooting Steps

If deployment fails:

1. **Check build logs** in Vercel dashboard
2. **Verify requirements.txt** contains all dependencies
3. **Test locally** with `python api/app.py`
4. **Simplify imports** if needed
5. **Check Python version compatibility**

## Support

If issues persist, check:
- Vercel Python runtime documentation
- Flask deployment guides
- This repository's issues section