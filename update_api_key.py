"""Update Groq API key in database"""

from app import app, db, Settings

with app.app_context():
    # Update or create Groq API key setting
    groq_setting = Settings.query.filter_by(key='groq_api_key').first()
    
    new_key = "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"
    
    if groq_setting:
        groq_setting.value = new_key
        print("✅ Updated existing Groq API key in database")
    else:
        groq_setting = Settings(
            key='groq_api_key',
            value=new_key
        )
        db.session.add(groq_setting)
        print("✅ Created new Groq API key setting in database")
    
    db.session.commit()
    print(f"✅ API Key saved: {new_key[:20]}...")
    print("✅ Database updated successfully!")
