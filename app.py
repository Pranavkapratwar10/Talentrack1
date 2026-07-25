from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import re
import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from openai import OpenAI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///talenttrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Groq API Configuration
# IMPORTANT: Get your FREE API key from https://console.groq.com/keys
# Replace the value below or update it from Admin Settings page
GROQ_API_KEY = "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"

# Helper function to get Groq API key from settings
def get_groq_api_key():
    """Get Groq API key from database settings or fallback to default"""
    try:
        setting = Settings.query.filter_by(key='groq_api_key').first()
        if setting and setting.value:
            return setting.value
        return GROQ_API_KEY
    except:
        return GROQ_API_KEY

# Custom Jinja filter to parse JSON
@app.template_filter('from_json')
def from_json_filter(value):
    try:
        # Clean the value first
        cleaned = value.strip()
        
        # Remove markdown code blocks
        if cleaned.startswith('```'):
            lines = cleaned.split('\n')
            cleaned = '\n'.join([line for line in lines if not line.strip().startswith('```')])
            cleaned = cleaned.strip()
        
        # Remove "json" text if present
        if cleaned.lower().startswith('json'):
            cleaned = cleaned[4:].strip()
        
        # Parse JSON
        return json.loads(cleaned)
    except Exception as e:
        print(f"JSON parsing error in filter: {e}")
        return None

# Custom Jinja filter to handle company logo paths
@app.template_filter('logo_url')
def logo_url_filter(logo_path):
    """Convert logo path to proper URL - handles both external URLs and local files"""
    if not logo_path:
        return None
    
    # Check if it's an external URL (starts with http:// or https://)
    if logo_path.startswith('http://') or logo_path.startswith('https://'):
        return logo_path
    
    # It's a local file - construct URL using the uploads route
    # logo_path should be like "company_logos/filename.png"
    return url_for('uploaded_file', filename=logo_path)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    full_text = db.Column(db.Text, nullable=False)
    extracted_data = db.Column(db.Text)  # JSON string with skills, experience, education, etc.
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Resume {self.original_filename}>'

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_logo = db.Column(db.String(200))
    position = db.Column(db.String(100), nullable=False)
    required_skills = db.Column(db.Text, nullable=False)
    experience_required = db.Column(db.String(50))
    education_required = db.Column(db.String(200))
    vacancies = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Job {self.company_name} - {self.position}>'

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    ats_score = db.Column(db.Float, nullable=False)
    ats_analysis = db.Column(db.Text)  # Detailed analysis from Groq AI
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, shortlisted, rejected
    status_updated_at = db.Column(db.DateTime)
    admin_message = db.Column(db.Text)  # Message from admin to candidate
    is_read = db.Column(db.Boolean, default=False)  # Whether user has seen the status update
    resume = db.relationship('Resume', backref='applications')

    def __repr__(self):
        return f'<Application User:{self.user_id} Job:{self.job_id}>'

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Settings {self.key}>'

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF"""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"
        doc.close()
    except Exception as e:
        print(f"PDF Extraction Error: {e}")
    return text.strip()

def clean_text(text):
    """Clean extracted text"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_resume_data_with_groq(text):
    """Extract comprehensive data from resume using Groq AI with robust error handling"""
    try:
        # Validate text length
        if not text or len(text.strip()) < 50:
            print("⚠️ Resume text too short or empty")
            return create_fallback_resume_data(text)
        
        print(f"📄 Processing resume with {len(text)} characters")
        
        # Truncate text if too long (API limit - Groq can handle up to ~30k tokens)
        max_chars = 20000
        if len(text) > max_chars:
            print(f"⚠️ Truncating resume text from {len(text)} to {max_chars} characters")
            text = text[:max_chars] + "..."
        
        api_key = get_groq_api_key()
        print(f"🔑 Using API key: {api_key[:20]}...")
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=30.0  # 30 second timeout
        )
        
        prompt = f"""You are an expert ATS Resume Parser AI. Extract ALL relevant information from this resume in detail.

CRITICAL INSTRUCTIONS:
1. Return ONLY a valid JSON object
2. NO markdown, NO code blocks, NO extra text
3. Extract COMPLETE information, not just keywords
4. Be thorough and detailed

Return this EXACT JSON structure:
{{
    "skills": ["List ALL technical skills, tools, languages, frameworks found"],
    "experience": "Total years (e.g., '2 years', '5+ years') or 'Fresher' if no experience",
    "education": ["List ALL degrees with college/university names and years if available"],
    "certifications": ["List ALL certifications mentioned"],
    "projects": ["List ALL projects with brief descriptions"],
    "summary": "Write a comprehensive 3-4 sentence professional summary based on the resume content"
}}

IMPORTANT EXTRACTION RULES:
- Skills: Extract ALL programming languages, frameworks, databases, tools, cloud platforms, technologies
- Experience: Calculate total years or mention 'Fresher'. Include company names in summary if present.
- Education: Include degree name, institution, field of study, and year if mentioned
- Certifications: List any courses, certifications, or professional qualifications
- Projects: Include project names and technologies used
- Summary: Create a detailed professional summary highlighting key strengths and experience

Resume Text:
{text}

Return ONLY the JSON object."""

        print("🤖 Calling Groq API...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # Lower temperature for more consistent extraction
            response_format={"type": "json_object"},
            max_tokens=2000  # Increased for more detailed responses
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Groq API response received ({len(result)} chars)")
        
        # Clean any markdown code blocks if present
        if result.startswith('```'):
            lines = result.split('\n')
            result = '\n'.join([line for line in lines if not line.strip().startswith('```')])
            result = result.strip()
        
        # Remove "json" text if present
        if result.lower().startswith('json'):
            result = result[4:].strip()
        
        # Validate it's proper JSON
        try:
            parsed = json.loads(result)
            print(f"✅ JSON parsed successfully")
            
            # Ensure all required fields exist
            required_fields = {
                'skills': ['General Skills'],
                'experience': 'Fresher',
                'education': ['Not Specified'],
                'certifications': [],
                'projects': [],
                'summary': 'Professional seeking opportunities'
            }
            
            for field, default in required_fields.items():
                if field not in parsed or not parsed[field]:
                    print(f"⚠️ Missing field '{field}', using default")
                    parsed[field] = default
            
            print(f"✅ Extracted {len(parsed.get('skills', []))} skills, {len(parsed.get('projects', []))} projects, {len(parsed.get('certifications', []))} certifications")
            
            # Return validated JSON string
            return json.dumps(parsed)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON validation failed: {e}")
            print(f"Raw result: {result[:500]}...")
            # Try to fix common JSON issues
            return create_fallback_resume_data(text)
            
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        import traceback
        traceback.print_exc()
        # Return fallback data instead of None
        return create_fallback_resume_data(text)

def create_fallback_resume_data(text):
    """Create fallback resume data using basic text parsing with improved extraction"""
    try:
        print("⚠️ Using fallback extraction method")
        
        # Basic skill extraction using comprehensive keywords
        skills = []
        skill_keywords = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust',
            # Web Technologies
            'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'html', 'css', 'bootstrap',
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis', 'elasticsearch',
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
            # Data & AI
            'machine learning', 'deep learning', 'ai', 'data science', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn',
            # Tools & Others
            'git', 'github', 'jira', 'agile', 'scrum', 'rest api', 'graphql', 'microservices'
        ]
        
        text_lower = text.lower()
        for skill in skill_keywords:
            if skill in text_lower:
                skills.append(skill.title())
        
        # Remove duplicates and limit
        skills = list(set(skills))[:20]
        
        if not skills:
            skills = ['General Skills']
        
        print(f"📊 Extracted {len(skills)} skills from fallback")
        
        # Enhanced experience detection
        experience = "Fresher"
        
        # Look for various experience patterns
        import re
        experience_patterns = [
            r'(\d+)\s*(?:\+)?\s*years?\s+(?:of\s+)?experience',
            r'experience\s*:\s*(\d+)\s*(?:\+)?\s*years?',
            r'(\d+)\s*(?:\+)?\s*yrs?\s+exp',
            r'total\s+experience\s*:\s*(\d+)',
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text_lower)
            if match:
                years = match.group(1)
                experience = f"{years} years" if int(years) > 1 else f"{years} year"
                print(f"💼 Found experience: {experience}")
                break
        
        # Enhanced education detection
        education = []
        edu_patterns = {
            'Bachelor': r'b\.?tech|b\.?e\.?|bachelor|b\.?sc|bca',
            'Master': r'm\.?tech|m\.?e\.?|master|m\.?sc|mca|mba',
            'PhD': r'ph\.?d|doctorate',
            'Diploma': r'diploma',
        }
        
        for degree, pattern in edu_patterns.items():
            if re.search(pattern, text_lower):
                education.append(degree)
        
        # Try to find university/college names
        college_match = re.search(r'(?:university|college|institute)\s+(?:of\s+)?([A-Z][a-zA-Z\s]+)', text)
        if college_match:
            education.append(f"from {college_match.group(1).strip()}")
        
        if not education:
            education = ['Not Specified']
        
        print(f"🎓 Extracted education: {education}")
        
        # Enhanced project detection
        projects = []
        project_keywords = ['project', 'developed', 'built', 'created', 'implemented']
        
        # Split text into sentences
        sentences = re.split(r'[.!\n]', text)
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in project_keywords):
                # Extract meaningful project descriptions
                if len(sentence.strip()) > 20 and len(sentence.strip()) < 200:
                    projects.append(sentence.strip())
                    if len(projects) >= 5:  # Limit to 5 projects
                        break
        
        print(f"📁 Extracted {len(projects)} projects")
        
        # Enhanced certification detection
        certifications = []
        cert_keywords = [
            'certified', 'certification', 'certificate', 'aws certified', 'azure certified',
            'google certified', 'oracle certified', 'cisco', 'comptia', 'pmp'
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in cert_keywords):
                if len(sentence.strip()) > 10 and len(sentence.strip()) < 150:
                    certifications.append(sentence.strip())
                    if len(certifications) >= 5:
                        break
        
        print(f"🏆 Extracted {len(certifications)} certifications")
        
        # Create summary based on extracted data
        summary = f"Professional candidate with {experience.lower()} in the field. "
        if skills and len(skills) > 1:
            summary += f"Proficient in {', '.join(skills[:5])}. "
        if education and education != ['Not Specified']:
            summary += f"Educational background includes {', '.join(education[:2])}."
        
        fallback_data = {
            'skills': skills,
            'experience': experience,
            'education': education,
            'certifications': certifications,
            'projects': projects,
            'summary': summary.strip()
        }
        
        print(f"✅ Fallback data created successfully")
        return json.dumps(fallback_data)
        
    except Exception as e:
        print(f"❌ Fallback data creation error: {e}")
        # Absolute fallback
        return json.dumps({
            'skills': ['General Skills'],
            'experience': 'Fresher',
            'education': ['Not Specified'],
            'certifications': [],
            'projects': [],
            'summary': 'Professional seeking opportunities'
        })

def calculate_ats_score_with_ai(resume_data, job_requirements):
    """Calculate accurate ATS score using Groq AI by comparing resume with job requirements"""
    try:
        client = OpenAI(
            api_key=get_groq_api_key(),
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Parse resume data if it's a string
        if isinstance(resume_data, str):
            try:
                resume_json = json.loads(resume_data)
            except:
                resume_json = {"raw": resume_data}
        else:
            resume_json = resume_data
        
        prompt = f"""You are an expert ATS (Applicant Tracking System) AI. Calculate an ACCURATE ATS score by comparing the candidate's resume with the job requirements.

JOB REQUIREMENTS:
Position: {job_requirements['position']}
Required Skills: {job_requirements['required_skills']}
Experience Required: {job_requirements.get('experience_required', 'Not specified')}
Education Required: {job_requirements.get('education_required', 'Not specified')}
Description: {job_requirements.get('description', 'Not specified')}

CANDIDATE'S RESUME:
Skills: {', '.join(resume_json.get('skills', [])) if isinstance(resume_json.get('skills'), list) else resume_json.get('skills', 'Not specified')}
Experience: {resume_json.get('experience', 'Not specified')}
Education: {', '.join(resume_json.get('education', [])) if isinstance(resume_json.get('education'), list) else resume_json.get('education', 'Not specified')}
Certifications: {', '.join(resume_json.get('certifications', [])) if isinstance(resume_json.get('certifications'), list) else resume_json.get('certifications', 'Not specified')}
Projects: {', '.join(resume_json.get('projects', [])) if isinstance(resume_json.get('projects'), list) else resume_json.get('projects', 'Not specified')}

SCORING INSTRUCTIONS:
1. Skills Match (50% weight):
   - Compare candidate's skills with required skills
   - Count exact matches and similar skills
   - If candidate has 70%+ of required skills = 90-100%
   - If candidate has 50-69% of required skills = 70-89%
   - If candidate has 30-49% of required skills = 50-69%
   - Below 30% = 0-49%

2. Experience Match (20% weight):
   - If experience matches or exceeds requirement = 100%
   - If fresher but job allows fresher = 80%
   - If fresher but job needs experience = 40%

3. Education Match (15% weight):
   - If education matches requirement = 100%
   - If related field = 80%
   - If different but relevant = 60%

4. Overall Fit (15% weight):
   - Consider certifications, projects, and overall profile

IMPORTANT: Be GENEROUS and ACCURATE. If candidate has relevant skills, give appropriate credit.

Return ONLY this JSON format (no markdown, no extra text):
{{
    "ats_score": 85,
    "skills_match": 90,
    "experience_match": 80,
    "education_match": 100,
    "overall_fit": 85,
    "matched_skills": ["Python", "TensorFlow"],
    "missing_skills": ["Docker"],
    "strengths": ["Strong ML background", "Multiple projects"],
    "recommendations": ["Gain production experience"],
    "summary": "Excellent candidate with strong technical skills."
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = response.choices[0].message.content.strip()
        
        # Validate JSON
        try:
            json.loads(result)
            return result
        except:
            # If JSON parsing fails, create a fallback response
            print(f"JSON parsing failed, creating fallback response")
            return json.dumps({
                "ats_score": 50,
                "skills_match": 50,
                "experience_match": 50,
                "education_match": 50,
                "overall_fit": 50,
                "matched_skills": ["Various skills"],
                "missing_skills": ["Some skills"],
                "strengths": ["Good potential"],
                "recommendations": ["Continue learning"],
                "summary": "Candidate shows potential for the role."
            })
            
    except Exception as e:
        print(f"Groq API Error: {e}")
        import traceback
        traceback.print_exc()
        return None

# Create database tables (persistent - only creates if not exists)
with app.app_context():
    db.create_all()  # Create tables only if they don't exist
    
    # Create admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin_user = User(
            username='admin',
            email='admin@talenttrack.com',
            mobile='0000000000',
            password=generate_password_hash('123456'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created successfully!")
    else:
        print("✅ Database loaded successfully!")
    
    # Initialize default Groq API key if not exists
    groq_setting = Settings.query.filter_by(key='groq_api_key').first()
    if not groq_setting:
        groq_setting = Settings(
            key='groq_api_key',
            value=GROQ_API_KEY
        )
        db.session.add(groq_setting)
        db.session.commit()
        print("✅ Default Groq API key initialized!")

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Validation functions
def validate_password(password):
    """Password must be at least 8 characters with uppercase, lowercase, number and special char"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, "Valid"

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_mobile(mobile):
    """Validate mobile number (10 digits)"""
    pattern = r'^\d{10}$'
    return re.match(pattern, mobile) is not None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters long', 'error')
            return redirect(url_for('register'))

        if not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('register'))

        if not validate_mobile(mobile):
            flash('Mobile number must be exactly 10 digits', 'error')
            return redirect(url_for('register'))

        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message, 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            mobile=mobile,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin

            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    resumes = Resume.query.filter_by(user_id=user.id).order_by(Resume.uploaded_at.desc()).all()
    user_applications = Application.query.filter_by(user_id=user.id).order_by(Application.applied_at.desc()).all()
    
    # Get list of companies user has already applied to
    applied_companies = []
    for app in user_applications:
        applied_companies.append(app.job.company_name)
    
    # Get unread notifications count (for badge)
    unread_count = Application.query.filter_by(user_id=user.id, is_read=False).filter(
        Application.status.in_(['shortlisted', 'rejected'])
    ).count()
    
    # Convert resumes to JSON-serializable format for JavaScript
    resumes_data = []
    for resume in resumes:
        resumes_data.append({
            'id': resume.id,
            'original_filename': resume.original_filename,
            'uploaded_at': resume.uploaded_at.isoformat(),
            'extracted_data': resume.extracted_data
        })
    
    # Convert applications to JSON-serializable format for JavaScript
    applications_data = []
    for app in user_applications:
        applications_data.append({
            'id': app.id,
            'job_id': app.job_id,
            'ats_score': app.ats_score,
            'status': app.status,
            'applied_at': app.applied_at.isoformat(),
            'is_read': app.is_read,
            'job': {
                'id': app.job.id,
                'company_name': app.job.company_name,
                'company_logo': app.job.company_logo,
                'position': app.job.position
            }
        })
    
    return render_template('dashboard.html', user=user, jobs=jobs, resumes=resumes, 
                         applied_companies=applied_companies, applications=user_applications,
                         unread_count=unread_count,
                         resumes_data=resumes_data, applications_data=applications_data)

@app.route('/upload_resume', methods=['POST'])
@login_required
def upload_resume():
    if 'resume' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    
    file = request.files['resume']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"user_{session['user_id']}_{timestamp}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
            
            # Extract text from PDF
            text = extract_text_from_pdf(filepath)
            
            if len(text) < 50:
                flash('Could not extract sufficient text from PDF. Please ensure it contains readable text.', 'error')
                os.remove(filepath)
                return redirect(url_for('dashboard'))
            
            # Extract comprehensive data using Groq AI (now has fallback)
            extracted_data = extract_resume_data_with_groq(text)
            
            # Check if we're using fallback (indicates Groq API issue)
            using_fallback = False
            
            # Validate the extracted data
            if not extracted_data:
                print('⚠️ No data extracted, using fallback')
                flash('Error processing resume. Using basic extraction.', 'warning')
                extracted_data = create_fallback_resume_data(text)
                using_fallback = True
            
            # Validate JSON format
            try:
                parsed_data = json.loads(extracted_data)
                # Ensure it has required structure
                if 'skills' not in parsed_data or 'experience' not in parsed_data:
                    raise ValueError("Missing required fields")
                
                # Check if this looks like fallback data (limited skills)
                if len(parsed_data.get('skills', [])) <= 10 and parsed_data.get('summary', '').startswith('Professional candidate'):
                    using_fallback = True
                    
            except Exception as e:
                print(f"Data validation error: {e}")
                flash('Resume uploaded but data extraction was limited. You can still apply for jobs.', 'warning')
                extracted_data = create_fallback_resume_data(text)
                using_fallback = True
            
            # Create resume record
            resume = Resume(
                user_id=session['user_id'],
                filename=filename,
                original_filename=original_filename,
                file_path=filepath,
                full_text=text,
                extracted_data=extracted_data
            )
            db.session.add(resume)
            db.session.commit()
            
            # Provide appropriate success message
            if using_fallback:
                flash(f'Resume "{original_filename}" uploaded with basic extraction. For detailed AI analysis, please add a valid Groq API key in Admin Settings.', 'warning')
            else:
                flash(f'Resume "{original_filename}" uploaded and analyzed successfully with AI!', 'success')
            
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            print(f"Error during resume upload: {e}")
            import traceback
            traceback.print_exc()
            
            # Clean up file if it exists
            if os.path.exists(filepath):
                os.remove(filepath)
            
            flash('An error occurred while processing your resume. Please try again.', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Invalid file type. Only PDF files are allowed.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/delete_resume/<int:resume_id>', methods=['POST'])
@login_required
def delete_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if resume belongs to current user
    if resume.user_id != session['user_id']:
        flash('Unauthorized action', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if resume is used in any applications
    if resume.applications:
        flash('Cannot delete resume that has been used in applications', 'error')
        return redirect(url_for('dashboard'))
    
    # Delete file
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    # Delete record
    db.session.delete(resume)
    db.session.commit()
    
    flash('Resume deleted successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/apply_job/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    user = User.query.get(session['user_id'])
    job = Job.query.get_or_404(job_id)
    resume_id = request.form.get('resume_id')
    
    # Check if user has uploaded resume
    if not user.resumes:
        flash('Please upload your resume first before applying', 'error')
        return redirect(url_for('dashboard'))
    
    # Get resume
    if not resume_id:
        # Use latest resume
        resume = Resume.query.filter_by(user_id=user.id).order_by(Resume.uploaded_at.desc()).first()
    else:
        resume = Resume.query.get(resume_id)
        if not resume or resume.user_id != user.id:
            flash('Invalid resume selected', 'error')
            return redirect(url_for('dashboard'))
    
    # Check if already applied to this COMPANY (not just this job)
    existing_application = Application.query.join(Job).filter(
        Application.user_id == user.id,
        Job.company_name == job.company_name
    ).first()
    
    if existing_application:
        flash(f'You have already applied to {job.company_name}. You can only apply once per company.', 'error')
        return redirect(url_for('dashboard'))
    
    # Prepare job requirements
    job_requirements = {
        'position': job.position,
        'required_skills': job.required_skills,
        'experience_required': job.experience_required,
        'education_required': job.education_required,
        'description': job.description
    }
    
    # Calculate ATS score using AI
    ats_analysis = calculate_ats_score_with_ai(resume.extracted_data, job_requirements)
    
    if not ats_analysis:
        flash('Error calculating ATS score. Please try again.', 'error')
        return redirect(url_for('dashboard'))
    
    # Parse ATS score from analysis
    try:
        # Clean the response - remove markdown code blocks if present
        cleaned_analysis = ats_analysis.strip()
        if cleaned_analysis.startswith('```'):
            # Remove markdown code blocks
            lines = cleaned_analysis.split('\n')
            cleaned_analysis = '\n'.join([line for line in lines if not line.startswith('```')])
        
        analysis_data = json.loads(cleaned_analysis)
        ats_score = float(analysis_data.get('ats_score', 0))
        
        # Ensure score is between 0 and 100
        ats_score = max(0, min(100, ats_score))
        
    except Exception as e:
        print(f"Error parsing ATS analysis: {e}")
        print(f"Raw analysis: {ats_analysis}")
        ats_score = 0
    
    # Create application
    application = Application(
        user_id=user.id,
        job_id=job_id,
        resume_id=resume.id,
        ats_score=ats_score,
        ats_analysis=ats_analysis
    )
    db.session.add(application)
    db.session.commit()
    
    flash(f'Application submitted successfully! Your ATS Score: {ats_score}%', 'success')
    return redirect(url_for('view_application', app_id=application.id))

@app.route('/application/<int:app_id>')
@login_required
def view_application(app_id):
    application = Application.query.get_or_404(app_id)
    
    # Check if application belongs to current user or user is admin
    user = User.query.get(session['user_id'])
    if application.user_id != user.id and not user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    # Parse ATS analysis
    try:
        # Clean the response - remove markdown code blocks if present
        cleaned_analysis = application.ats_analysis.strip()
        if cleaned_analysis.startswith('```'):
            lines = cleaned_analysis.split('\n')
            cleaned_analysis = '\n'.join([line for line in lines if not line.startswith('```')])
        
        analysis = json.loads(cleaned_analysis)
    except Exception as e:
        print(f"Error parsing analysis: {e}")
        analysis = None
    
    return render_template('view_application.html', application=application, analysis=analysis)

@app.route('/admin')
@admin_required
def admin_dashboard():
    # Get all users (non-admin)
    users = User.query.filter_by(is_admin=False).all()
    all_users = User.query.all()
    
    # Get all jobs
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    
    # Get ALL applications across the system
    all_applications = Application.query.all()
    
    # Calculate comprehensive stats for graphs
    admin_stats = {
        'total_users': len(users),
        'total_admins': len([u for u in all_users if u.is_admin]),
        'total_jobs': len(jobs),
        'total_applications': len(all_applications),
        'total_resumes': Resume.query.count(),
        
        # Application status breakdown
        'pending_apps': len([app for app in all_applications if app.status == 'pending']),
        'shortlisted_apps': len([app for app in all_applications if app.status == 'shortlisted']),
        'rejected_apps': len([app for app in all_applications if app.status == 'rejected']),
        
        # ATS score ranges
        'ats_excellent': len([app for app in all_applications if app.ats_score >= 70]),
        'ats_good': len([app for app in all_applications if app.ats_score >= 50 and app.ats_score < 70]),
        'ats_needs_work': len([app for app in all_applications if app.ats_score < 50]),
        
        # Applications by job (top 10)
        'jobs_with_apps': [],
        
        # Applications over time (last 7 days)
        'applications_timeline': [],
        
        # Top skills across all resumes
        'top_skills': {},
        
        # User engagement (users with applications)
        'active_users': len(set([app.user_id for app in all_applications])),
        'inactive_users': len(users) - len(set([app.user_id for app in all_applications])),
        
        # Average ATS scores by job
        'avg_ats_by_job': []
    }
    
    # Calculate applications per job
    for job in jobs:
        job_apps = [app for app in all_applications if app.job_id == job.id]
        if job_apps:
            admin_stats['jobs_with_apps'].append({
                'name': f"{job.company_name} - {job.position}",
                'count': len(job_apps)
            })
    
    # Sort and get top 10 jobs
    admin_stats['jobs_with_apps'] = sorted(
        admin_stats['jobs_with_apps'], 
        key=lambda x: x['count'], 
        reverse=True
    )[:10]
    
    # Calculate applications timeline (last 7 days)
    from datetime import timedelta
    today = datetime.utcnow().date()
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = len([app for app in all_applications if app.applied_at.date() == date])
        admin_stats['applications_timeline'].append({
            'date': date.strftime('%b %d'),
            'count': count
        })
    
    # Extract top skills from all resumes
    all_resumes = Resume.query.all()
    skill_counts = {}
    for resume in all_resumes:
        try:
            data = json.loads(resume.extracted_data)
            skills = data.get('skills', [])
            for skill in skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        except:
            pass
    
    # Get top 10 skills
    admin_stats['top_skills'] = sorted(
        [{'skill': k, 'count': v} for k, v in skill_counts.items()],
        key=lambda x: x['count'],
        reverse=True
    )[:10]
    
    # Calculate average ATS score by job (top 10)
    for job in jobs:
        job_apps = [app for app in all_applications if app.job_id == job.id]
        if job_apps:
            avg_score = sum([app.ats_score for app in job_apps]) / len(job_apps)
            admin_stats['avg_ats_by_job'].append({
                'name': f"{job.company_name} - {job.position}",
                'avg_score': round(avg_score, 1)
            })
    
    # Sort and get top 10
    admin_stats['avg_ats_by_job'] = sorted(
        admin_stats['avg_ats_by_job'],
        key=lambda x: x['avg_score'],
        reverse=True
    )[:10]
    
    # Prepare job stats for display (with datetime objects for template)
    job_stats = []
    job_stats_json = []  # JSON-serializable version for JavaScript
    
    for job in jobs:
        applications = Application.query.filter_by(job_id=job.id).all()
        
        # For template (with datetime)
        job_stats.append({
            'job': {
                'id': job.id,
                'company_name': job.company_name,
                'company_logo': job.company_logo,
                'position': job.position,
                'required_skills': job.required_skills,
                'vacancies': job.vacancies,
                'created_at': job.created_at
            },
            'total_applications': len(applications)
        })
        
        # For JavaScript (JSON-serializable)
        job_stats_json.append({
            'job': {
                'id': job.id,
                'company_name': job.company_name,
                'company_logo': job.company_logo,
                'position': job.position,
                'required_skills': job.required_skills,
                'vacancies': job.vacancies,
                'created_at': job.created_at.isoformat()
            },
            'total_applications': len(applications)
        })
    
    # Convert users to JSON-serializable format
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'mobile': user.mobile,
            'is_admin': user.is_admin
        })
    
    return render_template('admin.html', users=users, job_stats=job_stats, job_stats_json=job_stats_json, admin_stats=admin_stats, users_data=users_data)

@app.route('/admin/create_job', methods=['GET', 'POST'])
@admin_required
def create_job():
    if request.method == 'POST':
        company_name = request.form.get('company_name', '').strip()
        company_logo_url = request.form.get('company_logo', '').strip()
        position = request.form.get('position', '').strip()
        required_skills = request.form.get('required_skills', '').strip()
        experience_required = request.form.get('experience_required', '').strip()
        education_required = request.form.get('education_required', '').strip()
        vacancies = request.form.get('vacancies', '').strip()
        description = request.form.get('description', '').strip()
        
        if not all([company_name, position, required_skills, vacancies]):
            flash('Please fill all required fields', 'error')
            return redirect(url_for('create_job'))
        
        try:
            vacancies = int(vacancies)
            if vacancies < 1:
                raise ValueError
        except:
            flash('Vacancies must be a positive number', 'error')
            return redirect(url_for('create_job'))
        
        # Handle company logo - either URL or file upload
        company_logo = company_logo_url  # Default to URL if provided
        
        # Check if file was uploaded
        if 'company_logo_file' in request.files:
            file = request.files['company_logo_file']
            if file and file.filename != '':
                # Validate file type
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                
                if file_ext in allowed_extensions:
                    # Create company_logos folder if not exists
                    logos_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'company_logos')
                    os.makedirs(logos_folder, exist_ok=True)
                    
                    # Save with unique name
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    safe_company_name = secure_filename(company_name.replace(' ', '_'))
                    new_filename = f"{safe_company_name}_{timestamp}.{file_ext}"
                    filepath = os.path.join(logos_folder, new_filename)
                    file.save(filepath)
                    
                    # Store relative path for template
                    company_logo = f"company_logos/{new_filename}"
                else:
                    flash('Invalid image format. Allowed: PNG, JPG, JPEG, GIF, SVG, WEBP', 'error')
                    return redirect(url_for('create_job'))
        
        job = Job(
            company_name=company_name,
            company_logo=company_logo,
            position=position,
            required_skills=required_skills,
            experience_required=experience_required,
            education_required=education_required,
            vacancies=vacancies,
            description=description,
            created_by=session['user_id']
        )
        db.session.add(job)
        db.session.commit()
        
        flash(f'Job posting created successfully for {company_name}!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('create_job.html')

@app.route('/admin/job/<int:job_id>')
@admin_required
def view_job_applications(job_id):
    job = Job.query.get_or_404(job_id)
    applications = Application.query.filter_by(job_id=job_id).order_by(Application.ats_score.desc()).all()
    
    return render_template('job_applications.html', job=job, applications=applications)

@app.route('/admin/delete_job/<int:job_id>', methods=['POST'])
@admin_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash(f'Job posting for {job.company_name} deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_application_status/<int:app_id>/<status>', methods=['POST'])
@admin_required
def update_application_status(app_id, status):
    application = Application.query.get_or_404(app_id)
    admin_message = request.form.get('admin_message', '').strip()
    
    if status in ['pending', 'shortlisted', 'rejected']:
        old_status = application.status
        
        # VACANCY VALIDATION: Check if shortlisting would exceed vacancy count
        if status == 'shortlisted' and old_status != 'shortlisted':
            job = application.job
            
            # Count currently shortlisted candidates for this job
            current_shortlisted = Application.query.filter_by(
                job_id=job.id,
                status='shortlisted'
            ).count()
            
            # Check if we've reached the vacancy limit
            if current_shortlisted >= job.vacancies:
                flash(f'❌ Cannot shortlist more candidates! This job has {job.vacancies} {"vacancy" if job.vacancies == 1 else "vacancies"} and {current_shortlisted} candidates are already shortlisted. Please reject some candidates first or increase vacancy count.', 'error')
                return redirect(request.referrer or url_for('admin_dashboard'))
        
        # Update status
        application.status = status
        application.status_updated_at = datetime.utcnow()
        application.is_read = False  # Mark as unread for user
        
        # Set default messages if admin didn't provide one
        if not admin_message:
            if status == 'shortlisted':
                admin_message = f"Congratulations! You have been shortlisted for the {application.job.position} position at {application.job.company_name}. We will contact you soon for the next steps."
            elif status == 'rejected':
                admin_message = f"Thank you for applying to the {application.job.position} position at {application.job.company_name}. After careful consideration, we have decided to move forward with other candidates. We encourage you to apply for future opportunities."
            elif status == 'pending':
                admin_message = f"Your application for {application.job.position} at {application.job.company_name} is under review."
        
        application.admin_message = admin_message
        db.session.commit()
        
        flash(f'✅ Application status updated to {status}. Notification sent to candidate.', 'success')
    return redirect(request.referrer or url_for('admin_dashboard'))

@app.route('/mark_notification_read/<int:app_id>', methods=['POST'])
@login_required
def mark_notification_read(app_id):
    application = Application.query.get_or_404(app_id)
    
    # Check if application belongs to current user
    if application.user_id != session['user_id']:
        flash('Unauthorized action', 'error')
        return redirect(url_for('dashboard'))
    
    application.is_read = True
    db.session.commit()
    
    return redirect(url_for('notifications'))

@app.route('/notifications')
@login_required
def notifications():
    user = User.query.get(session['user_id'])
    
    # Get all notifications (applications with status updates)
    all_notifications = Application.query.filter_by(user_id=user.id).filter(
        Application.status.in_(['shortlisted', 'rejected'])
    ).order_by(Application.status_updated_at.desc()).all()
    
    # Get unread count for badge
    unread_count = Application.query.filter_by(user_id=user.id, is_read=False).filter(
        Application.status.in_(['shortlisted', 'rejected'])
    ).count()
    
    return render_template('notifications.html', user=user, notifications=all_notifications, unread_count=unread_count)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user and not user.is_admin:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} deleted successfully', 'success')
    else:
        flash('Cannot delete this user', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/toggle_admin/<int:user_id>', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_admin = not user.is_admin
        db.session.commit()
        status = 'admin' if user.is_admin else 'regular user'
        flash(f'User {user.username} is now a {status}', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if request.method == 'POST':
        new_api_key = request.form.get('groq_api_key', '').strip()
        
        if not new_api_key:
            flash('API key cannot be empty', 'error')
            return redirect(url_for('admin_settings'))
        
        # Update or create the setting
        setting = Settings.query.filter_by(key='groq_api_key').first()
        if setting:
            setting.value = new_api_key
            setting.updated_at = datetime.utcnow()
        else:
            setting = Settings(key='groq_api_key', value=new_api_key)
            db.session.add(setting)
        
        db.session.commit()
        flash('✅ Groq API key updated successfully!', 'success')
        return redirect(url_for('admin_settings'))
    
    # GET request - show current API key
    current_key = get_groq_api_key()
    setting = Settings.query.filter_by(key='groq_api_key').first()
    last_updated = setting.updated_at if setting else None
    
    return render_template('admin_settings.html', current_key=current_key, last_updated=last_updated)

# Route to serve uploaded files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files (resumes, company logos, etc.)"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
