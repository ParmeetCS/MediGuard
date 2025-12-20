"""
Test Data Generator - Add Sample Health Checks
Creates sample health check data to test AI analysis
"""

import streamlit as st
from datetime import date, timedelta
from storage.health_repository import save_health_check


def generate_sample_data_page():
    """Streamlit page to generate sample health data"""
    
    st.markdown("## 🧪 Generate Sample Health Data")
    st.markdown("---")
    
    st.info("""
    **For Testing AI Analysis**
    
    This tool generates 7 days of sample health check data with a gradual decline pattern.
    Use this to test the AI analysis without completing actual health checks.
    """)
    
    user_id = st.session_state.get('user_id')
    
    if not user_id:
        st.error("❌ You must be logged in to generate sample data")
        return
    
    st.markdown(f"**User ID:** `{user_id}`")
    
    st.markdown("### Sample Data Pattern")
    st.markdown("""
    - **Day 1-7**: Gradual 8% decline in stability
    - **Overall mobility**: 88% → 83% (declining trend)
    - **Hand steadiness**: 90% → 87% (mild decline)
    - **Walking stability**: 88.5% → 83% (declining)
    
    This pattern will trigger:
    - Moderate severity drift detection
    - Context analysis based on your lifestyle data
    - Risk assessment showing consistent downward trend
    - Care recommendations
    """)
    
    st.markdown("---")
    
    if st.button("🚀 Generate Sample Data", type="primary", use_container_width=True):
        with st.spinner("Generating 7 days of sample health checks..."):
            # Sample data with gradual decline
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
            
            success_count = 0
            errors = []
            
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
                    success_count += 1
                else:
                    errors.append(f"Day {day_offset + 1}: {result['message']}")
            
            if success_count == 7:
                st.success(f"""
                ✅ **Sample Data Generated Successfully!**
                
                Inserted 7 days of health check data ({date.today() - timedelta(days=6)} to {date.today()})
                """)
                
                st.balloons()
                
                st.info("""
                **Next Steps:**
                1. Go to **Dashboard** to see trend charts
                2. Go to **AI Health Chat** and click "Run AI Health Analysis"
                3. The AI will analyze the gradual decline pattern using your lifestyle context
                """)
            else:
                st.warning(f"⚠️ Inserted {success_count}/7 records")
                if errors:
                    with st.expander("View Errors"):
                        for error in errors:
                            st.error(error)


if __name__ == "__main__":
    generate_sample_data_page()
