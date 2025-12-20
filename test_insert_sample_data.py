"""
Sample Data Insertion Script - For Testing AI Analysis
This script inserts sample health check data into Supabase for testing
"""

import os
from dotenv import load_dotenv
from datetime import date, timedelta
from storage.health_repository import save_health_check

# Load environment
load_dotenv()

def insert_sample_health_data(user_id: str):
    """Insert 7 days of sample health check data with gradual decline"""
    
    print(f"Inserting sample health data for user: {user_id}")
    
    # Generate 7 days of sample data with gradual decline in stability
    sample_data = [
        {
            'day': 0,
            'sit_stand_speed': 2.5,
            'sit_stand_stability': 92.0,
            'walk_speed': 1.2,
            'walk_stability': 88.5,
            'gait_symmetry': 85.0,
            'hand_steadiness': 90.0,
            'tremor_index': 5.0,
            'coordination_score': 87.0,
            'overall_mobility': 88.0
        },
        {
            'day': 1,
            'sit_stand_speed': 2.6,
            'sit_stand_stability': 90.5,
            'walk_speed': 1.18,
            'walk_stability': 87.0,
            'gait_symmetry': 84.5,
            'hand_steadiness': 89.5,
            'tremor_index': 5.5,
            'coordination_score': 86.5,
            'overall_mobility': 87.0
        },
        {
            'day': 2,
            'sit_stand_speed': 2.7,
            'sit_stand_stability': 89.0,
            'walk_speed': 1.15,
            'walk_stability': 86.0,
            'gait_symmetry': 83.5,
            'hand_steadiness': 89.0,
            'tremor_index': 6.0,
            'coordination_score': 85.5,
            'overall_mobility': 86.0
        },
        {
            'day': 3,
            'sit_stand_speed': 2.8,
            'sit_stand_stability': 87.5,
            'walk_speed': 1.12,
            'walk_stability': 85.0,
            'gait_symmetry': 83.0,
            'hand_steadiness': 88.5,
            'tremor_index': 6.5,
            'coordination_score': 85.0,
            'overall_mobility': 85.0
        },
        {
            'day': 4,
            'sit_stand_speed': 2.9,
            'sit_stand_stability': 86.0,
            'walk_speed': 1.10,
            'walk_stability': 84.0,
            'gait_symmetry': 82.5,
            'hand_steadiness': 88.0,
            'tremor_index': 7.0,
            'coordination_score': 84.0,
            'overall_mobility': 84.0
        },
        {
            'day': 5,
            'sit_stand_speed': 3.0,
            'sit_stand_stability': 85.0,
            'walk_speed': 1.08,
            'walk_stability': 83.5,
            'gait_symmetry': 82.0,
            'hand_steadiness': 87.5,
            'tremor_index': 7.5,
            'coordination_score': 83.5,
            'overall_mobility': 83.5
        },
        {
            'day': 6,
            'sit_stand_speed': 3.1,
            'sit_stand_stability': 84.0,
            'walk_speed': 1.05,
            'walk_stability': 83.0,
            'gait_symmetry': 81.5,
            'hand_steadiness': 87.0,
            'tremor_index': 8.0,
            'coordination_score': 83.0,
            'overall_mobility': 83.0
        }
    ]
    
    # Insert each day's data
    for day_data in sample_data:
        day_offset = day_data.pop('day')
        check_date = date.today() - timedelta(days=(6 - day_offset))
        
        result = save_health_check(
            user_id=user_id,
            health_data=day_data,
            check_date=check_date
        )
        
        if result['success']:
            print(f"✅ Day {day_offset + 1} inserted: {check_date}")
        else:
            print(f"❌ Day {day_offset + 1} failed: {result['message']}")
    
    print("\n🎉 Sample data insertion complete!")
    print("Now you can:")
    print("1. Go to AI Health Chat")
    print("2. Click 'Run AI Health Analysis'")
    print("3. See the AI analyze the gradual 8% decline in stability")


if __name__ == "__main__":
    import streamlit as st
    
    # Get user_id from Streamlit session or prompt
    print("=" * 60)
    print("SAMPLE DATA INSERTION FOR AI TESTING")
    print("=" * 60)
    print()
    
    user_id = input("Enter your user_id (from st.session_state['user_id']): ").strip()
    
    if not user_id:
        print("❌ User ID is required!")
        exit(1)
    
    confirm = input(f"Insert 7 days of sample data for '{user_id}'? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        insert_sample_health_data(user_id)
    else:
        print("❌ Operation cancelled")
