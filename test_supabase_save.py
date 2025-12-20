"""
Test script to verify Supabase connection and save operation
Run this to diagnose why data isn't being saved
"""

from auth.supabase_auth import get_supabase_client
from storage.health_repository import save_health_check
from datetime import date

print("=" * 60)
print("SUPABASE CONNECTION TEST")
print("=" * 60)

# Test 1: Check if client can be created
print("\n1. Testing Supabase client initialization...")
try:
    client = get_supabase_client()
    print("   ✅ Client created successfully")
    print(f"   URL: {client.supabase_url if hasattr(client, 'supabase_url') else 'N/A'}")
except Exception as e:
    print(f"   ❌ Failed to create client: {e}")
    exit(1)

# Test 2: Check table access
print("\n2. Testing table read access...")
try:
    response = client.table('health_checks').select('*').limit(1).execute()
    print(f"   ✅ Can read from health_checks table")
    print(f"   Found {len(response.data)} records")
except Exception as e:
    print(f"   ❌ Cannot read from table: {e}")

# Test 3: Try to insert test data
print("\n3. Testing data insert...")
test_data = {
    'sit_stand_movement_speed': 0.75,
    'sit_stand_stability': 0.80,
    'sit_stand_motion_smoothness': 0.70,
    'sit_stand_posture_deviation': 0.25,
    'sit_stand_micro_movements': 0.15,
    'sit_stand_range_of_motion': 0.65,
    'sit_stand_acceleration_variance': 0.30,
    'sit_stand_frame_count': 150,
    
    'walk_movement_speed': 0.70,
    'walk_stability': 0.75,
    'walk_motion_smoothness': 0.68,
    'walk_posture_deviation': 0.28,
    'walk_micro_movements': 0.18,
    'walk_range_of_motion': 0.62,
    'walk_acceleration_variance': 0.32,
    'walk_frame_count': 148,
    
    'steady_movement_speed': 0.15,
    'steady_stability': 0.85,
    'steady_motion_smoothness': 0.78,
    'steady_posture_deviation': 0.12,
    'steady_micro_movements': 0.10,
    'steady_range_of_motion': 0.20,
    'steady_acceleration_variance': 0.15,
    'steady_frame_count': 145,
    
    'avg_movement_speed': 0.53,
    'avg_stability': 0.80
}

# Use test user ID
test_user_id = "test_user_123"

print(f"   Attempting to save data for user: {test_user_id}")
result = save_health_check(test_user_id, test_data)

if result['success']:
    print(f"   ✅ {result['message']}")
    print(f"   Saved data: {result.get('data', {})}")
else:
    print(f"   ❌ {result['message']}")
    print(f"   This is likely due to Row Level Security (RLS) policies")
    print(f"   RLS requires auth.uid() to match user_id")

# Test 4: Check with default_user
print("\n4. Testing with 'default_user' (common fallback)...")
result2 = save_health_check("default_user", test_data)
if result2['success']:
    print(f"   ✅ {result2['message']}")
else:
    print(f"   ❌ {result2['message']}")

print("\n" + "=" * 60)
print("DIAGNOSIS:")
print("=" * 60)

if not result['success'] and not result2['success']:
    print("""
The data is NOT being saved because of Row Level Security (RLS) policies.

SOLUTION OPTIONS:

1. TEMPORARY FIX (for testing):
   Run this SQL in Supabase to allow inserts without auth:
   
   DROP POLICY IF EXISTS "Users can insert their own health checks" ON health_checks;
   
   CREATE POLICY "Users can insert their own health checks"
   ON health_checks FOR INSERT
   WITH CHECK (true);  -- Allows all inserts for testing

2. PROPER FIX (recommended):
   Make sure you're logged in with Supabase Auth:
   - Use the login page in your app
   - The user_id should match auth.uid()
   - Check st.session_state.user_id matches your auth user

3. CHECK YOUR AUTH:
   - Are you logged in via the app's authentication?
   - Is st.session_state.user_id set correctly?
   - Does it match a real Supabase auth user?
""")
else:
    print("\n✅ Data can be saved! The issue might be:")
    print("   - User not properly authenticated in the app")
    print("   - Session state user_id not set correctly")
    print("   - Check the app flow after login")

print("\n" + "=" * 60)
