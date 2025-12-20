"""
Home Page - MediGuard Drift AI
Landing page that explains the system and its purpose
"""

import streamlit as st


def show():
    """
    Display the home page content
    """
    
    # ========================================
    # HERO SECTION
    # ========================================
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #4A90E2; font-size: 2.8rem; margin-bottom: 0.5rem;'>
                Welcome to MediGuard Drift AI
            </h1>
            <p style='font-size: 1.3rem; color: #666; margin-top: 0;'>
                Catch Small Changes Before They Become Big Problems
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # THE PROBLEM: HEALTH DRIFT
    # ========================================
    st.markdown("### 🔍 What is Health Drift?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Health drift** is the gradual, often unnoticed decline in your health metrics over time. 
        
        Think of it like this: You don't gain 20 pounds overnight. Your blood pressure doesn't 
        suddenly spike. These changes happen slowly—a pound here, a few points there—until one 
        day you realize there's a problem.
        
        **The Challenge:** By the time you notice symptoms, the issue may already be significant. 
        Traditional healthcare often catches problems only during annual checkups, missing the 
        subtle early warning signs.
        
        **Our Solution:** MediGuard Drift AI monitors your daily health data and uses advanced 
        AI to detect these small drifts early, giving you the power to take action before minor 
        changes become major concerns.
        """)
    
    with col2:
        st.info("""
        **Common Examples:**
        
        📉 Gradual weight gain
        
        💓 Slow BP increase
        
        😴 Declining sleep quality
        
        🎯 Activity level drop
        
        🍽️ Diet pattern shifts
        """)
    
    st.markdown("---")
    
    # ========================================
    # HOW IT WORKS
    # ========================================
    st.markdown("### ⚙️ How It Works")
    st.markdown("MediGuard Drift AI operates in four simple steps:")
    
    # Create 4 columns for the steps
    step1, step2, step3, step4 = st.columns(4)
    
    with step1:
        st.markdown("""
        <div style='background: #EFF6FB; padding: 1.5rem; border-radius: 10px; height: 100%; border: 1px solid #D1E7F5;'>
            <h3 style='color: #4A90E2; text-align: center;'>1️⃣</h3>
            <h4 style='text-align: center; color: #2C5F7F;'>Log Daily Data</h4>
            <p style='text-align: center; font-size: 0.9rem; color: #555;'>
                Enter your daily health metrics: weight, blood pressure, sleep, 
                activity, and how you feel.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with step2:
        st.markdown("""
        <div style='background: #F0F8F1; padding: 1.5rem; border-radius: 10px; height: 100%; border: 1px solid #D4ECD6;'>
            <h3 style='color: #50C878; text-align: center;'>2️⃣</h3>
            <h4 style='text-align: center; color: #2D6F3E;'>AI Analysis</h4>
            <p style='text-align: center; font-size: 0.9rem; color: #555;'>
                Our AI agent analyzes your data, comparing it to your baseline 
                and detecting subtle patterns.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with step3:
        st.markdown("""
        <div style='background: #FBF5ED; padding: 1.5rem; border-radius: 10px; height: 100%; border: 1px solid #F0E0C8;'>
            <h3 style='color: #E67E22; text-align: center;'>3️⃣</h3>
            <h4 style='text-align: center; color: #8B5A00;'>Get Insights</h4>
            <p style='text-align: center; font-size: 0.9rem; color: #555;'>
                Receive personalized alerts about drifts, trends, and 
                correlations in your health data.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with step4:
        st.markdown("""
        <div style='background: #F7F2F8; padding: 1.5rem; border-radius: 10px; height: 100%; border: 1px solid #E8D9ED;'>
            <h3 style='color: #9C27B0; text-align: center;'>4️⃣</h3>
            <h4 style='text-align: center; color: #6B1B7F;'>Take Action</h4>
            <p style='text-align: center; font-size: 0.9rem; color: #555;'>
                Use insights to make informed decisions and discuss 
                findings with your healthcare provider.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ========================================
    # WHAT MAKES US UNIQUE
    # ========================================
    st.markdown("### ✨ What Makes MediGuard Drift AI Unique?")
    
    # Create 3 columns for unique features
    unique1, unique2, unique3 = st.columns(3)
    
    with unique1:
        st.markdown("""
        #### 🛡️ Preventive-First Approach
        We don't wait for problems to happen. By monitoring daily changes and detecting 
        early drifts, we help you stay ahead of potential health issues.
        
        **Traditional:** Annual checkups catch problems after they develop  
        **MediGuard:** Daily monitoring prevents problems from developing
        """)
    
    with unique2:
        st.markdown("""
        #### 🤖 Agentic AI Intelligence
        Our AI doesn't just store data—it actively analyzes, learns your patterns, 
        and provides intelligent insights tailored to your unique health profile.
        
        **Traditional:** Generic health apps with basic tracking  
        **MediGuard:** Smart AI agent that understands YOUR health
        """)
    
    with unique3:
        st.markdown("""
        #### 👤 Hyper-Personalized
        Every person's health baseline is different. Our system learns what's normal 
        for YOU and alerts you when YOUR patterns change.
        
        **Traditional:** One-size-fits-all health recommendations  
        **MediGuard:** Personalized insights based on YOUR data
        """)
    
    st.markdown("---")
    
    # ========================================
    # CALL TO ACTION
    # ========================================
    st.markdown("### 🚀 Ready to Get Started?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4A90E2 0%, #50C878 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center;'>
            <h3 style='color: white; margin-bottom: 1rem;'>Begin Your Health Monitoring Journey</h3>
            <p style='color: #E8F4F8; margin-bottom: 1.5rem;'>
                Set up your profile and log your first daily health check to start 
                tracking your health drift today.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("📝 Complete Profile", use_container_width=True, type="primary"):
                st.session_state.current_page = "Profile"
                st.rerun()
        with btn_col2:
            if st.button("📋 Log Health Data", use_container_width=True):
                st.session_state.current_page = "Daily Health Check"
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # IMPORTANT DISCLAIMER
    # ========================================
    st.warning("""
    ⚠️ **Important Medical Disclaimer**
    
    MediGuard Drift AI is a health monitoring and tracking tool designed to help you observe 
    patterns in your personal health data. **This system is NOT a medical diagnostic tool** 
    and does not provide medical advice, diagnosis, or treatment recommendations.
    
    **Please Note:**
    - All insights provided are for informational purposes only
    - This tool does not replace professional medical advice
    - Always consult with qualified healthcare professionals for medical concerns
    - In case of emergency, contact your local emergency services immediately
    - Do not use this system to self-diagnose or delay seeking medical attention
    
    By using MediGuard Drift AI, you acknowledge that you understand these limitations and 
    will seek appropriate medical care when needed.
    """)
    
    st.markdown("---")
    
    # ========================================
    # FOOTER
    # ========================================
    st.markdown("""
        <div style='text-align: center; color: #999; font-size: 0.85rem; padding: 1rem;'>
            <p>💙 Your health is your most valuable asset. Let's protect it together.</p>
        </div>
    """, unsafe_allow_html=True)
