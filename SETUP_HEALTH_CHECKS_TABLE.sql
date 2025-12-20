-- ========================================
-- SUPABASE SETUP INSTRUCTIONS
-- Run these SQL commands in Supabase SQL Editor
-- ========================================

-- Step 1: Run this in Supabase SQL Editor
-- Navigate to: Supabase Dashboard > SQL Editor > New Query
-- Paste and execute this entire script

-- ========================================
-- OPTION A: Drop and Recreate (if you want fresh start)
-- UNCOMMENT the next line if you want to delete all existing data
-- ========================================
-- DROP TABLE IF EXISTS health_checks CASCADE;

-- ========================================
-- OPTION B: Add Missing Columns (preserves existing data)
-- This will run first and add columns if they don't exist
-- ========================================

-- Add check_timestamp if missing
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='check_timestamp') THEN
        ALTER TABLE health_checks ADD COLUMN check_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW();
    END IF;
END $$;

-- Add Sit-to-Stand columns
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='sit_stand_movement_speed') THEN
        ALTER TABLE health_checks ADD COLUMN sit_stand_movement_speed FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='sit_stand_stability') THEN
        ALTER TABLE health_checks ADD COLUMN sit_stand_stability FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='sit_stand_motion_smoothness') THEN
        ALTER TABLE health_checks ADD COLUMN sit_stand_motion_smoothness FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='sit_stand_posture_deviation') THEN
        ALTER TABLE health_checks ADD COLUMN sit_stand_posture_deviation FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='sit_stand_micro_movements') THEN
        ALTER TABLE health_checks ADD COLUMN sit_stand_micro_movements FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='sit_stand_range_of_motion') THEN
        ALTER TABLE health_checks ADD COLUMN sit_stand_range_of_motion FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='sit_stand_acceleration_variance') THEN
        ALTER TABLE health_checks ADD COLUMN sit_stand_acceleration_variance FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='sit_stand_frame_count') THEN
        ALTER TABLE health_checks ADD COLUMN sit_stand_frame_count INTEGER;
    END IF;
END $$;

-- Add Walking columns
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='walk_movement_speed') THEN
        ALTER TABLE health_checks ADD COLUMN walk_movement_speed FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='walk_stability') THEN
        ALTER TABLE health_checks ADD COLUMN walk_stability FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='walk_motion_smoothness') THEN
        ALTER TABLE health_checks ADD COLUMN walk_motion_smoothness FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='walk_posture_deviation') THEN
        ALTER TABLE health_checks ADD COLUMN walk_posture_deviation FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='walk_micro_movements') THEN
        ALTER TABLE health_checks ADD COLUMN walk_micro_movements FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='walk_range_of_motion') THEN
        ALTER TABLE health_checks ADD COLUMN walk_range_of_motion FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='walk_acceleration_variance') THEN
        ALTER TABLE health_checks ADD COLUMN walk_acceleration_variance FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='walk_frame_count') THEN
        ALTER TABLE health_checks ADD COLUMN walk_frame_count INTEGER;
    END IF;
END $$;

-- Add Steady Hold columns
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='steady_movement_speed') THEN
        ALTER TABLE health_checks ADD COLUMN steady_movement_speed FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='steady_stability') THEN
        ALTER TABLE health_checks ADD COLUMN steady_stability FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='steady_motion_smoothness') THEN
        ALTER TABLE health_checks ADD COLUMN steady_motion_smoothness FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='steady_posture_deviation') THEN
        ALTER TABLE health_checks ADD COLUMN steady_posture_deviation FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='steady_micro_movements') THEN
        ALTER TABLE health_checks ADD COLUMN steady_micro_movements FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='steady_range_of_motion') THEN
        ALTER TABLE health_checks ADD COLUMN steady_range_of_motion FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='steady_acceleration_variance') THEN
        ALTER TABLE health_checks ADD COLUMN steady_acceleration_variance FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='steady_frame_count') THEN
        ALTER TABLE health_checks ADD COLUMN steady_frame_count INTEGER;
    END IF;
END $$;

-- Add Summary columns
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='avg_movement_speed') THEN
        ALTER TABLE health_checks ADD COLUMN avg_movement_speed FLOAT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='avg_stability') THEN
        ALTER TABLE health_checks ADD COLUMN avg_stability FLOAT;
    END IF;
END $$;

-- Add Metadata columns (created_at, updated_at)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='created_at') THEN
        ALTER TABLE health_checks ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='health_checks' AND column_name='updated_at') THEN
        ALTER TABLE health_checks ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
    END IF;
END $$;

-- ========================================
-- Remove UNIQUE Constraint (to allow multiple checks per day)
-- ========================================
ALTER TABLE IF EXISTS health_checks DROP CONSTRAINT IF EXISTS health_checks_user_id_check_date_key;

-- ========================================
-- Now Create Table if it doesn't exist at all
-- ========================================

CREATE TABLE IF NOT EXISTS health_checks (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    check_date DATE NOT NULL DEFAULT CURRENT_DATE,
    check_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Sit-to-Stand Activity Features
    sit_stand_movement_speed FLOAT,
    sit_stand_stability FLOAT,
    sit_stand_motion_smoothness FLOAT,
    sit_stand_posture_deviation FLOAT,
    sit_stand_micro_movements FLOAT,
    sit_stand_range_of_motion FLOAT,
    sit_stand_acceleration_variance FLOAT,
    sit_stand_frame_count INTEGER,
    
    -- Walking Activity Features
    walk_movement_speed FLOAT,
    walk_stability FLOAT,
    walk_motion_smoothness FLOAT,
    walk_posture_deviation FLOAT,
    walk_micro_movements FLOAT,
    walk_range_of_motion FLOAT,
    walk_acceleration_variance FLOAT,
    walk_frame_count INTEGER,
    
    -- Steady Hold Activity Features
    steady_movement_speed FLOAT,
    steady_stability FLOAT,
    steady_motion_smoothness FLOAT,
    steady_posture_deviation FLOAT,
    steady_micro_movements FLOAT,
    steady_range_of_motion FLOAT,
    steady_acceleration_variance FLOAT,
    steady_frame_count INTEGER,
    
    -- Overall Summary Metrics
    avg_movement_speed FLOAT,
    avg_stability FLOAT,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    
    -- NOTE: Removed UNIQUE constraint to allow multiple health checks per day
);

-- ========================================
-- Create Indexes for Performance
-- ========================================

CREATE INDEX IF NOT EXISTS idx_health_checks_user_id ON health_checks(user_id);
CREATE INDEX IF NOT EXISTS idx_health_checks_date ON health_checks(check_date DESC);
CREATE INDEX IF NOT EXISTS idx_health_checks_user_date ON health_checks(user_id, check_date DESC);

-- ========================================
-- Enable Row Level Security
-- ========================================

ALTER TABLE health_checks ENABLE ROW LEVEL SECURITY;

-- ========================================
-- Drop Old Policies (if exists)
-- ========================================

DROP POLICY IF EXISTS "Users can view their own health checks" ON health_checks;
DROP POLICY IF EXISTS "Users can insert their own health checks" ON health_checks;
DROP POLICY IF EXISTS "Users can update their own health checks" ON health_checks;
DROP POLICY IF EXISTS "Users can delete their own health checks" ON health_checks;

-- ========================================
-- Create RLS Policies
-- ========================================

-- Users can only see their own health checks
CREATE POLICY "Users can view their own health checks"
ON health_checks FOR SELECT
USING (auth.uid()::text = user_id);

-- Users can insert their own health checks
CREATE POLICY "Users can insert their own health checks"
ON health_checks FOR INSERT
WITH CHECK (auth.uid()::text = user_id);

-- Users can update their own health checks
CREATE POLICY "Users can update their own health checks"
ON health_checks FOR UPDATE
USING (auth.uid()::text = user_id)
WITH CHECK (auth.uid()::text = user_id);

-- Users can delete their own health checks
CREATE POLICY "Users can delete their own health checks"
ON health_checks FOR DELETE
USING (auth.uid()::text = user_id);

-- ========================================
-- Create Trigger for Updated At
-- ========================================

CREATE OR REPLACE FUNCTION update_health_checks_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_health_checks_updated_at ON health_checks;

CREATE TRIGGER update_health_checks_updated_at
    BEFORE UPDATE ON health_checks
    FOR EACH ROW
    EXECUTE FUNCTION update_health_checks_updated_at();

-- ========================================
-- Add Table Comments
-- ========================================

COMMENT ON TABLE health_checks IS 'Stores daily health check data from camera-based movement analysis';
COMMENT ON COLUMN health_checks.user_id IS 'User ID from Supabase Auth (auth.uid())';
COMMENT ON COLUMN health_checks.check_date IS 'Date of health check (unique per user per day)';
COMMENT ON COLUMN health_checks.sit_stand_movement_speed IS 'Movement speed during sit-to-stand test (0-1)';
COMMENT ON COLUMN health_checks.walk_stability IS 'Stability score during walking test (0-1)';
COMMENT ON COLUMN health_checks.steady_stability IS 'Stability during steady hold test (0-1)';
COMMENT ON COLUMN health_checks.avg_movement_speed IS 'Average movement speed across all tests';
COMMENT ON COLUMN health_checks.avg_stability IS 'Average stability across all tests';

-- ========================================
-- SUCCESS!
-- ========================================

-- If this runs without errors, your table is ready!
-- Now run your Streamlit app and complete a daily health check.
-- Data will be automatically saved to this table.
