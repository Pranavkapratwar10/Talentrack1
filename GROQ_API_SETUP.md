# 🔑 Groq API Setup Guide

## Why You Need This

TalentTrack uses **Groq AI** (powered by Llama 3.3) to intelligently extract detailed information from resumes including:
- ✅ All technical skills
- ✅ Work experience and years
- ✅ Education details with institutions
- ✅ Certifications
- ✅ Projects with descriptions
- ✅ Professional summary

Without a valid API key, the system falls back to basic keyword matching which provides limited information.

---

## 🚀 How to Get Your FREE Groq API Key

### Step 1: Sign Up for Groq
1. Go to **https://console.groq.com/**
2. Click **"Sign Up"** or **"Get Started"**
3. Create a free account (no credit card required)

### Step 2: Generate API Key
1. After logging in, go to **https://console.groq.com/keys**
2. Click **"Create API Key"**
3. Give it a name like "TalentTrack"
4. Copy the generated API key (starts with `gsk_...`)

⚠️ **IMPORTANT**: Save this key immediately - you won't be able to see it again!

---

## 📝 How to Add API Key to TalentTrack

### Method 1: Through Admin Settings (Recommended)
1. Login as admin (username: `admin`, password: `123456`)
2. Go to **Admin Dashboard** → **Settings**
3. Paste your Groq API key in the **"Groq API Key"** field
4. Click **"Save Settings"**
5. Done! ✅

### Method 2: Directly in Code
1. Open `app.py` file
2. Find line ~27: `GROQ_API_KEY = ""`
3. Replace with your key: `GROQ_API_KEY = "gsk_your_actual_key_here"`
4. Save the file
5. The server will auto-reload

---

## 🧪 Testing Your API Key

After adding your API key, test it:

```bash
python test_groq.py
```

You should see:
```
✅ Groq API is working!
✅ Resume extraction successful!
```

---

## 📊 Before vs After

### ❌ Without Valid API Key (Basic Extraction)
```
Skills: Python, Sql, Html, Css, Machine Learning
Experience: Fresher
Education: Not Specified
Summary: Professional candidate with relevant experience
```

### ✅ With Valid API Key (AI Extraction)
```
Skills: Python, TensorFlow, Scikit-learn, Pandas, NumPy, SQL, Git, Docker, AWS
Experience: 2 years
Education: Bachelor of Technology in Computer Science from ABC University (2021)
Certifications: AWS Certified Machine Learning Specialty
Projects: 
  - ML Recommendation System using TensorFlow
  - Data Pipeline with Apache Spark
Summary: Experienced Machine Learning Engineer with 2 years of hands-on experience 
         in developing and deploying ML models. Proficient in Python, TensorFlow, 
         and cloud technologies. Strong background in data engineering and MLOps.
```

---

## 🆓 Groq API Limits (Free Tier)

- **Rate Limit**: 30 requests per minute
- **Context Limit**: 8,192 tokens per request
- **Cost**: 100% FREE (as of 2026)
- **Models Available**: Llama 3.3 70B, Mixtral, and more

This is more than enough for a job application system!

---

## 🔧 Troubleshooting

### "Invalid API Key" Error
- Double-check you copied the entire key (starts with `gsk_`)
- Make sure there are no extra spaces
- Generate a new key if the old one expired

### "Rate Limit Exceeded"
- Groq free tier: 30 requests/minute
- Wait a minute and try again
- Resume uploads work one at a time, so this shouldn't be an issue

### Resume Still Shows Basic Info
1. Check if API key is saved in Admin Settings
2. Run `python test_groq.py` to verify connection
3. Check server logs for error messages
4. Try uploading a new resume (old ones keep their extraction)

---

## 📞 Need Help?

- **Groq Documentation**: https://console.groq.com/docs
- **Groq Discord**: https://discord.gg/groq
- **GitHub Issues**: Create an issue in your repository

---

## 🎯 Quick Start Command

```bash
# 1. Get API key from https://console.groq.com/keys
# 2. Start the application
python app.py

# 3. Go to http://127.0.0.1:5000
# 4. Login as admin and add API key in Settings
# 5. Upload a resume and see the magic! ✨
```

---

**Made with ❤️ using Groq AI**
