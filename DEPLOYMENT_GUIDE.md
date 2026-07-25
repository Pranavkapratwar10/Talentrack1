# 🚀 Free Deployment Guide for TalentTrack

## 🎯 Best Free Hosting Options (2026)

I'll show you **5 free platforms** where you can deploy TalentTrack and get a public URL!

---

## ⭐ Option 1: Render.com (RECOMMENDED - Easiest!)

**Why Render?**
- ✅ 100% Free tier (no credit card needed)
- ✅ Automatic HTTPS
- ✅ Easy deployment from GitHub
- ✅ Supports SQLite and file uploads
- ✅ Auto-deploy on git push
- ✅ Get URL like: `https://talenttrack.onrender.com`

### 📝 Steps:

#### 1. Prepare Your Code
```bash
# In your project folder
git init
git add .
git commit -m "Initial commit"
```

#### 2. Push to GitHub
```bash
# Create a new repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/talenttrack.git
git branch -M main
git push -u origin main
```

#### 3. Deploy on Render
1. Go to https://render.com
2. Click **"Sign Up"** (use GitHub account)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name:** `talenttrack`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** `Free`
6. Click **"Create Web Service"**
7. Wait 2-3 minutes for deployment
8. **Done!** You'll get a URL like: `https://talenttrack.onrender.com`

⚠️ **Note:** Free tier sleeps after 15 min of inactivity. First request takes 30-60 seconds to wake up.

---

## ⭐ Option 2: Railway.app

**Why Railway?**
- ✅ $5 free credit monthly
- ✅ Very fast deployment
- ✅ Great for Flask apps
- ✅ Better performance than Render
- ✅ Get URL like: `https://talenttrack.up.railway.app`

### 📝 Steps:

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Choose **"Deploy from GitHub repo"**
4. Select your repository
5. Railway auto-detects Python and deploys!
6. **Done!** Get your URL from dashboard

---

## ⭐ Option 3: PythonAnywhere

**Why PythonAnywhere?**
- ✅ 100% Free forever
- ✅ Good for Flask apps
- ✅ Persistent storage
- ✅ Get URL like: `https://yourname.pythonanywhere.com`

### 📝 Steps:

1. Go to https://www.pythonanywhere.com
2. Create free account
3. Go to **"Web"** tab → **"Add a new web app"**
4. Choose **"Flask"** → **"Python 3.10"**
5. Upload your code:
   - Click **"Files"** tab
   - Upload all files or use git clone
6. Configure WSGI file:
   - Click on WSGI config file
   - Point to your `app.py`
7. Click **"Reload"** 
8. **Done!** Access at `https://yourname.pythonanywhere.com`

---

## ⭐ Option 4: Vercel (With Modifications)

**Why Vercel?**
- ✅ Super fast CDN
- ✅ Automatic HTTPS
- ✅ GitHub integration
- ✅ Get URL like: `https://talenttrack.vercel.app`

### 📝 Steps:

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

3. Deploy:
```bash
vercel
```

4. Follow prompts and get your URL!

⚠️ **Note:** Vercel has limitations with file uploads. Better for read-only apps.

---

## ⭐ Option 5: Fly.io

**Why Fly.io?**
- ✅ Free tier with 3 VMs
- ✅ Global deployment
- ✅ Full app support
- ✅ Get URL like: `https://talenttrack.fly.dev`

### 📝 Steps:

1. Install Fly CLI:
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

2. Login:
```bash
fly auth login
```

3. Launch app:
```bash
fly launch
```

4. Follow prompts (use defaults)
5. Deploy:
```bash
fly deploy
```

6. **Done!** Get URL from output

---

## 🏆 My Recommendation: **Render.com**

**Best for your TalentTrack app because:**
1. ✅ No credit card needed
2. ✅ Supports file uploads (resumes, logos)
3. ✅ SQLite database works perfectly
4. ✅ Easy GitHub integration
5. ✅ Free HTTPS certificate
6. ✅ Simple deployment process

---

## 🚀 Quick Deploy Guide (Render - Recommended)

### Step 1: Create GitHub Repository

```bash
# Initialize git (if not already done)
cd d:\pranav__all_projects\talenttrack
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - TalentTrack application"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/talenttrack.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. **Sign up:** https://render.com (use GitHub account)
2. **New Web Service** → Connect GitHub → Select repository
3. **Configure:**
   - Name: `talenttrack` (or any name you want)
   - Environment: `Python 3`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Plan: **Free**
4. **Advanced Settings (Optional):**
   - Add environment variable: `GROQ_API_KEY` = `your_key`
5. **Create Web Service**
6. **Wait 2-3 minutes**
7. **Done! ✨** Your app is live!

### Step 3: Access Your App

You'll get a URL like:
```
https://talenttrack.onrender.com
```

Or with your chosen name:
```
https://YOUR_APP_NAME.onrender.com
```

---

## 🔐 Important: Environment Variables

Add these environment variables in Render dashboard:

```
GROQ_API_KEY=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
SECRET_KEY=your-secret-key-change-this-to-random-string
```

---

## 📊 Comparison Table

| Platform | Free Tier | File Upload | Database | Speed | Best For |
|----------|-----------|-------------|----------|-------|----------|
| **Render** | ✅ Yes | ✅ Yes | ✅ SQLite | ⭐⭐⭐ | Full apps |
| **Railway** | ✅ $5/mo | ✅ Yes | ✅ SQLite | ⭐⭐⭐⭐ | Performance |
| **PythonAnywhere** | ✅ Forever | ✅ Yes | ✅ SQLite | ⭐⭐ | Simple apps |
| **Vercel** | ✅ Yes | ❌ Limited | ❌ No | ⭐⭐⭐⭐⭐ | Static/API |
| **Fly.io** | ✅ Yes | ✅ Yes | ✅ SQLite | ⭐⭐⭐⭐ | Advanced |

---

## ⚠️ Important Notes

### Database Persistence
- **Render Free Tier:** Database resets on restart (use PostgreSQL add-on for persistence)
- **Solution:** Upload sample data or connect to external database

### File Uploads
- Uploaded resumes persist during session
- For permanent storage, consider:
  - AWS S3 (free tier: 5GB)
  - Cloudinary (free tier: 25GB)
  - Supabase Storage (free tier: 1GB)

### Performance
- Free tiers may "sleep" after inactivity
- First request may take 30-60 seconds
- Perfect for demo/portfolio projects

---

## 🎯 Next Steps After Deployment

1. **Test Your App:**
   - Visit your URL
   - Create account
   - Upload resume
   - Apply for jobs

2. **Share Your Link:**
   ```
   🌐 Live Demo: https://talenttrack.onrender.com
   📝 GitHub: https://github.com/YOUR_USERNAME/talenttrack
   ```

3. **Update README:**
   - Add live demo link
   - Add deployment badges
   - Add screenshots

---

## 🆘 Troubleshooting

### App doesn't start:
```bash
# Check logs in Render dashboard
# Or locally test with:
gunicorn app:app
```

### Database errors:
- Ensure `instance` folder exists
- Check file permissions
- Database recreates on each deploy (free tier)

### Import errors:
- Verify `requirements.txt` is complete
- Check Python version matches runtime.txt

---

## 📚 Additional Resources

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **Flask Deployment:** https://flask.palletsprojects.com/en/stable/deploying/

---

## 🎉 You're Ready to Deploy!

Choose **Render.com** for easiest deployment, then share your live link! 🚀

**Questions? Issues?** Check the troubleshooting section or platform docs.

---

**Happy Deploying! ✨**
