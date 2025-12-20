-- ========================================
-- Enhanced Health Checks Table Schema
-- For comprehensive daily health check data
-- ========================================

-- Drop existing table if you want to recreate with new columns
-- DROP TABLE IF EXISTS health_checks CASCADE;

-- Create or replace health_checks table with comprehensive columns
CREATE TABLE IF NOT EXISTS health_checks (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    check_date DATE NOT NULL DEFAULT CURRENT_DATE,
    check_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Sit-to-Stand Activity
    sit_stand_movement_speed FLOAT,
    sit_stand_stability FLOAT,
    sit_stand_motion_smoothness FLOAT,
    sit_stand_posture_deviation FLOAT,
    sit_stand_micro_movements FLOAT,
    sit_stand_range_of_motion FLOAT,
    sit_stand_acceleration_variance FLOAT,
    sit_stand_time FLOAT,
    
    -- Walking Activity
    walk_movement_speed FLOAT,
    walk_stability FLOAT,
    walk_motion_smoothness FLOAT,
    walk_posture_deviation FLOAT,
    walk_gait_symmetry FLOAT,
    walk_stride_consistency FLOAT,
    walk_coordination_score FLOAT,
    
    -- Steady Hold Activity
    steady_stability FLOAT,
    steady_micro_movements FLOAT,
    steady_posture_deviation FLOAT,
    steady_tremor_index FLOAT,
    steady_hand_steadiness FLOAT,
    steady_balance_score FLOAT,
    
    -- Overall Summary Metrics
    avg_movement_speed FLOAT,
    avg_stability FLOAT,
    avg_motion_smoothness FLOAT,
    overall_mobility FLOAT,
    overall_coordination FLOAT,
    
    -- Metadata
    total_frames_captured INTEGER,
    check_duration_seconds INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Unique constraint: one check per user per day
    UNIQUE(user_id, check_date)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_health_checks_user_id ON health_checks(user_id);
CREATE INDEX IF NOT EXISTS idx_health_checks_date ON health_checks(check_date);
CREATE INDEX IF NOT EXISTS idx_health_checks_user_date ON health_checks(user_id, check_date DESC);
CREATE INDEX IF NOT EXISTS idx_health_checks_timestamp ON health_checks(check_timestamp DESC);

-- Enable Row Level Security
ALTER TABLE health_checks ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own health checks" ON health_checks;
DROP POLICY IF EXISTS "Users can insert their own health checks" ON health_checks;
DROP POLICY IF EXISTS "Users can update their own health checks" ON health_checks;
DROP POLICY IF EXISTS "Users can delete their own health checks" ON health_checks;

-- Create RLS policies
CREATE POLICY "Users can view their own health checks"
ON health_checks FOR SELECT
USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert their own health checks"
ON health_checks FOR INSERT
WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update their own health checks"
ON health_checks FOR UPDATE
USING (auth.uid()::text = user_id)
WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can delete their own health checks"
ON health_checks FOR DELETE
USING (auth.uid()::text = user_id);

-- Create trigger function for updated_at
CREATE OR REPLACE FUNCTION update_health_checks_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
DROP TRIGGER IF EXISTS update_health_checks_updated_at ON health_checks;
CREATE TRIGGER update_health_checks_updated_at
    BEFORE UPDATE ON health_checks
    FOR EACH ROW
    EXECUTE FUNCTION update_health_checks_updated_at();

-- Add helpful comments
COMMENT ON TABLE health_checks IS 'Stores comprehensive daily health check measurements from camera-based movement analysis';
COMMENT ON COLUMN health_checks.user_id IS 'User identifier from Supabase Auth (auth.uid())';
COMMENT ON COLUMN health_checks.check_date IS 'Date of the health check (used for uniqueness constraint)';
COMMENT ON COLUMN health_checks.check_timestamp IS 'Exact timestamp when check was performed';
COMMENT ON COLUMN health_checks.sit_stand_movement_speed IS 'Movement speed during sit-to-stand activity (0-1 scale)';
COMMENT ON COLUMN health_checks.sit_stand_stability IS 'Stability score during sit-to-stand (0-1 scale)';
COMMENT ON COLUMN health_checks.walk_movement_speed IS 'Movement speed during walking activity (0-1 scale)';
COMMENT ON COLUMN health_checks.steady_stability IS 'Stability score during steady hold test (0-1 scale)';
COMMENT ON COLUMN health_checks.avg_movement_speed IS 'Average movement speed across all activities';
COMMENT ON COLUMN health_checks.avg_stability IS 'Average stability across all activities';
COMMENT ON COLUMN health_checks.overall_mobility IS 'Overall mobility assessment score';

-- Grant necessary permissions (adjust as needed for your setup)
-- GRANT ALL ON health_checks TO authenticated;
-- GRANT ALL ON SEQUENCE health_checks_id_seq TO authenticated;
