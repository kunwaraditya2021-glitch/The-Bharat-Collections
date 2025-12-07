#!/usr/bin/env python3
"""
Check Flask app status and Supabase configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("BHARAT COLLECTIONS - AUTHENTICATION SETUP STATUS")
print("=" * 60)

# Check .env configuration
print("\n1. SUPABASE CREDENTIALS:")
print("-" * 60)

supabase_url = os.getenv('SUPABASE_URL', '')
supabase_key = os.getenv('SUPABASE_KEY', '')
supabase_service_key = os.getenv('SUPABASE_SERVICE_KEY', '')

if supabase_url:
    print(f"✓ SUPABASE_URL: {supabase_url}")
else:
    print("✗ SUPABASE_URL: NOT CONFIGURED")

if supabase_key:
    key_preview = supabase_key[:20] + "..." + supabase_key[-10:]
    print(f"✓ SUPABASE_KEY: {key_preview}")
else:
    print("✗ SUPABASE_KEY: NOT CONFIGURED")

if supabase_service_key:
    print(f"✓ SUPABASE_SERVICE_KEY: Loaded")
else:
    print("✗ SUPABASE_SERVICE_KEY: NOT CONFIGURED")

# Check JWT configuration
print("\n2. JWT AUTHENTICATION:")
print("-" * 60)

jwt_secret = os.getenv('JWT_SECRET', '')
jwt_expiration = os.getenv('JWT_EXPIRATION_HOURS', '')

if jwt_secret:
    print(f"✓ JWT_SECRET: Configured")
else:
    print("✗ JWT_SECRET: NOT CONFIGURED")

if jwt_expiration:
    print(f"✓ JWT_EXPIRATION_HOURS: {jwt_expiration}")
else:
    print("✗ JWT_EXPIRATION_HOURS: NOT CONFIGURED")

# Check Flask configuration
print("\n3. FLASK CONFIGURATION:")
print("-" * 60)

flask_secret = os.getenv('FLASK_SECRET_KEY', '')
flask_host = os.getenv('FLASK_HOST', '0.0.0.0')
flask_port = os.getenv('FLASK_PORT', '5000')
flask_debug = os.getenv('FLASK_DEBUG', 'False')

if flask_secret:
    print(f"✓ FLASK_SECRET_KEY: Configured")
else:
    print("✗ FLASK_SECRET_KEY: NOT CONFIGURED")

print(f"✓ FLASK_HOST: {flask_host}")
print(f"✓ FLASK_PORT: {flask_port}")
print(f"✓ FLASK_DEBUG: {flask_debug}")

# Check required Python libraries
print("\n4. REQUIRED LIBRARIES:")
print("-" * 60)

required_libs = {
    'flask': 'Flask web framework',
    'supabase': 'Supabase database client',
    'jwt': 'JWT token handling',
    'bcrypt': 'Password hashing',
    'python_dotenv': 'Environment variable loader',
}

for lib, description in required_libs.items():
    try:
        __import__(lib)
        print(f"✓ {lib}: Installed ({description})")
    except ImportError:
        print(f"✗ {lib}: NOT INSTALLED ({description})")

# Summary
print("\n" + "=" * 60)
print("NEXT STEPS:")
print("=" * 60)

if supabase_url and supabase_key:
    print("\n✓ Supabase credentials are configured!")
    print("\n📋 ACTION REQUIRED:")
    print("  1. Go to: https://app.supabase.com/")
    print("  2. Open your project")
    print("  3. Create the 'users' table using SQL Editor:")
    print("     See SUPABASE_TABLE_SETUP.md for the SQL script")
    print("\n  4. Once table is created, restart Flask app:")
    print("     python app.py")
    print("\n  5. Test signup at: http://localhost:5000")
    print("     Click 'Account' button in navbar")
else:
    print("\n✗ Supabase credentials are missing!")
    print("\n📋 ACTION REQUIRED:")
    print("  1. Create a Supabase project at: https://supabase.com")
    print("  2. Get your credentials from: Project Settings > API")
    print("  3. Add to .env file:")
    print("     SUPABASE_URL=your-url")
    print("     SUPABASE_KEY=your-key")

print("\n" + "=" * 60)
