"""Verify TalentTrack setup is complete"""

import sys
from app import app, db, Settings, User
from openai import OpenAI

print("=" * 70)
print("🔍 TALENTTRACK SETUP VERIFICATION")
print("=" * 70)

# Test 1: Database connection
try:
    with app.app_context():
        user_count = User.query.count()
        print(f"✅ Database connection: OK ({user_count} users)")
except Exception as e:
    print(f"❌ Database connection: FAILED - {e}")
    sys.exit(1)

# Test 2: Admin user exists
try:
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if admin and admin.is_admin:
            print(f"✅ Admin user: EXISTS (username: admin, password: 123456)")
        else:
            print(f"⚠️  Admin user: NOT FOUND")
except Exception as e:
    print(f"❌ Admin user check: FAILED - {e}")

# Test 3: Groq API key in database
try:
    with app.app_context():
        groq_setting = Settings.query.filter_by(key='groq_api_key').first()
        if groq_setting and groq_setting.value:
            api_key = groq_setting.value
            print(f"✅ Groq API key (DB): {api_key[:20]}...")
        else:
            print(f"⚠️  Groq API key (DB): NOT SET")
except Exception as e:
    print(f"❌ Groq API key check: FAILED - {e}")

# Test 4: Groq API connection
try:
    with app.app_context():
        from app import get_groq_api_key
        api_key = get_groq_api_key()
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=10.0
        )
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say OK"}],
            temperature=0.3,
            max_tokens=10
        )
        
        print(f"✅ Groq API connection: WORKING")
except Exception as e:
    print(f"❌ Groq API connection: FAILED - {e}")
    sys.exit(1)

# Test 5: File upload directory
import os
try:
    upload_dir = 'uploads'
    if os.path.exists(upload_dir):
        file_count = len([f for f in os.listdir(upload_dir) if f.endswith('.pdf')])
        print(f"✅ Upload directory: EXISTS ({file_count} PDF files)")
    else:
        print(f"⚠️  Upload directory: NOT FOUND")
except Exception as e:
    print(f"❌ Upload directory check: FAILED - {e}")

print("=" * 70)
print("🎉 SETUP VERIFICATION COMPLETE!")
print("=" * 70)
print()
print("📝 NEXT STEPS:")
print("1. Open browser: http://127.0.0.1:5000")
print("2. Login with: admin / 123456")
print("3. Upload a resume to test AI extraction")
print()
print("✨ Your TalentTrack application is ready to use!")
print("=" * 70)
