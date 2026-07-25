#!/bin/bash

# Quick Deploy Script for TalentTrack

echo "🚀 TalentTrack Deployment Script"
echo "================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add all files
echo ""
echo "📝 Adding files to git..."
git add .

# Commit
echo ""
echo "💾 Committing changes..."
git commit -m "Deploy TalentTrack application"

# Instructions for GitHub
echo ""
echo "================================"
echo "📋 NEXT STEPS:"
echo "================================"
echo ""
echo "1. Create a NEW repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/talenttrack.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy on Render.com:"
echo "   - Go to: https://render.com"
echo "   - Click: New + → Web Service"
echo "   - Connect your GitHub repository"
echo "   - Deploy!"
echo ""
echo "================================"
echo "✨ Your app will be live in 2-3 minutes!"
echo "================================"
