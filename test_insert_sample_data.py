"""
Sample Data Insertion Script - For Testing AI Analysis
This script inserts sample health check data into Supabase for testing
"""

import os
from dotenv import load_dotenv
from datetime import date, timedelta, datetime
from supabase import create_client

# Load environment
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

def insert_sample_health_data(user_id: str):
    """Insert 7 days of sample health check data with gradual decline"""
    
    print(f"\n🔄 Inserting sample health data for user: {user_id}")
    
    # Generate 7 days of sample data with gradual decline in stability
    # Using actual column names from health_checks table
    sample_data = [
        {
            'day': 0,
            'sit_stand_movement_speed': 0.85,
            'sit_stand_stability': 0.92,
            'sit_stand_motion_smoothness': 0.88,
            'sit_stand_posture_deviation': 0.12,
            'sit_stand_micro_movements': 0.08,
            'walk_movement_speed': 0.78,
            'walk_stability': 0.89,
            'walk_motion_smoothness': 0.85,
            'walk_posture_deviation': 0.15,
            'walk_micro_movements': 0.10,
            'steady_movement_speed': 0.05,
            'steady_stability': 0.95,
            'steady_motion_smoothness': 0.92,
            'steady_posture_deviation': 0.08,
            'steady_micro_movements': 0.06,
            'avg_movement_speed': 0.56,
            'avg_stability': 0.92
        },
        {
            'day': 1,
            'sit_stand_movement_speed': 0.83,
            'sit_stand_stability': 0.90,
            'sit_stand_motion_smoothness': 0.86,
            'sit_stand_posture_deviation': 0.13,
            'sit_stand_micro_movements': 0.09,
            'walk_movement_speed': 0.76,
            'walk_stability': 0.87,
            'walk_motion_smoothness': 0.83,
            'walk_posture_deviation': 0.16,
            'walk_micro_movements': 0.11,
            'steady_movement_speed': 0.06,
            'steady_stability': 0.93,
            'steady_motion_smoothness': 0.90,
            'steady_posture_deviation': 0.09,
            'steady_micro_movements': 0.07,
            'avg_movement_speed': 0.55,
            'avg_stability': 0.90
        },
        {
            'day': 2,
            'sit_stand_movement_speed': 0.81,
            'sit_stand_stability': 0.88,
            'sit_stand_motion_smoothness': 0.84,
            'sit_stand_posture_deviation': 0.14,
            'sit_stand_micro_movements': 0.10,
            'walk_movement_speed': 0.74,
            'walk_stability': 0.85,
            'walk_motion_smoothness': 0.81,
            'walk_posture_deviation': 0.17,
            'walk_micro_movements': 0.12,
            'steady_movement_speed': 0.07,
            'steady_stability': 0.91,
            'steady_motion_smoothness': 0.88,
            'steady_posture_deviation': 0.10,
            'steady_micro_movements': 0.08,
            'avg_movement_speed': 0.54,
            'avg_stability': 0.88
        },
        {
            'day': 3,
            'sit_stand_movement_speed': 0.79,
            'sit_stand_stability': 0.86,
            'sit_stand_motion_smoothness': 0.82,
            'sit_stand_posture_deviation': 0.15,
            'sit_stand_micro_movements': 0.11,
            'walk_movement_speed': 0.72,
            'walk_stability': 0.83,
            'walk_motion_smoothness': 0.79,
            'walk_posture_deviation': 0.18,
            'walk_micro_movements': 0.13,
            'steady_movement_speed': 0.08,
            'steady_stability': 0.89,
            'steady_motion_smoothness': 0.86,
            'steady_posture_deviation': 0.11,
            'steady_micro_movements': 0.09,
            'avg_movement_speed': 0.53,
            'avg_stability': 0.86
        },
        {
            'day': 4,
            'sit_stand_movement_speed': 0.77,
            'sit_stand_stability': 0.84,
            'sit_stand_motion_smoothness': 0.80,
            'sit_stand_posture_deviation': 0.16,
            'sit_stand_micro_movements': 0.12,
            'walk_movement_speed': 0.70,
            'walk_stability': 0.81,
            'walk_motion_smoothness': 0.77,
            'walk_posture_deviation': 0.19,
            'walk_micro_movements': 0.14,
            'steady_movement_speed': 0.09,
            'steady_stability': 0.87,
            'steady_motion_smoothness': 0.84,
            'steady_posture_deviation': 0.12,
            'steady_micro_movements': 0.10,
            'avg_movement_speed': 0.52,
            'avg_stability': 0.84
        },
        {
            'day': 5,
            'sit_stand_movement_speed': 0.75,
            'sit_stand_stability': 0.82,
            'sit_stand_motion_smoothness': 0.78,
            'sit_stand_posture_deviation': 0.17,
            'sit_stand_micro_movements': 0.13,
            'walk_movement_speed': 0.68,
            'walk_stability': 0.79,
            'walk_motion_smoothness': 0.75,
            'walk_posture_deviation': 0.20,
            'walk_micro_movements': 0.15,
            'steady_movement_speed': 0.10,
            'steady_stability': 0.85,
            'steady_motion_smoothness': 0.82,
            'steady_posture_deviation': 0.13,
            'steady_micro_movements': 0.11,
            'avg_movement_speed': 0.51,
            'avg_stability': 0.82
        },
        {
            'day': 6,
            'sit_stand_movement_speed': 0.73,
            'sit_stand_stability': 0.80,
            'sit_stand_motion_smoothness': 0.76,
            'sit_stand_posture_deviation': 0.18,
            'sit_stand_micro_movements': 0.14,
            'walk_movement_speed': 0.66,
            'walk_stability': 0.77,
            'walk_motion_smoothness': 0.73,
            'walk_posture_deviation': 0.21,
            'walk_micro_movements': 0.16,
            'steady_movement_speed': 0.11,
            'steady_stability': 0.83,
            'steady_motion_smoothness': 0.80,
            'steady_posture_deviation': 0.14,
            'steady_micro_movements': 0.12,
            'avg_movement_speed': 0.50,
            'avg_stability': 0.80
        }
    ]
    
    # Connect to Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Insert each day's data
    success_count = 0
    for day_data in sample_data:
        day_offset = day_data.pop('day')
        check_date = (date.today() - timedelta(days=(6 - day_offset))).isoformat()
        
        # Build full record
        record = {
            'user_id': user_id,
            'check_date': check_date,
            'check_timestamp': datetime.now().isoformat(),
            **day_data
        }
        
        try:
            response = supabase.table('health_checks').upsert(
                record,
                on_conflict='user_id,check_date'
            ).execute()
            
            print(f"   ✅ Day {day_offset + 1} inserted: {check_date} (stability: {day_data['avg_stability']:.0%})")
            success_count += 1
        except Exception as e:
            print(f"   ❌ Day {day_offset + 1} failed: {str(e)}")
    
    print(f"\n🎉 Sample data insertion complete! ({success_count}/7 records inserted)")
    print("\n📊 Pattern inserted: Gradual 12% decline in stability over 7 days")
    print("   Day 1: 92% → Day 7: 80% stability")
    print("\nNow you can:")
    print("   1. Go to AI Health Chat page")
    print("   2. You should see: '✅ 7 health checks'")
    print("   3. Click 'Run Complete AI Analysis'")
    print("   4. See the 5-agent pipeline detect the drift pattern!")


if __name__ == "__main__":
    print("=" * 60)
    print("SAMPLE DATA INSERTION FOR AI TESTING")
    print("=" * 60)
    print("\n📝 This will insert 7 days of realistic health check data")
    print("   showing a gradual 12% decline in stability (92% → 80%)")
    print("\n⚠️  You need your user_id from Streamlit session state")
    print("   To find it: Open the app, check st.session_state['user_id']")
    print()
    
    user_id = input("Enter your user_id: ").strip()
    
    if not user_id:
        print("\n❌ User ID is required!")
        print("\n💡 To get your user_id:")
        print("   1. Run: python -m streamlit run app.py")
        print("   2. Open browser developer tools (F12)")
        print("   3. In Console, type: window.streamlit.session_state")
        print("   4. Find user_id value")
        exit(1)
    
    confirm = input(f"\n✅ Insert 7 days of sample data for '{user_id}'? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        insert_sample_health_data(user_id)
    else:
        print("\n❌ Operation cancelled")
