"""Test script to verify Groq API connectivity and resume extraction"""

from openai import OpenAI
import json

GROQ_API_KEY = "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"

def test_groq_connection():
    """Test basic Groq API connection"""
    try:
        print("🔍 Testing Groq API connection...")
        
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            timeout=30.0
        )
        
        # Simple test
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'API Working' in JSON format"}],
            temperature=0.3,
            response_format={"type": "json_object"},
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        print(f"✅ Groq API is working!")
        print(f"Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Groq API connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_resume_extraction():
    """Test resume extraction with sample data"""
    try:
        print("\n🔍 Testing resume extraction...")
        
        sample_resume = """
        John Doe
        Software Engineer
        Email: john@example.com | Phone: 123-456-7890
        
        PROFESSIONAL SUMMARY
        Experienced software engineer with 3 years of experience in full-stack development.
        
        SKILLS
        Python, JavaScript, React, Node.js, Django, Flask, SQL, MongoDB, AWS, Docker, Git
        
        EXPERIENCE
        Software Engineer | Tech Corp | 2021 - Present (3 years)
        - Developed microservices using Python and Django
        - Built React-based web applications
        - Managed AWS cloud infrastructure
        
        EDUCATION
        Bachelor of Technology in Computer Science
        XYZ University | 2021
        
        PROJECTS
        1. E-commerce Platform - Built using React and Node.js
        2. ML Recommendation System - Developed using Python and TensorFlow
        
        CERTIFICATIONS
        - AWS Certified Solutions Architect
        - Google Cloud Professional
        """
        
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            timeout=30.0
        )
        
        prompt = f"""Extract information from this resume and return ONLY valid JSON:

{sample_resume}

Return this structure:
{{
    "skills": ["list of skills"],
    "experience": "X years or Fresher",
    "education": ["degrees"],
    "certifications": ["certs"],
    "projects": ["projects"],
    "summary": "professional summary"
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        parsed = json.loads(result)
        
        print(f"✅ Resume extraction successful!")
        print(f"\n📊 Extracted Data:")
        print(f"Skills: {len(parsed.get('skills', []))} found")
        print(f"Experience: {parsed.get('experience', 'N/A')}")
        print(f"Education: {parsed.get('education', [])}")
        print(f"Certifications: {len(parsed.get('certifications', []))} found")
        print(f"Projects: {len(parsed.get('projects', []))} found")
        print(f"\nFull Response:\n{json.dumps(parsed, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Resume extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("GROQ API TEST SUITE")
    print("=" * 60)
    
    # Test 1: Basic connectivity
    test1 = test_groq_connection()
    
    # Test 2: Resume extraction
    test2 = test_resume_extraction()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"Groq API Connection: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Resume Extraction: {'✅ PASS' if test2 else '❌ FAIL'}")
    print("=" * 60)
