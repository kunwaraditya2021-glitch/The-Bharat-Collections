# Supabase Authentication Setup Guide

This guide will help you set up real user authentication with Supabase for The Bharat Collections.

## Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up or log in with your account
4. Create a new project:
   - **Project Name**: The Bharat Collections (or your choice)
   - **Database Password**: Create a strong password
   - **Region**: Choose the closest region to your users
5. Wait for the project to be initialized (2-3 minutes)

## Step 2: Get Your API Credentials

1. In your Supabase project, go to **Settings** (gear icon)
2. Click on **API** in the left sidebar
3. Copy these credentials:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_KEY`
   - **service_role** secret → `SUPABASE_SERVICE_KEY`

## Step 3: Create Users Table

1. In Supabase, go to the **SQL Editor** (left sidebar)
2. Click **New Query**
3. Copy and paste this SQL:

```sql
-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);

-- Enable RLS (Row Level Security)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows users to read their own data
CREATE POLICY "Users can read own data"
    ON users FOR SELECT
    USING (auth.uid()::text = id::text);
```

4. Click **Run** button to execute the SQL

## Step 4: Update Your `.env` File

1. In the project root directory, create or update the `.env` file
2. Add these environment variables:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
FLASK_SECRET_KEY=your-flask-secret-key-change-this
```

3. **Important**: Never commit `.env` to Git (add to `.gitignore`)

## Step 5: Install Required Python Packages

```bash
pip install supabase
pip install python-dotenv
pip install bcrypt
pip install pyjwt
```

## Step 6: Test the Integration

1. Start your Flask app:
```bash
python app.py
```

2. Open your browser and go to `http://localhost:5000`

3. Click the **Account** button in the navbar

4. Try signing up with:
   - **Name**: John Doe
   - **Email**: john@example.com
   - **Password**: testpass123 (min 8 chars)

5. If successful, you'll be logged in automatically

6. Try logging out and signing back in with your credentials

## Step 7: Verify in Supabase

1. Go to your Supabase project
2. Click on **Table Editor** (left sidebar)
3. Select the **users** table
4. You should see your newly created user record with encrypted password

## Troubleshooting

### "Signup failed: Signup failed" Error
- **Check**: Is `SUPABASE_URL` set correctly?
- **Check**: Is `SUPABASE_KEY` (anon key) correct?
- **Check**: Does the `users` table exist with correct columns?
- **Check**: Are you using Python 3.7+ and have all dependencies installed?

### "Connection refused" Error
- **Check**: Is Supabase service running? (Test at https://supabase.com)
- **Check**: Is your internet connection working?
- **Check**: Is the `SUPABASE_URL` correct? (should start with `https://`)

### Password Issues
- **Check**: Is password at least 8 characters?
- **Check**: Do passwords match in signup form?
- **Check**: Are you using the correct email/password at login?

### User Not Found at Login
- **Check**: Did you sign up first?
- **Check**: Are you using the same email address?
- **Check**: Check Supabase Table Editor to see if user exists

## Security Notes

⚠️ **Production Security Checklist**:
1. Use `SUPABASE_SERVICE_KEY` only on backend (never expose to frontend)
2. Use `SUPABASE_KEY` for frontend (it's public)
3. Always hash passwords before storing (bcrypt handles this)
4. Enable HTTPS in production
5. Implement rate limiting on auth endpoints
6. Add email verification before account activation
7. Use strong JWT secrets (generate with: `openssl rand -hex 32`)
8. Enable Row Level Security (RLS) policies in Supabase
9. Regularly rotate API keys
10. Monitor failed login attempts

## Next Steps

After successful setup:
1. ✅ Users can now sign up and create accounts
2. ✅ Users can login with their credentials
3. ✅ Account button shows logged-in user's name
4. 🔄 Implement email verification
5. 🔄 Add password reset functionality
6. 🔄 Add social login (Google, Facebook)
7. 🔄 Connect orders to user accounts

---

**Questions?** Check the Supabase documentation: https://supabase.com/docs
