# Quick Deploy Script for TalentTrack (Windows PowerShell)

Write-Host "🚀 TalentTrack Deployment Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Check if git is initialized
if (-Not (Test-Path .git)) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git already initialized" -ForegroundColor Green
}

# Add all files
Write-Host ""
Write-Host "📝 Adding files to git..." -ForegroundColor Yellow
git add .

# Commit
Write-Host ""
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
git commit -m "Deploy TalentTrack application"

# Instructions
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "📋 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create a NEW repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Run these commands:" -ForegroundColor White
Write-Host ""
Write-Host '   git remote add origin https://github.com/YOUR_USERNAME/talenttrack.git' -ForegroundColor Yellow
Write-Host '   git branch -M main' -ForegroundColor Yellow
Write-Host '   git push -u origin main' -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Deploy on Render.com:" -ForegroundColor White
Write-Host "   - Go to: https://render.com" -ForegroundColor Yellow
Write-Host "   - Click: New + → Web Service" -ForegroundColor Yellow
Write-Host "   - Connect your GitHub repository" -ForegroundColor Yellow
Write-Host "   - Configure and Deploy!" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✨ Your app will be live in 2-3 minutes!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
