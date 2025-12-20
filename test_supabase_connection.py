"""
Test Supabase connection and verify table structure
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

print("=" * 60)
print("SUPABASE CONNECTION TEST")
print("=" * 60)

# Test 1: Check environment variables
print("\n1. Checking environment variables...")
print(f"   SUPABASE_URL: {SUPABASE_URL[:30]}..." if SUPABASE_URL else "   ❌ SUPABASE_URL not found")
print(f"   SUPABASE_KEY: {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "   ❌ SUPABASE_KEY not found")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("\n❌ ERROR: Missing Supabase credentials in .env file")
    exit(1)

# Test 2: Create Supabase client
print("\n2. Creating Supabase client...")
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("   ✅ Client created successfully")
except Exception as e:
    print(f"   ❌ Error creating client: {e}")
    exit(1)

# Test 3: Check if health_checks table exists
print("\n3. Checking if 'health_checks' table exists...")
try:
    # Try to query the table (limit 0 to not fetch data)
    response = supabase.table('health_checks').select('*').limit(0).execute()
    print("   ✅ Table 'health_checks' exists!")
except Exception as e:
    print(f"   ❌ Table check failed: {e}")
    print("\n   💡 Solution: Run the SQL script in Supabase SQL Editor:")
    print("      File: SETUP_HEALTH_CHECKS_TABLE.sql")
    exit(1)

# Test 4: Check table structure
print("\n4. Checking table structure...")
try:
    # Try to fetch one row to see structure
    response = supabase.table('health_checks').select('*').limit(1).execute()
    
    if response.data:
        print(f"   ✅ Table has {len(response.data)} record(s)")
        print("\n   Sample record structure:")
        for key in response.data[0].keys():
            print(f"      - {key}")
    else:
        print("   ℹ️ Table exists but has no data yet")
        print("   This is normal if no health checks have been completed")
        
except Exception as e:
    print(f"   ⚠️ Could not fetch sample data: {e}")

# Test 5: Check required columns
print("\n5. Checking for required columns...")
required_columns = [
    'user_id', 'check_date', 'check_timestamp',
    'sit_stand_movement_speed', 'sit_stand_stability',
    'walk_movement_speed', 'walk_stability',
    'steady_movement_speed', 'steady_stability',
    'avg_movement_speed', 'avg_stability'
]

try:
    # Try a test query with specific columns
    test_response = supabase.table('health_checks').select(','.join(required_columns)).limit(0).execute()
    print("   ✅ All required columns exist!")
except Exception as e:
    error_str = str(e)
    print(f"   ❌ Column check failed: {error_str}")
    
    # Try to identify missing columns
    if 'does not exist' in error_str.lower():
        print("\n   💡 Solution: Some columns are missing. Run the SQL migration:")
        print("      File: SETUP_HEALTH_CHECKS_TABLE.sql")
        print("      This will add missing columns without losing data")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
