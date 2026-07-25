# TalentTrack - Installation Guide

## Prerequisites

### System Requirements
- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **RAM:** Minimum 2GB (4GB recommended)
- **Storage:** 500MB free space
- **Internet:** Required for AI API calls

### Required Accounts
- **Groq API Account:** Get free API key from [console.groq.com](https://console.groq.com/keys)

---

## Installation Steps

### 1. Clone or Download Project
```bash
# If using Git
git clone <repository-url>
cd talenttrack

# Or download and extract ZIP file
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** If you encounter any errors, try upgrading pip first:
```bash
pip install --upgrade pip
```

### 4. Verify Installation
```bash
python -c "import flask; print(flask.__version__)"
python -c "import fitz; print('PyMuPDF OK')"
python -c "import openai; print('OpenAI OK')"
```

### 5. Configure Groq API Key (Optional)
The application comes with a default API key, but you can set your own:

**Option A: Through Admin Settings (Recommended)**
1. Run the application
2. Login as admin (username: `admin`, password: `123456`)
3. Go to Settings (⚙️ in profile dropdown)
4. Update Groq API key
5. Save

**Option B: Edit app.py (Before First Run)**
```python
# In app.py, line 27
GROQ_API_KEY = "your-api-key-here"
```

### 6. Run Application
```bash
python app.py
```

You should see:
```
✅ Database loaded successfully!
 * Running on http://127.0.0.1:5000
```

### 7. Access Application
Open your browser and navigate to:
- **Local:** http://127.0.0.1:5000
- **Network:** http://YOUR_IP:5000

---

## First Time Setup

### 1. Landing Page
- View 8 feature cards
- Click "Login" or "Create Account"

### 2. Admin Login
**Default Credentials:**
- Username: `admin`
- Password: `123456`

**⚠️ IMPORTANT:** Change admin password in production!

### 3. Create User Account
Click "Create Account" and fill in:
- Username (min 3 characters)
- Email (valid format)
- Mobile (10 digits)
- Password (min 8 chars, uppercase, lowercase, number, special char)

### 4. Admin First Steps
1. Go to Settings and verify/update Groq API key
2. Create first job posting
3. Test with sample resume

### 5. User First Steps
1. Upload resume (PDF format)
2. Wait for AI analysis
3. Browse available jobs
4. Apply to jobs

---

## Troubleshooting

### Common Issues

#### 1. Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. Database Error
```
OperationalError: no such table: user
```
**Solution:** Delete `instance/talenttrack.db` and restart:
```bash
rm -rf instance/talenttrack.db  # macOS/Linux
del instance\talenttrack.db     # Windows
python app.py
```

#### 3. Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution:** Change port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

#### 4. PDF Extraction Error
```
Could not extract text from PDF
```
**Solution:** Ensure PDF is text-based (not scanned image). Use OCR-enabled PDFs.

#### 5. Groq API Error
```
AuthenticationError: Invalid API key
```
**Solution:** 
1. Get valid API key from [console.groq.com](https://console.groq.com/keys)
2. Update in Admin Settings
3. Test with sample resume

#### 6. File Upload Error
```
413 Request Entity Too Large
```
**Solution:** File size exceeds 16MB limit. Compress PDF or split into smaller files.

---

## Directory Structure After Installation

```
talenttrack/
│
├── venv/                    # Virtual environment (if created)
│
├── instance/
│   └── talenttrack.db       # SQLite database (auto-created)
│
├── uploads/
│   ├── company_logos/       # Company logos (auto-created)
│   └── *.pdf                # Uploaded resumes
│
├── static/                  # CSS, JS, images
├── templates/               # HTML templates
├── app.py                   # Main application
├── requirements.txt         # Dependencies
└── *.md                     # Documentation
```

---

## Testing the Installation

### 1. Test Admin Access
```
URL: http://127.0.0.1:5000/login
Username: admin
Password: 123456
Expected: Redirect to admin dashboard
```

### 2. Test User Registration
```
URL: http://127.0.0.1:5000/register
Fill form with valid data
Expected: Success message, redirect to login
```

### 3. Test Resume Upload
```
Login as user
Upload PDF resume
Expected: AI analysis completes, data extracted
```

### 4. Test Job Application
```
Admin creates job
User applies with resume
Expected: ATS score calculated, application submitted
```

### 5. Test Notifications
```
Admin shortlists/rejects application
User checks notifications
Expected: Notification appears with message
```

---

## Production Deployment

### 1. Security Checklist
- [ ] Change admin password
- [ ] Set strong SECRET_KEY in app.py
- [ ] Disable debug mode (`debug=False`)
- [ ] Use HTTPS
- [ ] Set up firewall rules
- [ ] Configure rate limiting
- [ ] Enable logging
- [ ] Set up backups

### 2. Use Production Server
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Database Migration
For production, consider PostgreSQL or MySQL:
```python
# In app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/talenttrack'
```

### 4. Environment Variables
Create `.env` file:
```
SECRET_KEY=your-secret-key-here
GROQ_API_KEY=your-groq-api-key
DATABASE_URL=your-database-url
```

Load in app.py:
```python
from dotenv import load_dotenv
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

### 5. Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Updating the Application

### 1. Pull Latest Changes
```bash
git pull origin main
```

### 2. Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### 3. Backup Database
```bash
cp instance/talenttrack.db instance/talenttrack.db.backup
```

### 4. Restart Application
```bash
# Stop current process (Ctrl+C)
python app.py
```

---

## Uninstallation

### 1. Deactivate Virtual Environment
```bash
deactivate
```

### 2. Remove Project Directory
```bash
rm -rf talenttrack  # macOS/Linux
rmdir /s talenttrack  # Windows
```

### 3. Remove Python Packages (Optional)
```bash
pip uninstall -r requirements.txt -y
```

---

## Getting Help

### Documentation
- `README.md` - Project overview
- `ARCHITECTURE.md` - System architecture
- `ATS_SYSTEM_GUIDE.md` - ATS scoring details
- `ADMIN_DASHBOARD_GUIDE.md` - Admin features
- `USER_DASHBOARD_UPDATE.md` - User features

### Support
- Check documentation files
- Review error messages carefully
- Verify all dependencies installed
- Ensure Python version is 3.8+
- Check Groq API key is valid

---

## Quick Reference

### Start Application
```bash
python app.py
```

### Access URLs
- Landing: http://127.0.0.1:5000
- Login: http://127.0.0.1:5000/login
- Register: http://127.0.0.1:5000/register
- Admin: http://127.0.0.1:5000/admin
- Settings: http://127.0.0.1:5000/admin/settings

### Default Credentials
- Username: `admin`
- Password: `123456`

### File Limits
- Resume: 16MB max, PDF only
- Logo: Any image format (PNG, JPG, GIF, SVG, WEBP)

### API Information
- Provider: Groq
- Model: Llama 3.3 70B Versatile
- Endpoint: https://api.groq.com/openai/v1

---

**Installation Complete!** 🎉

You're now ready to use TalentTrack. Start by logging in as admin and creating your first job posting!
