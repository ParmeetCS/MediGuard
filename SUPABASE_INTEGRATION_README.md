# Daily Health Check - Supabase Integration

## ✅ What's Been Done

### 1. Updated daily_check.py
- ✅ Added Supabase integration
- ✅ Saves health check data to `health_checks` table
- ✅ Loads historical data from Supabase
- ✅ Includes JSON backup fallback
- ✅ Displays trends from database

### 2. Created SQL Schema Files
- ✅ `SETUP_HEALTH_CHECKS_TABLE.sql` - **Run this in Supabase!**
- ✅ `health_checks_enhanced_schema.sql` - Alternative comprehensive schema

## 🚀 Setup Instructions

### Step 1: Run SQL in Supabase

1. Go to your Supabase Dashboard
2. Navigate to: **SQL Editor** (left sidebar)
3. Click: **New Query**
4. Open file: `SETUP_HEALTH_CHECKS_TABLE.sql`
5. Copy all content and paste into Supabase SQL Editor
6. Click: **Run** (or press Ctrl+Enter)

You should see: "Success. No rows returned"

### Step 2: Verify Table Created

1. In Supabase, go to: **Table Editor** (left sidebar)
2. Look for: `health_checks` table
3. You should see columns like:
   - user_id
   - check_date
   - sit_stand_movement_speed
   - walk_stability
   - steady_stability
   - avg_movement_speed
   - avg_stability
   - etc.

### Step 3: Test the Integration

1. Run your Streamlit app
2. Go to: **Daily Health Check** page
3. Complete all 3 activities:
   - Sit to Stand
   - Short Walk
   - Hold Steady
4. Click: **Save Results**
5. Should see: "✅ Health check data saved to database successfully!"

### Step 4: Verify Data in Supabase

1. Go to Supabase **Table Editor**
2. Select: `health_checks` table
3. You should see your data with today's date!

## 📊 Data Flow

```
Camera Capture → Feature Extraction → Combine Features → Save to Supabase
     (OpenCV)         (vision/)          (daily_check.py)    (health_checks)
```

## 🗂️ Table Structure

**health_checks** table stores:

### Per Activity Data:
- **sit_stand_*** - Features from Sit-to-Stand test
- **walk_*** - Features from Walking test  
- **steady_*** - Features from Steady Hold test

### Summary Metrics:
- **avg_movement_speed** - Average across all activities
- **avg_stability** - Average stability score

### Metadata:
- **user_id** - From Supabase Auth
- **check_date** - Date of check (unique per user/day)
- **check_timestamp** - Exact time of check
- **created_at** / **updated_at** - Timestamps

## 🔒 Security (RLS)

Row Level Security ensures:
- ✅ Users can only see their own data
- ✅ Users can only insert their own data
- ✅ Users can only update their own data
- ✅ Data is isolated by auth.uid()

## 📈 Features

1. **Automatic Save**: Data saves to Supabase after completing all tests
2. **Historical Trends**: View your progress over time with charts
3. **Backup Storage**: Also saves to local JSON as fallback
4. **One Check Per Day**: Constraint prevents duplicate entries

## 🐛 Troubleshooting

**If save fails:**
- Check Supabase connection in .env file
- Check user is logged in (user_id in session)
- Data will fallback to local JSON file

**If table doesn't exist:**
- Run the SQL script again
- Check for error messages in Supabase SQL Editor

**If RLS blocks access:**
- Ensure user is authenticated
- Check auth.uid() matches user_id column

## 🎯 Next Steps

After setup, your daily health checks will:
1. ✅ Save to Supabase automatically
2. ✅ Be available for AI agent analysis
3. ✅ Show historical trends
4. ✅ Enable drift detection
