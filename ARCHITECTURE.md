# TalentTrack - Complete System Architecture

## Table of Contents
1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Diagram](#architecture-diagram)
4. [Database Schema](#database-schema)
5. [Application Layers](#application-layers)
6. [Core Features](#core-features)
7. [API Integration](#api-integration)
8. [Security](#security)
9. [File Structure](#file-structure)
10. [Deployment](#deployment)

---

## System Overview

**TalentTrack** is an AI-powered Applicant Tracking System (ATS) built with Flask that automates resume analysis, candidate evaluation, and hiring workflows using Groq AI (Llama 3.3 70B model).

### Key Capabilities
- AI-powered resume parsing and data extraction
- Automated ATS scoring with detailed analysis
- Real-time notifications and status updates
- Interactive analytics dashboards
- Company logo management (online/offline)
- Vacancy limit enforcement
- Multi-resume support per user

---

## Technology Stack

### Backend
- **Framework:** Flask 3.x (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** Flask Sessions with Werkzeug Security
- **PDF Processing:** PyMuPDF (fitz)
- **AI/ML:** Groq API (Llama 3.3 70B Versatile)

### Frontend
- **HTML5** with Jinja2 templating
- **CSS3** with custom variables and gradients
- **JavaScript** (Vanilla JS)
- **Charts:** Chart.js for analytics visualization

### External APIs
- **Groq AI API:** Resume parsing and ATS scoring
- **OpenAI SDK:** Client for Groq API communication

---

## Architecture Diagram

\\\
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Hero    │  │  Login   │  │Dashboard │  │  Admin   │   │
│  │  Page    │  │ Register │  │  (User)  │  │Dashboard │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER (Flask)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Route Handlers & Controllers            │   │
│  │  • Authentication  • Job Management  • Applications  │   │
│  │  • Resume Upload   • Notifications   • Settings     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                 Business Logic Layer                 │   │
│  │  • Resume Parser  • ATS Calculator  • Validators    │   │
│  │  • File Handler   • Notification Manager            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   SQLite DB  │  │  File System │  │  Groq API    │     │
│  │  (ORM Models)│  │   (Uploads)  │  │  (External)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
\\\

---

## Database Schema

### Entity Relationship Diagram

\\\
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    User     │         │   Resume    │         │     Job     │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ id (PK)     │────┐    │ id (PK)     │    ┌────│ id (PK)     │
│ username    │    │    │ user_id(FK) │    │    │ company_name│
│ email       │    └───→│ filename    │    │    │ company_logo│
│ mobile      │         │ file_path   │    │    │ position    │
│ password    │         │ full_text   │    │    │ req_skills  │
│ is_admin    │         │ extracted   │    │    │ experience  │
└─────────────┘         │ uploaded_at │    │    │ education   │
                        └─────────────┘    │    │ vacancies   │
                                           │    │ description │
                                           │    │ created_by  │
                                           │    │ created_at  │
                                           │    └─────────────┘
                                           │
                        ┌─────────────┐    │
                        │ Application │    │
                        ├─────────────┤    │
                        │ id (PK)     │    │
                        │ user_id(FK) │────┘
                        │ job_id (FK) │────┘
                        │ resume_id   │────┘
                        │ ats_score   │
                        │ ats_analysis│
                        │ applied_at  │
                        │ status      │
                        │ admin_msg   │
                        │ is_read     │
                        └─────────────┘

┌─────────────┐
│  Settings   │
├─────────────┤
│ id (PK)     │
│ key         │
│ value       │
│ updated_at  │
└─────────────┘
\\\

### Table Descriptions

#### **User Table**
Stores user accounts (both regular users and admins)
- Primary authentication entity
- One-to-many with Resume and Application
- Password hashed with Werkzeug

#### **Resume Table**
Stores uploaded resumes and extracted data
- Links to User (many-to-one)
- Stores PDF file path and extracted text
- Contains AI-extracted JSON data (skills, experience, etc.)

#### **Job Table**
Job postings created by admin
- Company information and requirements
- Vacancy count for limit enforcement
- Links to User (created_by)

#### **Application Table**
Job applications submitted by users
- Links User, Job, and Resume
- Stores ATS score and analysis
- Tracks status (pending/shortlisted/rejected)
- Notification system (is_read flag)

#### **Settings Table**
System configuration (API keys, etc.)
- Key-value storage
- Currently stores Groq API key
- Extensible for future settings

---

## Application Layers

### 1. Presentation Layer (Templates)

\\\
templates/
├── index.html              # Hero landing page (8 feature cards)
├── login.html              # User authentication
├── register.html           # User registration
├── dashboard.html          # User dashboard (6 graphs, expandable jobs)
├── admin.html              # Admin dashboard (6 system-wide graphs)
├── admin_settings.html     # Admin settings (API key management)
├── create_job.html         # Job posting form (logo upload)
├── job_applications.html   # Application management (vacancy limits)
├── view_application.html   # Detailed ATS analysis view
└── notifications.html      # User notifications page
\\\

### 2. Business Logic Layer (app.py)

#### Core Functions

**Authentication & Authorization**
\\\python
- validate_password()      # Password strength validation
- validate_email()         # Email format validation
- validate_mobile()        # Mobile number validation
- login_required()         # Decorator for protected routes
- admin_required()         # Decorator for admin-only routes
\\\

**Resume Processing**
\\\python
- extract_text_from_pdf()           # PDF text extraction
- extract_resume_data_with_groq()   # AI data extraction
- clean_text()                      # Text preprocessing
\\\

**ATS Scoring**
\\\python
- calculate_ats_score_with_ai()     # AI-powered ATS calculation
- get_groq_api_key()                # Dynamic API key retrieval
\\\

**File Management**
\\\python
- allowed_file()                    # File type validation
- secure_filename()                 # Filename sanitization
- uploaded_file()                   # File serving route
\\\

**Jinja Filters**
\\\python
- from_json()                       # JSON parsing filter
- logo_url()                        # Logo path resolver
\\\

### 3. Data Access Layer (SQLAlchemy ORM)

All database operations use SQLAlchemy models with relationships:
- Automatic foreign key management
- Cascade delete operations
- Query optimization with joins

---

## Core Features

### 1. AI-Powered Resume Analysis

**Flow:**
\\\
User uploads PDF → PyMuPDF extracts text → Groq AI analyzes →
Extracts: Skills, Experience, Education, Certifications, Projects, Summary
→ Stores as JSON in database
\\\

**AI Prompt Engineering:**
- Structured JSON output format
- Comprehensive data extraction
- Error handling and fallbacks

### 2. ATS Scoring System

**Scoring Algorithm:**
\\\
Skills Match (50%):     Compare candidate vs job requirements
Experience Match (20%): Years of experience alignment
Education Match (15%):  Degree and field relevance
Overall Fit (15%):      Certifications, projects, profile
────────────────────
Total ATS Score (0-100%)
\\\

**Output:**
- Numerical score (0-100)
- Matched skills list
- Missing skills list
- Strengths and recommendations
- Detailed summary

### 3. Vacancy Management

**Business Rules:**
- Users can apply unlimited times (more applicants = better pool)
- Shortlisted count ≤ Vacancy count (enforced)
- Backend validation prevents over-shortlisting
- Visual indicators show available spots
- Buttons disabled when vacancy full

**Implementation:**
\\\python
current_shortlisted = Application.query.filter_by(
    job_id=job.id, status='shortlisted'
).count()

if current_shortlisted >= job.vacancies:
    flash('Cannot shortlist more candidates!')
    return redirect(...)
\\\

### 4. Notification System

**Architecture:**
\\\
Admin updates status → Application.is_read = False →
Badge appears on user profile → User clicks notifications →
Sees all updates → Marks as read → Badge disappears
\\\

**Features:**
- Real-time unread count
- Persistent storage
- Custom admin messages
- Status-based filtering

### 5. Analytics Dashboards

**User Dashboard (6 Graphs):**
1. Application Status Distribution (Pie)
2. ATS Score Range (Bar)
3. Companies Applied (Horizontal Bar)
4. Resume Performance (Line)
5. Application Timeline (Line)
6. Success Metrics (Doughnut)

**Admin Dashboard (6 Graphs):**
1. Application Status Overview (Pie)
2. ATS Score Distribution (Bar)
3. Top Jobs by Applications (Horizontal Bar)
4. Application Trends (Line)
5. Top Skills Across Resumes (Bar)
6. User Engagement Rate (Doughnut)

**Technology:** Chart.js with dynamic data from Flask

### 6. Company Logo Management

**Dual Support:**
- **Online URLs:** Direct image links (http/https)
- **Local Files:** Upload to uploads/company_logos/

**Implementation:**
\\\python
@app.template_filter('logo_url')
def logo_url_filter(logo_path):
    if logo_path.startswith('http'):
        return logo_path  # External URL
    return url_for('uploaded_file', filename=logo_path)  # Local file
\\\

**Features:**
- Live preview before upload
- Drag-and-drop interface
- Multiple format support (PNG, JPG, GIF, SVG, WEBP)
- Secure filename handling

### 7. Admin Settings

**Configurable Settings:**
- Groq API key management
- Database-driven configuration
- Real-time updates (no restart needed)
- Masked display for security

**Access Control:**
- Admin-only access
- Profile dropdown integration
- Comprehensive documentation

---

## API Integration

### Groq AI API

**Endpoint:** https://api.groq.com/openai/v1

**Model:** Llama 3.3 70B Versatile

**Usage:**
1. **Resume Parsing**
   - Input: Raw PDF text
   - Output: Structured JSON (skills, experience, etc.)
   - Temperature: 0.3 (deterministic)

2. **ATS Scoring**
   - Input: Resume data + Job requirements
   - Output: Score + detailed analysis
   - Temperature: 0.3 (consistent scoring)

**Error Handling:**
- Try-catch blocks
- Fallback responses
- JSON validation
- API key validation

**Configuration:**
\\\python
client = OpenAI(
    api_key=get_groq_api_key(),  # Dynamic from database
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,
    response_format={"type": "json_object"}
)
\\\

---

## Security

### Authentication
- **Password Hashing:** Werkzeug PBKDF2 SHA-256
- **Session Management:** Flask secure sessions
- **CSRF Protection:** Built-in Flask protection

### Authorization
- **Role-Based Access:** Admin vs User roles
- **Route Protection:** Decorators (@login_required, @admin_required)
- **Resource Ownership:** Users can only access their own data

### File Security
- **Upload Validation:** File type and size checks
- **Secure Filenames:** Werkzeug secure_filename()
- **Path Traversal Prevention:** Restricted upload directory
- **File Size Limit:** 16MB maximum

### Data Security
- **SQL Injection:** SQLAlchemy ORM prevents injection
- **XSS Protection:** Jinja2 auto-escaping
- **API Key Storage:** Database storage (not hardcoded)
- **Sensitive Data:** Masked display (API keys)

### Best Practices
- Input validation on all forms
- Error messages don't leak sensitive info
- Admin credentials not displayed on login page
- Logout clears all session data

---

## File Structure

\\\
talenttrack/
│
├── app.py                          # Main application file (1100+ lines)
│
├── instance/
│   └── talenttrack.db              # SQLite database
│
├── static/
│   ├── style.css                   # Main stylesheet (2800+ lines)
│   ├── script.js                   # Common JavaScript
│   ├── dashboard.js                # User dashboard charts
│   ├── admin-dashboard.js          # Admin dashboard charts
│   ├── logo.svg                    # Main logo (200x60)
│   └── logo-icon.svg               # Icon logo (40x40)
│
├── templates/
│   ├── index.html                  # Landing page
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── dashboard.html              # User dashboard
│   ├── admin.html                  # Admin dashboard
│   ├── admin_settings.html         # Settings page
│   ├── create_job.html             # Job creation form
│   ├── job_applications.html       # Application management
│   ├── view_application.html       # Application details
│   └── notifications.html          # Notifications page
│
├── uploads/
│   ├── company_logos/              # Company logo uploads
│   └── *.pdf                       # Resume uploads
│
├── requirements.txt                # Python dependencies
│
└── Documentation/
    ├── README.md
    ├── ATS_SYSTEM_GUIDE.md
    ├── ADMIN_DASHBOARD_GUIDE.md
    ├── USER_DASHBOARD_UPDATE.md
    ├── NOTIFICATION_SYSTEM_GUIDE.md
    ├── LOGO_IMPLEMENTATION.md
    ├── VACANCY_LIMIT_FEATURE.md
    ├── ADMIN_SETTINGS_FEATURE.md
    └── COMPLETE_SYSTEM_ARCHITECTURE.md
\\\

---

## Deployment

### Requirements
\\\
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
PyMuPDF==1.23.8
openai==1.12.0
\\\

### Environment Setup
\\\ash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access application
http://localhost:5000
\\\

### Configuration
- **Debug Mode:** Enabled (development)
- **Host:** 0.0.0.0 (all interfaces)
- **Port:** 5000
- **Database:** SQLite (auto-created)
- **Upload Folder:** ./uploads
- **Max File Size:** 16MB

### Production Considerations
1. **Disable Debug Mode**
2. **Use Production WSGI Server** (Gunicorn, uWSGI)
3. **Configure HTTPS**
4. **Use PostgreSQL/MySQL** instead of SQLite
5. **Set Strong SECRET_KEY**
6. **Enable Rate Limiting**
7. **Configure Logging**
8. **Set up Backup System**
9. **Use Environment Variables** for sensitive data
10. **Implement Caching** (Redis)

---

## Key Design Decisions

### 1. Why SQLite?
- **Pros:** Zero configuration, portable, sufficient for small-medium scale
- **Cons:** Not suitable for high concurrency
- **Migration Path:** Easy to switch to PostgreSQL/MySQL

### 2. Why Groq AI?
- **Fast inference:** Llama 3.3 70B with high speed
- **Cost-effective:** Competitive pricing
- **JSON mode:** Structured output support
- **Quality:** Excellent for resume parsing

### 3. Why Flask?
- **Lightweight:** Minimal overhead
- **Flexible:** Easy to customize
- **Python Ecosystem:** Rich libraries
- **Learning Curve:** Easy to understand

### 4. Why Chart.js?
- **Free & Open Source**
- **Responsive:** Works on all devices
- **Easy Integration:** Simple JavaScript API
- **Beautiful:** Professional-looking charts

### 5. Why Session-Based Auth?
- **Simple:** No token management
- **Secure:** Built-in Flask support
- **Sufficient:** For this application scale
- **Stateful:** Easier to manage

---

## Performance Optimizations

### Database
- Indexed foreign keys
- Efficient queries with joins
- Lazy loading for relationships
- Query result caching (in memory)

### File Handling
- Secure filename generation
- Organized folder structure
- File size limits
- Type validation

### Frontend
- CSS minification (production)
- Image optimization
- Lazy loading for charts
- Responsive images

### API Calls
- Error handling and retries
- Timeout configuration
- Response validation
- Fallback mechanisms

---

## Future Enhancements

### Planned Features
1. **Email Notifications:** SMTP integration
2. **Advanced Search:** Full-text search for resumes
3. **Bulk Operations:** Batch shortlist/reject
4. **Interview Scheduling:** Calendar integration
5. **Resume Comparison:** Side-by-side comparison
6. **Export Reports:** PDF/Excel export
7. **API Endpoints:** RESTful API for integrations
8. **Multi-language:** i18n support
9. **Dark Mode:** Theme switching
10. **Mobile App:** React Native/Flutter

### Technical Improvements
1. **Caching Layer:** Redis for performance
2. **Message Queue:** Celery for async tasks
3. **Containerization:** Docker deployment
4. **CI/CD Pipeline:** Automated testing and deployment
5. **Monitoring:** Application performance monitoring
6. **Logging:** Centralized logging system
7. **Testing:** Unit and integration tests
8. **Documentation:** API documentation (Swagger)

---

## Conclusion

TalentTrack is a modern, AI-powered ATS system that streamlines the hiring process through intelligent automation. Built with Flask and powered by Groq AI, it provides a comprehensive solution for resume management, candidate evaluation, and hiring workflows.

**Key Strengths:**
- ✅ AI-powered resume analysis
- ✅ Automated ATS scoring
- ✅ Real-time notifications
- ✅ Interactive analytics
- ✅ Vacancy management
- ✅ Configurable settings
- ✅ Secure and scalable

**Production Ready:** With proper configuration and deployment, TalentTrack can handle real-world hiring workflows for small to medium-sized organizations.

---

**Version:** 1.0.0  
**Last Updated:** May 14, 2026  
**Author:** TalentTrack Development Team  
**License:** Proprietary
