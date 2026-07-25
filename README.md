# 🎯 TalentTrack - AI-Powered Recruitment System

> Smart recruitment platform with AI-powered ATS scoring, resume analysis, and job matching using Groq AI (Llama 3.3 70B)

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Features

### 👤 For Job Seekers
- ✅ **Smart Resume Upload** - AI extracts skills, experience, education, certifications, and projects
- ✅ **One-Click Applications** - Apply to multiple companies with saved resumes
- ✅ **ATS Score Analysis** - Get detailed match scores for each application
- ✅ **Application Tracking** - Monitor status (Pending, Shortlisted, Rejected)
- ✅ **Real-time Notifications** - Get notified of application status updates

### 👔 For Recruiters (Admin)
- ✅ **Job Posting Management** - Create detailed job listings with company branding
- ✅ **AI-Powered Candidate Screening** - Automatic ATS scoring and matching
- ✅ **Application Management** - Review, shortlist, or reject candidates
- ✅ **Candidate Communication** - Send personalized messages to applicants
- ✅ **Analytics Dashboard** - View application statistics and trends

### 🤖 AI-Powered Features
- **Resume Parsing** - Extract comprehensive data from PDF resumes
- **ATS Scoring** - Intelligent matching between resume and job requirements
- **Skill Analysis** - Identify technical skills, certifications, and projects
- **Experience Evaluation** - Calculate years of experience and domain expertise
- **Powered by** - Groq AI with Llama 3.3 70B model

---

## 🚀 Live Demo

**🌐 Live Application:** 
https://talentrack10.onrender.com/

**Admin Login:**
- Username: `admin`
- Password: `123456`

**Test User Login:**
- Register your own account or use demo credentials

---

## 📸 Screenshots

*(Add screenshots of your application here)*

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0 (Web Framework)
- SQLAlchemy (ORM)
- SQLite (Database)

**AI/ML:**
- Groq AI API (Llama 3.3 70B)
- PyMuPDF (PDF text extraction)
- OpenAI SDK (for Groq integration)

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive Design
- Modern UI/UX

**Deployment:**
- Gunicorn (WSGI Server)
- Compatible with Render, Railway, PythonAnywhere

---

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Local Setup

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/talenttrack.git
cd talenttrack
```

2. **Create virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Get Groq API Key:**
- Visit https://console.groq.com/keys
- Sign up (free, no credit card)
- Create API key
- Copy the key

5. **Configure API Key:**

**Option A: Edit `app.py`**
```python
GROQ_API_KEY = "your_groq_api_key_here"
```

**Option B: Use Admin Settings**
- Start app, login as admin, go to Settings
- Add API key in the web interface

6. **Run the application:**
```bash
python app.py
```

7. **Access the app:**
```
http://127.0.0.1:5000
```

---

## 🌐 Deployment (FREE)

### Quick Deploy to Render.com (Recommended)

1. **Prepare for deployment:**
```bash
# Windows PowerShell
.\deploy.ps1

# Linux/Mac
chmod +x deploy.sh
./deploy.sh
```

2. **Push to GitHub:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/talenttrack.git
git branch -M main
git push -u origin main
```

3. **Deploy on Render:**
- Go to https://render.com
- Sign up with GitHub
- New Web Service → Connect repository
- Configure:
  - **Name:** `talenttrack`
  - **Build:** `pip install -r requirements.txt`
  - **Start:** `gunicorn app:app`
  - **Environment:** Add `GROQ_API_KEY`
- Click "Create Web Service"
- Wait 2-3 minutes
- **Done!** 🎉

**Your app will be live at:** `https://talenttrack.onrender.com`

### Other Deployment Options
- See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
  - Railway.app
  - PythonAnywhere
  - Fly.io
  - Vercel

---

## 📚 Usage Guide

### For Job Seekers

1. **Register Account**
   - Click "Register"
   - Fill in details
   - Create account

2. **Upload Resume**
   - Go to Dashboard
   - Upload PDF resume
   - AI automatically extracts all information

3. **Apply for Jobs**
   - Browse available jobs
   - Select your resume
   - Click "Apply Now"
   - Get instant ATS score

4. **Track Applications**
   - View all applications in dashboard
   - Check status updates
   - Read admin messages

### For Recruiters (Admin)

1. **Login as Admin**
   - Username: `admin`
   - Password: `123456`

2. **Create Job Posting**
   - Click "Create Job"
   - Add job details, requirements
   - Upload company logo
   - Publish

3. **Review Applications**
   - View all applicants
   - Check ATS scores
   - Review detailed analysis

4. **Manage Candidates**
   - Shortlist qualified candidates
   - Reject unmatched profiles
   - Send personalized messages

---

## 🔑 Environment Variables

Create a `.env` file or configure in hosting platform:

```env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your-secret-key-for-sessions
FLASK_ENV=production
```

---

## 📖 API Documentation

### Groq AI Integration

**Resume Extraction:**
```python
extract_resume_data_with_groq(text)
# Returns: JSON with skills, experience, education, certifications, projects, summary
```

**ATS Scoring:**
```python
calculate_ats_score_with_ai(resume_data, job_requirements)
# Returns: JSON with score, matched skills, missing skills, recommendations
```

---

## 🧪 Testing

**Test Groq API Connection:**
```bash
python test_groq.py
```

**Verify Setup:**
```bash
python verify_setup.py
```

---

## 🔐 Security

- Passwords hashed with Werkzeug
- Session management with Flask
- Input validation and sanitization
- Secure file uploads (PDF only)
- XSS and CSRF protection

**⚠️ Important:** Change default admin password in production!

---

## 📊 Database Schema

- **Users** - User accounts and authentication
- **Resumes** - Uploaded resumes with AI-extracted data
- **Jobs** - Job postings by recruiters
- **Applications** - Job applications with ATS scores
- **Settings** - System configuration

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed schema.

---

## 🐛 Troubleshooting

### Resume Upload Issues
- Ensure PDF is readable (not scanned image)
- Check Groq API key is valid
- Review server logs for errors

### Deployment Issues
- Verify `requirements.txt` is complete
- Check Python version matches `runtime.txt`
- Ensure `Procfile` is correct

### API Issues
- Verify Groq API key in settings
- Check API rate limits (30 req/min free tier)
- Run `python test_groq.py` to diagnose

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- **Groq AI** - For powerful and free AI inference
- **Flask** - For excellent web framework
- **PyMuPDF** - For PDF text extraction
- **Render** - For free hosting

---

## 📞 Support

Have questions or issues?

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/talenttrack/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/YOUR_USERNAME/talenttrack/discussions)

---

## 🗺️ Roadmap

- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Resume builder
- [ ] Interview scheduling
- [ ] Video interview integration
- [ ] Multi-language support
- [ ] Mobile app

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ using Flask and Groq AI**

🚀 **Deploy Now:** [Deployment Guide](DEPLOYMENT_GUIDE.md)
