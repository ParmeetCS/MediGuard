-- ========================================
-- MediGuard Drift AI - User Profile Table
-- Stores basic user information (name, age, lifestyle)
-- ========================================

-- Create user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    name TEXT,
    age INTEGER,
    lifestyle TEXT,
    additional_context TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on user_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);

-- Enable Row Level Security (RLS)
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can insert their own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can update their own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can delete their own profile" ON user_profiles;

-- Create policy: Users can only read their own profile
CREATE POLICY "Users can view their own profile"
ON user_profiles
FOR SELECT
USING (auth.uid()::text = user_id);

-- Create policy: Users can insert their own profile
CREATE POLICY "Users can insert their own profile"
ON user_profiles
FOR INSERT
WITH CHECK (auth.uid()::text = user_id);

-- Create policy: Users can update their own profile
CREATE POLICY "Users can update their own profile"
ON user_profiles
FOR UPDATE
USING (auth.uid()::text = user_id)
WITH CHECK (auth.uid()::text = user_id);

-- Create policy: Users can delete their own profile
CREATE POLICY "Users can delete their own profile"
ON user_profiles
FOR DELETE
USING (auth.uid()::text = user_id);

-- Create trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_user_profiles_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_user_profiles_updated_at_trigger ON user_profiles;

CREATE TRIGGER update_user_profiles_updated_at_trigger
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_user_profiles_updated_at();

-- Add comments for documentation
COMMENT ON TABLE user_profiles IS 'Stores user basic profile information for personalized health monitoring';
COMMENT ON COLUMN user_profiles.user_id IS 'Unique user identifier from Supabase Auth';
COMMENT ON COLUMN user_profiles.name IS 'User full name';
COMMENT ON COLUMN user_profiles.age IS 'User age for baseline calculations';
COMMENT ON COLUMN user_profiles.lifestyle IS 'Lifestyle category: Student, Working Professional, Athlete, Retired, etc.';
COMMENT ON COLUMN user_profiles.additional_context IS 'Optional additional context (health conditions, fitness goals, lifestyle changes)';
