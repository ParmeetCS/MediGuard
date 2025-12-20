-- ========================================
-- MediGuard Drift AI - Supabase Database Schema
-- Complete schema for all tables
-- ========================================

-- ========================================
-- User Profile Table
-- Stores basic user information (name, age, lifestyle)
-- ========================================

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

CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);

ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view their own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can insert their own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can update their own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can delete their own profile" ON user_profiles;

CREATE POLICY "Users can view their own profile"
ON user_profiles FOR SELECT
USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert their own profile"
ON user_profiles FOR INSERT
WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update their own profile"
ON user_profiles FOR UPDATE
USING (auth.uid()::text = user_id)
WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can delete their own profile"
ON user_profiles FOR DELETE
USING (auth.uid()::text = user_id);

COMMENT ON TABLE user_profiles IS 'Stores user basic profile information';
COMMENT ON COLUMN user_profiles.user_id IS 'Unique user identifier from Supabase Auth';
COMMENT ON COLUMN user_profiles.name IS 'User full name';
COMMENT ON COLUMN user_profiles.age IS 'User age for baseline calculations';
COMMENT ON COLUMN user_profiles.lifestyle IS 'Lifestyle category';
COMMENT ON COLUMN user_profiles.additional_context IS 'Optional additional context';

-- ========================================
-- User Context Data Table
-- Stores lifestyle and health context
-- ========================================

-- Create user_context_data table
CREATE TABLE IF NOT EXISTS user_context_data (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    medical_summary TEXT,
    known_conditions TEXT,
    report_summary TEXT,
    sleep_hours FLOAT DEFAULT 7.0,
    stress_level TEXT DEFAULT 'medium',
    workload TEXT DEFAULT 'moderate',
    activity_level TEXT DEFAULT 'moderate',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on user_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_context_user_id ON user_context_data(user_id);

-- Enable Row Level Security (RLS)
ALTER TABLE user_context_data ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own context data" ON user_context_data;
DROP POLICY IF EXISTS "Users can insert their own context data" ON user_context_data;
DROP POLICY IF EXISTS "Users can update their own context data" ON user_context_data;
DROP POLICY IF EXISTS "Users can delete their own context data" ON user_context_data;

-- Create policy: Users can only read their own data
CREATE POLICY "Users can view their own context data"
ON user_context_data
FOR SELECT
USING (auth.uid()::text = user_id);

-- Create policy: Users can insert their own data
CREATE POLICY "Users can insert their own context data"
ON user_context_data
FOR INSERT
WITH CHECK (auth.uid()::text = user_id);

-- Create policy: Users can update their own data
CREATE POLICY "Users can update their own context data"
ON user_context_data
FOR UPDATE
USING (auth.uid()::text = user_id)
WITH CHECK (auth.uid()::text = user_id);

-- Create policy: Users can delete their own data
CREATE POLICY "Users can delete their own context data"
ON user_context_data
FOR DELETE
USING (auth.uid()::text = user_id);

-- Create trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_user_context_data_updated_at ON user_context_data;

CREATE TRIGGER update_user_context_data_updated_at
    BEFORE UPDATE ON user_context_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE user_context_data IS 'Stores user health context and lifestyle information for personalized AI insights';
COMMENT ON COLUMN user_context_data.user_id IS 'Unique user identifier from Supabase Auth';
COMMENT ON COLUMN user_context_data.medical_summary IS 'Brief medical history summary';
COMMENT ON COLUMN user_context_data.known_conditions IS 'Known medical conditions being monitored';
COMMENT ON COLUMN user_context_data.report_summary IS 'Summary of recent medical reports';
COMMENT ON COLUMN user_context_data.sleep_hours IS 'Average hours of sleep per night';
COMMENT ON COLUMN user_context_data.stress_level IS 'Current stress level: low, medium, or high';
COMMENT ON COLUMN user_context_data.workload IS 'Work/study load: light, moderate, or heavy';
COMMENT ON COLUMN user_context_data.activity_level IS 'Physical activity level: sedentary, light, moderate, active, very active';

-- ========================================
-- Health Check Data Table
-- Stores daily health check measurements
-- ========================================

CREATE TABLE IF NOT EXISTS health_checks (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    check_date DATE NOT NULL DEFAULT CURRENT_DATE,
    sit_stand_speed FLOAT,
    sit_stand_stability FLOAT,
    walk_speed FLOAT,
    walk_stability FLOAT,
    gait_symmetry FLOAT,
    hand_steadiness FLOAT,
    tremor_index FLOAT,
    coordination_score FLOAT,
    overall_mobility FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, check_date)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_health_checks_user_id ON health_checks(user_id);
CREATE INDEX IF NOT EXISTS idx_health_checks_date ON health_checks(check_date);
CREATE INDEX IF NOT EXISTS idx_health_checks_user_date ON health_checks(user_id, check_date DESC);

-- Enable RLS
ALTER TABLE health_checks ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own health checks" ON health_checks;
DROP POLICY IF EXISTS "Users can insert their own health checks" ON health_checks;
DROP POLICY IF EXISTS "Users can update their own health checks" ON health_checks;
DROP POLICY IF EXISTS "Users can delete their own health checks" ON health_checks;

-- Policies
CREATE POLICY "Users can view their own health checks"
ON health_checks
FOR SELECT
USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert their own health checks"
ON health_checks
FOR INSERT
WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update their own health checks"
ON health_checks
FOR UPDATE
USING (auth.uid()::text = user_id)
WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can delete their own health checks"
ON health_checks
FOR DELETE
USING (auth.uid()::text = user_id);

-- Comments
COMMENT ON TABLE health_checks IS 'Stores daily health check measurements for drift detection';
COMMENT ON COLUMN health_checks.user_id IS 'Unique user identifier from Supabase Auth';
COMMENT ON COLUMN health_checks.check_date IS 'Date of the health check';
COMMENT ON COLUMN health_checks.sit_stand_speed IS 'Sit-to-stand speed in seconds per rep';
COMMENT ON COLUMN health_checks.sit_stand_stability IS 'Sit-to-stand stability percentage';
COMMENT ON COLUMN health_checks.walk_speed IS 'Walking speed in meters per second';
COMMENT ON COLUMN health_checks.walk_stability IS 'Walking stability percentage';
COMMENT ON COLUMN health_checks.overall_mobility IS 'Overall mobility score percentage';
