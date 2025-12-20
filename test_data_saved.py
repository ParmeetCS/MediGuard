"""
Check if health check data exists in Supabase
Run this AFTER completing a daily health check
"""
import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime, timedelta

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

print("=" * 60)
print("CHECKING FOR HEALTH CHECK DATA")
print("=" * 60)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Check total records
print("\n1. Checking total records in health_checks table...")
try:
    response = supabase.table('health_checks').select('*', count='exact').execute()
    total_count = response.count
    print(f"   📊 Total records: {total_count}")
    
    if total_count == 0:
        print("\n   ⚠️ NO DATA FOUND")
        print("   This means no daily health checks have been completed yet.")
        print("\n   💡 TO FIX:")
        print("      1. Run: python -m streamlit run app.py")
        print("      2. Go to '🩺 Daily Health Check' page")
        print("      3. Complete all 3 activities")
        print("      4. Data will be auto-saved")
        print("\n   OR run: python test_insert_sample_data.py")
        print("      To insert sample data for testing")
    else:
        print("   ✅ Data exists!")
        
        # Show recent records
        print("\n2. Recent health check records:")
        recent = supabase.table('health_checks')\
            .select('*')\
            .order('check_date', desc=True)\
            .limit(5)\
            .execute()
        
        for idx, record in enumerate(recent.data, 1):
            print(f"\n   Record #{idx}:")
            print(f"      Date: {record.get('check_date')}")
            print(f"      User: {record.get('user_id', 'unknown')[:20]}...")
            print(f"      Avg Movement Speed: {record.get('avg_movement_speed', 'N/A')}")
            print(f"      Avg Stability: {record.get('avg_stability', 'N/A')}")
        
        print("\n   ✅ AI Health Chat should now work!")
        print("      Go to AI Health Chat page to run analysis.")

except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("CHECK COMPLETE")
print("=" * 60)
