"""
Profile Page - MediGuard Drift AI
User context collection page for personalized health monitoring
"""

import streamlit as st


def show():
    """
    Display the profile page for collecting user context
    """
    
    # ========================================
    # PAGE HEADER
    # ========================================
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: #4A90E2; font-size: 2.5rem;'>👤 Your Profile</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Help us understand you better for personalized health insights
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # WHY WE NEED THIS DATA
    # ========================================
    st.info("""
    **📋 Why do we collect this information?**
    
    Your profile helps our AI provide personalized health insights tailored to YOUR lifestyle:
    - **Name**: Personalize your experience
    - **Age**: Age-appropriate health baselines and recommendations
    - **Lifestyle**: Context for activity levels, stress patterns, and health expectations
    - **Notes**: Any relevant context that helps us better understand your health journey
    
    💡 *This data is stored locally in your session and helps make your health monitoring more relevant and accurate.*
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # INITIALIZE SESSION STATE
    # ========================================
    # Initialize profile fields in session state if they don't exist
    if 'profile_name' not in st.session_state:
        st.session_state.profile_name = ""
    if 'profile_age' not in st.session_state:
        st.session_state.profile_age = 25
    if 'profile_lifestyle' not in st.session_state:
        st.session_state.profile_lifestyle = "Working Professional"
    if 'profile_notes' not in st.session_state:
        st.session_state.profile_notes = ""
    if 'profile_saved' not in st.session_state:
        st.session_state.profile_saved = False
    
    # ========================================
    # PROFILE FORM
    # ========================================
    st.markdown("### 📝 Basic Information")
    
    # Create a form-like layout with better spacing
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Name input
        st.markdown("#### Your Name")
        name = st.text_input(
            "Enter your full name or preferred name",
            value=st.session_state.profile_name,
            placeholder="e.g., John Doe",
            help="This is how we'll address you throughout the app",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Lifestyle dropdown
        st.markdown("#### Lifestyle")
        lifestyle = st.selectbox(
            "Select the option that best describes your current lifestyle",
            options=[
                "Student",
                "Working Professional",
                "Active/Athlete",
                "Retired",
                "Stay-at-home Parent",
                "Other"
            ],
            index=["Student", "Working Professional", "Active/Athlete", "Retired", 
                   "Stay-at-home Parent", "Other"].index(st.session_state.profile_lifestyle)
            if st.session_state.profile_lifestyle in ["Student", "Working Professional", 
                                                       "Active/Athlete", "Retired", 
                                                       "Stay-at-home Parent", "Other"]
            else 1,
            help="Your lifestyle helps us understand your daily routines and activity patterns",
            label_visibility="collapsed"
        )
        
        st.markdown("""
            <p style='font-size: 0.85rem; color: #666; margin-top: 0.5rem;'>
                💡 This helps us set appropriate activity and health expectations
            </p>
        """, unsafe_allow_html=True)
    
    with col2:
        # Age input
        st.markdown("#### Age")
        age = st.number_input(
            "Enter your age in years",
            min_value=1,
            max_value=120,
            value=st.session_state.profile_age,
            step=1,
            help="Used for age-appropriate health baselines and recommendations",
            label_visibility="collapsed"
        )
        
        st.markdown("""
            <p style='font-size: 0.85rem; color: #666; margin-top: 0.5rem;'>
                🎂 Age helps establish appropriate health baselines
            </p>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # OPTIONAL NOTES SECTION
    # ========================================
    st.markdown("### 📌 Additional Context (Optional)")
    
    notes = st.text_area(
        "Share any relevant information that might help us provide better insights",
        value=st.session_state.profile_notes,
        height=150,
        placeholder="Examples:\n- Existing health conditions you're monitoring\n- Fitness goals you're working towards\n- Lifestyle changes you're planning\n- Any other context that might be relevant\n\nNote: This is NOT for sensitive medical data.",
        help="Optional field for any additional context",
        label_visibility="collapsed"
    )
    
    st.markdown("""
        <p style='font-size: 0.85rem; color: #666; font-style: italic;'>
            💡 Tip: The more context you provide, the better our AI can personalize insights. 
            However, avoid sharing sensitive medical information or personal health records.
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # SAVE BUTTON
    # ========================================
    st.markdown("### 💾 Save Your Profile")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        save_button = st.button(
            "💾 Save Profile",
            type="primary",
            use_container_width=True
        )
    
    # Handle save action
    if save_button:
        # Validate required fields
        if not name.strip():
            st.error("❌ Please enter your name before saving.")
        else:
            # Save to session state
            st.session_state.profile_name = name
            st.session_state.profile_age = age
            st.session_state.profile_lifestyle = lifestyle
            st.session_state.profile_notes = notes
            st.session_state.profile_saved = True
            
            # Show success message
            st.success("✅ Profile saved successfully!")
            st.balloons()
            
            # Show summary
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📋 Profile Summary")
            
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.markdown(f"""
                    <div style='background: #E3F2FD; padding: 1rem; border-radius: 8px;'>
                        <p style='margin: 0;'><strong>Name:</strong> {name}</p>
                        <p style='margin: 0.5rem 0 0 0;'><strong>Age:</strong> {age} years</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with summary_col2:
                st.markdown(f"""
                    <div style='background: #E8F5E9; padding: 1rem; border-radius: 8px;'>
                        <p style='margin: 0;'><strong>Lifestyle:</strong> {lifestyle}</p>
                        <p style='margin: 0.5rem 0 0 0;'><strong>Notes:</strong> {len(notes)} characters</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Next steps
            st.info("""
            **🎯 What's Next?**
            
            Your profile is set up! Now you can:
            1. 📋 **Log your first daily health check** to start tracking
            2. 📊 **View your dashboard** once you have some data
            3. 💬 **Chat with our AI assistant** for personalized insights
            """)
            
            # Quick action button
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("📋 Start Health Check", use_container_width=True):
                    st.session_state.current_page = "Daily Health Check"
                    st.rerun()
    
    # ========================================
    # SHOW CURRENT PROFILE IF SAVED
    # ========================================
    if st.session_state.profile_saved and not save_button:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### ✅ Current Profile")
        
        profile_col1, profile_col2 = st.columns(2)
        
        with profile_col1:
            st.markdown(f"""
                <div style='background: #F0F7FF; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #4A90E2;'>
                    <h4 style='margin-top: 0; color: #4A90E2;'>Basic Info</h4>
                    <p><strong>👤 Name:</strong> {st.session_state.profile_name}</p>
                    <p><strong>🎂 Age:</strong> {st.session_state.profile_age} years</p>
                    <p><strong>💼 Lifestyle:</strong> {st.session_state.profile_lifestyle}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with profile_col2:
            st.markdown(f"""
                <div style='background: #F0F7FF; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #50C878;'>
                    <h4 style='margin-top: 0; color: #50C878;'>Additional Notes</h4>
                    <p style='font-style: italic; color: #666;'>
                        {st.session_state.profile_notes if st.session_state.profile_notes 
                         else "No additional notes provided."}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <p style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 1rem;'>
                💡 You can update your profile anytime by changing the fields above and clicking Save Profile.
            </p>
        """, unsafe_allow_html=True)
    
    # ========================================
    # DATA PRIVACY NOTE
    # ========================================
    st.markdown("---")
    st.markdown("""
        <div style='background: #FFF9E6; padding: 1rem; border-radius: 8px; border-left: 4px solid #FFC107;'>
            <p style='margin: 0; font-size: 0.9rem;'>
                🔒 <strong>Privacy Note:</strong> Your profile data is currently stored in your session 
                and will be cleared when you close the app. Future versions will include secure 
                storage options to persist your data across sessions.
            </p>
        </div>
    """, unsafe_allow_html=True)
