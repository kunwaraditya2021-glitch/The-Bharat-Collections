# ACTION REQUIRED: Create Users Table in Supabase

Your Supabase credentials are configured correctly:
- ✓ SUPABASE_URL: https://jrhsxhcidmayyxavhznn.supabase.co
- ✓ SUPABASE_KEY: Loaded from .env

## Next Step: Create the `users` table

You need to create the `users` table in your Supabase database. Here's how:

### Method 1: Using Supabase Dashboard (Easiest)

1. Go to your Supabase project dashboard: https://app.supabase.com/
2. Navigate to **SQL Editor** (on the left sidebar)
3. Click **New Query**
4. Copy and paste this SQL:

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

-- Create index for faster email lookups
CREATE INDEX idx_users_email ON users(email);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
```

5. Click **Run** button (or press Ctrl+Enter)
6. Wait for the query to complete (should say "Success" in green)

### Method 2: Using the Table Editor

1. In Supabase dashboard, click **Table Editor**
2. Click **Create a new table**
3. Name it: `users`
4. Add columns:
   - `id` (UUID, Primary Key, default: gen_random_uuid())
   - `email` (Text, Unique, Not Null)
   - `name` (Text, Not Null)
   - `password` (Text, Not Null)
   - `role` (Text, Default: 'user')
   - `created_at` (Timestamp, Default: now())
   - `updated_at` (Timestamp, Default: now())
5. Click **Save**

## After Creating the Table

Once the table is created, your Flask app will automatically:
1. Connect to Supabase
2. Accept signup requests
3. Create user accounts with hashed passwords
4. Generate JWT tokens for authentication

Then you can test the signup/login in your app's Account modal!

## Verification

To verify the table was created successfully:
1. In Supabase dashboard, click **Table Editor**
2. You should see a `users` table in the list
3. When you click it, you should see the columns listed above
