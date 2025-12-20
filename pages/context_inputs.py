"""
Context Inputs Page - MediGuard Drift AI
Page for collecting additional user context and health information
"""

import streamlit as st
from auth.supabase_auth import get_supabase_client
from datetime import datetime


def save_context_to_supabase(user_id: str, context_data: dict) -> tuple[bool, str]:
    """
    Save user context data to Supabase
    
    Args:
        user_id (str): User's unique ID
        context_data (dict): Context data to save
    
    Returns:
        tuple: (success, message)
    """
    try:
        supabase = get_supabase_client()
        
        if not supabase:
            return False, "Database connection not configured."
        
        # Prepare data for insertion
        data = {
            "user_id": user_id,
            "medical_summary": context_data.get('medical_summary', ''),
            "known_conditions": context_data.get('known_conditions', ''),
            "report_summary": context_data.get('report_summary', ''),
            "sleep_hours": context_data.get('sleep_hours', 7),
            "stress_level": context_data.get('stress_level', 'Medium'),
            "workload": context_data.get('workload', 'Moderate'),
            "activity_level": context_data.get('activity_level', 'Moderate'),
            "created_at": datetime.now().isoformat()
        }
        
        # Insert or update context data
        response = supabase.table('user_context_data').upsert(data, on_conflict='user_id').execute()
        
        return True, "Context data saved successfully!"
        
    except Exception as e:
        return False, f"Error saving data: {str(e)}"


def load_existing_context(user_id: str) -> dict:
    """
    Load existing context data for a user from Supabase
    
    Args:
        user_id (str): User's unique ID
    
    Returns:
        dict: Existing context data or empty dict if none found
    """
    try:
        supabase = get_supabase_client()
        
        if not supabase:
            return {}
        
        response = supabase.table('user_context_data').select('*').eq('user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            data = response.data[0]
            return {
                'medical_summary': data.get('medical_summary', ''),
                'known_conditions': data.get('known_conditions', ''),
                'report_summary': data.get('report_summary', ''),
                'sleep_hours': data.get('sleep_hours', 7.0),
                'stress_level': data.get('stress_level', 'Medium'),
                'workload': data.get('workload', 'Moderate'),
                'activity_level': data.get('activity_level', 'Moderate'),
                'created_at': data.get('created_at')
            }
        return {}
        
    except Exception as e:
        st.error(f"Error loading existing data: {str(e)}")
        return {}


def show():
    """
    Display the context inputs page
    """
    
    # ========================================
    # PAGE HEADER
    # ========================================
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: #4A90E2; font-size: 2.5rem;'>📝 Health Context</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Provide additional context for personalized health insights
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # LOAD EXISTING DATA
    # ========================================
    user_id = st.session_state.get('user_id')
    
    if not user_id:
        st.error("❌ User not authenticated. Please log in.")
        return
    
    existing_data = load_existing_context(user_id)
    
    # Show existing data summary if available
    if existing_data and existing_data.get('medical_summary'):
        with st.expander("📄 **Your Current Context Data** (Click to view)", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🏥 Medical Information:**")
                if existing_data.get('medical_summary'):
                    st.write(f"Medical History: {existing_data['medical_summary'][:100]}...")
                if existing_data.get('known_conditions'):
                    st.write(f"Known Conditions: {existing_data['known_conditions'][:100]}...")
                if existing_data.get('report_summary'):
                    st.write(f"Recent Reports: {existing_data['report_summary'][:100]}...")
            
            with col2:
                st.markdown("**🌟 Lifestyle Factors:**")
                st.write(f"Sleep Hours: {existing_data.get('sleep_hours', 7)} hours/night")
                st.write(f"Stress Level: {existing_data.get('stress_level', 'medium').title()}")
                st.write(f"Workload: {existing_data.get('workload', 'moderate').title()}")
                st.write(f"Activity Level: {existing_data.get('activity_level', 'moderate').title()}")
            
            if existing_data.get('updated_at'):
                st.caption(f"Last updated: {existing_data['updated_at']}")
        
        st.info("💡 **Tip:** Fill in the form below to update your context information.")
    
    # ========================================
    # PRIVACY NOTICE
    # ========================================
    st.info("""
    🔒 **Privacy Notice**
    
    The information you provide here helps our AI provide more personalized insights. 
    All data is encrypted and stored securely. You can update or delete this information 
    anytime. This data is for monitoring purposes only—not for diagnosis or treatment.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # CONTEXT INPUT FORM
    # ========================================
    st.markdown("### 📋 Health & Lifestyle Context")
    
    with st.form("context_form", clear_on_submit=False):
        
        # Medical History Section
        st.markdown("#### 🏥 Medical Background")
        st.caption("Provide a brief summary to help contextualize your health patterns")
        
        medical_summary = st.text_area(
            "Medical Summary",
            value=existing_data.get('medical_summary', ''),
            placeholder="Brief summary of relevant medical history...",
            height=100,
            help="Optional: General medical background that might be relevant to health monitoring"
        )
        
        known_conditions = st.text_area(
            "Known Conditions",
            value=existing_data.get('known_conditions', ''),
            placeholder="Any conditions you're currently managing or monitoring...",
            height=80,
            help="Optional: Conditions you're aware of"
        )
        
        report_summary = st.text_area(
            "Report Summary",
            value=existing_data.get('report_summary', ''),
            placeholder="Summary of recent checkups or test results...",
            height=100,
            help="Optional: Brief notes from recent visits or test results"
        )
        
        st.markdown("---")
        
        # Lifestyle Factors Section
        st.markdown("#### 🌟 Daily Lifestyle Factors")
        st.caption("These factors help us understand patterns in your health data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sleep_hours = st.number_input(
                "Average Sleep Hours per Night",
                min_value=0.0,
                max_value=12.0,
                value=float(existing_data.get('sleep_hours', 7.0)),
                step=0.5,
                help="Typical number of hours you sleep each night"
            )
            
            # Get stress level index
            stress_options = ["Low", "Medium", "High"]
            current_stress = existing_data.get('stress_level', 'Medium')
            stress_index = stress_options.index(current_stress) if current_stress in stress_options else 1
            
            stress_level = st.selectbox(
                "Stress Level",
                options=stress_options,
                index=stress_index,
                help="Your general stress level over the past week"
            )
            
        with col2:
            # Get workload index
            workload_options = ["Light", "Moderate", "Heavy"]
            current_workload = existing_data.get('workload', 'Moderate')
            workload_index = workload_options.index(current_workload) if current_workload in workload_options else 1
            
            workload = st.selectbox(
                "Workload",
                options=workload_options,
                index=workload_index,
                help="How demanding is your current work or study schedule?"
            )
            
            # Get activity level index
            activity_options = ["Sedentary", "Moderate", "Active"]
            current_activity = existing_data.get('activity_level', 'Moderate')
            activity_index = activity_options.index(current_activity) if current_activity in activity_options else 1
            
            activity_level = st.selectbox(
                "Activity Level",
                options=activity_options,
                index=activity_index,
                help="Your typical level of physical activity throughout the day"
            )
        
        st.markdown("---")
        
        # Submit Button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button(
                "💾 Save / Update",
                type="primary",
                use_container_width=True
            )
        
        # Handle form submission
        if submit_button:
            # Get user ID from session state
            user_id = st.session_state.get('user_id')
            
            if not user_id:
                st.error("❌ User not authenticated. Please log in again.")
            else:
                # Prepare context data
                context_data = {
                    'medical_summary': medical_summary,
                    'known_conditions': known_conditions,
                    'report_summary': report_summary,
                    'sleep_hours': sleep_hours,
                    'stress_level': stress_level,
                    'workload': workload,
                    'activity_level': activity_level
                }
                
                # Save to Supabase
                with st.spinner("Saving your context data..."):
                    success, message = save_context_to_supabase(user_id, context_data)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
    
    st.markdown("---")
    
    # ========================================
    # INFORMATION SECTION
    # ========================================
    st.markdown("### 💡 Why We Collect This Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Personalization**
        
        Your context helps our AI understand YOUR unique health baseline 
        and provide insights tailored to your specific situation.
        """)
    
    with col2:
        st.markdown("""
        **📊 Better Analysis**
        
        Lifestyle factors like sleep and stress significantly affect health metrics. 
        This context improves drift detection accuracy.
        """)
    
    with col3:
        st.markdown("""
        **🔐 Your Control**
        
        You own this data. Update it anytime, and it stays private and encrypted. 
        We never share without your explicit permission.
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # IMPORTANT REMINDERS
    # ========================================
    st.warning("""
    ⚠️ **Important Reminders**
    
    - This information is for health monitoring context only
    - Do NOT use this as a replacement for medical records or consultations
    - Always discuss health concerns with qualified healthcare professionals
    - We do not store or analyze actual medical documents—only your summaries
    - This data helps AI provide insights but does NOT diagnose conditions
    """)
    
    st.markdown("---")
    
    # ========================================
    # DATA MANAGEMENT
    # ========================================
    st.markdown("### ⚙️ Manage Your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Update Context", use_container_width=True):
            st.info("Fill in the form above with updated information and click 'Save Context'")
    
    with col2:
        if st.button("🗑️ Clear All Context", use_container_width=True, type="secondary"):
            st.warning("This feature will be available soon. Contact support if you need to delete your data.")
