#!/bin/bash

echo "🚀 Python Technical Questions - Deployment Script"
echo "=================================================="

# Check if git is clean
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Please commit all changes before deploying"
    exit 1
fi

echo "✅ Git repository is clean"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin master

echo "✅ Code pushed to GitHub"
echo ""
echo "🌐 Next Steps:"
echo "1. Go to https://render.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'New Web Service'"
echo "4. Select this repository"
echo "5. Configure:"
echo "   - Name: python-technical-questions"
echo "   - Environment: Python"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn app:app"
echo "6. Click 'Create Web Service'"
echo ""
echo "🎉 Your app will be live in a few minutes!"
