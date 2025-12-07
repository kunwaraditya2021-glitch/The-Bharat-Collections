#!/usr/bin/env python3
"""
Test Supabase connection and create users table if it doesn't exist
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY loaded: {'Yes' if SUPABASE_KEY else 'No'}")
print(f"SUPABASE_SERVICE_KEY loaded: {'Yes' if SUPABASE_SERVICE_KEY else 'No'}")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("\n❌ Error: Supabase credentials not found in .env")
    sys.exit(1)

try:
    from supabase import create_client
    print("\n✓ Supabase library imported successfully")
    
    # Create Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Supabase client created")
    
    # Test connection
    try:
        response = supabase.table("users").select("*").limit(1).execute()
        print("✓ Users table exists!")
        print(f"  Current users in table: {len(response.data)}")
        if response.data:
            print(f"  Sample user: {response.data[0]}")
    except Exception as table_error:
        print(f"⚠ Users table doesn't exist or error: {str(table_error)}")
        print("\nTo create the users table, please run the SQL in Supabase:")
        print("""
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
        """)
        
except ImportError:
    print("\n❌ Error: supabase-py library not installed")
    print("Run: pip install supabase")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {str(e)}")
    sys.exit(1)

print("\n✓ All checks passed!")
