-- SQL Query to Update user_context_data Table
-- Add new columns for storing AI-extracted key points from health report analysis
-- Run this query in your Supabase SQL Editor

-- Step 1: Add columns for AI analysis key points
ALTER TABLE user_context_data
ADD COLUMN IF NOT EXISTS ai_key_findings TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS ai_health_recommendations TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS ai_abnormal_values TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS ai_positive_aspects TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS ai_next_steps TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- Add comments to document what each column stores
COMMENT ON COLUMN user_context_data.ai_key_findings IS 'Key medical findings extracted from AI analysis of health reports';
COMMENT ON COLUMN user_context_data.ai_health_recommendations IS 'Health recommendations and action items from AI analysis';
COMMENT ON COLUMN user_context_data.ai_abnormal_values IS 'Abnormal test values or out-of-range metrics identified by AI';
COMMENT ON COLUMN user_context_data.ai_positive_aspects IS 'Positive health indicators identified in the report';
COMMENT ON COLUMN user_context_data.ai_next_steps IS 'Prioritized next steps and follow-up actions for the patient';

-- Verify the columns were added successfully
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'user_context_data'
AND column_name LIKE 'ai_%'
ORDER BY ordinal_position;
