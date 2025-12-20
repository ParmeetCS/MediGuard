"""
Daily Health Check Page - MediGuard Drift AI
Camera-based daily health assessment with movement analysis
"""

import streamlit as st
import time
import random


def show():
    """
    Display the daily health check page with camera-based assessment
    """
    
    # ========================================
    # PAGE HEADER
    # ========================================
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: #4A90E2; font-size: 2.5rem;'>📋 Daily Health Check</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Quick 2-minute camera-based movement assessment
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # INITIALIZE SESSION STATE
    # ========================================
    if 'check_started' not in st.session_state:
        st.session_state.check_started = False
    if 'check_completed' not in st.session_state:
        st.session_state.check_completed = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    
    # ========================================
    # INTRODUCTION & INSTRUCTIONS
    # ========================================
    if not st.session_state.check_started:
        st.markdown("### 👋 Welcome to Your Daily Health Check")
        
        st.info("""
        **What is this?**
        
        This quick assessment uses your camera to observe simple movements and extract 
        health-related metrics. No wearables needed—just you and your camera!
        
        💡 **Privacy Note:** All processing happens in your browser. No video is stored or transmitted.
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========================================
        # WHAT WE'LL MEASURE
        # ========================================
        st.markdown("### 📊 What We'll Measure")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: #E3F2FD; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                <h3 style='color: #4A90E2; margin: 0;'>🏃</h3>
                <h4>Movement Speed</h4>
                <p style='font-size: 0.9rem; color: #666;'>
                    How quickly you move during simple actions
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #E8F5E9; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                <h3 style='color: #50C878; margin: 0;'>⚖️</h3>
                <h4>Stability</h4>
                <p style='font-size: 0.9rem; color: #666;'>
                    Balance and steadiness during movements
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: #FFF3E0; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                <h3 style='color: #FF9800; margin: 0;'>🎯</h3>
                <h4>Coordination</h4>
                <p style='font-size: 0.9rem; color: #666;'>
                    Smoothness and control of movements
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        
        # ========================================
        # INSTRUCTIONS FOR ACTIONS
        # ========================================
        st.markdown("### 📝 What You'll Do (2 minutes)")
        
        st.markdown("""
        We'll guide you through three simple actions. Make sure you have:
        - ✅ Enough space to stand and move (about 3 feet)
        - ✅ Good lighting
        - ✅ Camera positioned to see your full body or upper body
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Action cards
        action1, action2, action3 = st.columns(3)
        
        with action1:
            st.markdown("""
            <div style='background: #F0F7FF; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #4A90E2;'>
                <h4 style='color: #4A90E2; margin-top: 0;'>1️⃣ Sit-Stand Test</h4>
                <p style='font-size: 0.9rem;'>
                    <strong>Duration:</strong> 30 seconds<br>
                    <strong>Action:</strong> Stand up from a chair and sit back down, repeat 5 times<br>
                    <strong>Measures:</strong> Lower body strength, movement speed
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with action2:
            st.markdown("""
            <div style='background: #F0F7FF; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #50C878;'>
                <h4 style='color: #50C878; margin-top: 0;'>2️⃣ Short Walk</h4>
                <p style='font-size: 0.9rem;'>
                    <strong>Duration:</strong> 45 seconds<br>
                    <strong>Action:</strong> Walk normally for a few steps, turn around, walk back<br>
                    <strong>Measures:</strong> Gait pattern, balance, coordination
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with action3:
            st.markdown("""
            <div style='background: #F0F7FF; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FF9800;'>
                <h4 style='color: #FF9800; margin-top: 0;'>3️⃣ Steady Hands</h4>
                <p style='font-size: 0.9rem;'>
                    <strong>Duration:</strong> 30 seconds<br>
                    <strong>Action:</strong> Hold your hands steady in front of you<br>
                    <strong>Measures:</strong> Fine motor control, tremor detection
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========================================
        # START BUTTON
        # ========================================
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("🎥 Start Daily Health Check", type="primary", use_container_width=True):
                st.session_state.check_started = True
                st.session_state.check_completed = False
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========================================
        # TIPS
        # ========================================
        st.markdown("---")
        st.markdown("### 💡 Quick Tips")
        
        tip_col1, tip_col2 = st.columns(2)
        
        with tip_col1:
            st.markdown("""
            **✅ Do:**
            - Wear comfortable clothing
            - Ensure camera can see you clearly
            - Move at your natural, comfortable pace
            - Relax and be yourself
            """)
        
        with tip_col2:
            st.markdown("""
            **❌ Don't:**
            - Rush through the movements
            - Try to perform "perfectly"
            - Worry if you need to pause
            - Do anything that causes discomfort
            """)
    
    # ========================================
    # CHECK IN PROGRESS
    # ========================================
    elif st.session_state.check_started and not st.session_state.check_completed:
        st.markdown("### 🎥 Camera Assessment in Progress")
        
        # ========================================
        # CAMERA PLACEHOLDER
        # ========================================
        st.markdown("""
        <div style='background: #1a1a1a; padding: 3rem; border-radius: 15px; text-align: center; 
                    border: 3px dashed #4A90E2; margin: 2rem 0;'>
            <h2 style='color: white; margin: 0;'>📷</h2>
            <h3 style='color: #4A90E2; margin: 1rem 0;'>Webcam Feed</h3>
            <p style='color: #999; margin: 0;'>
                Camera placeholder - In production, live webcam feed would appear here
            </p>
            <p style='color: #666; font-size: 0.9rem; margin-top: 1rem;'>
                🟢 Camera Active | Processing Movement Data
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # ========================================
        # SIMULATED ANALYSIS PROCESS
        # ========================================
        st.markdown("### 🔄 Analysis Steps")
        
        # Create progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            ("🏃 Analyzing Sit-Stand Movement...", 0.15),
            ("📊 Extracting movement speed metrics...", 0.30),
            ("🚶 Analyzing Walking Pattern...", 0.50),
            ("⚖️ Calculating stability scores...", 0.65),
            ("✋ Analyzing Hand Steadiness...", 0.80),
            ("🎯 Computing coordination metrics...", 0.90),
            ("✅ Finalizing Analysis...", 1.0)
        ]
        
        for step_text, progress_value in steps:
            status_text.markdown(f"**{step_text}**")
            progress_bar.progress(progress_value)
            time.sleep(0.8)  # Simulate processing time
        
        status_text.markdown("**✅ Analysis Complete!**")
        time.sleep(0.5)
        
        # ========================================
        # GENERATE SIMULATED RESULTS
        # ========================================
        # Generate realistic dummy values with some variation
        st.session_state.analysis_results = {
            'sit_stand_speed': round(random.uniform(1.8, 3.5), 2),  # seconds per rep
            'sit_stand_stability': round(random.uniform(75, 95), 1),  # percentage
            'walk_speed': round(random.uniform(0.9, 1.4), 2),  # meters per second
            'walk_stability': round(random.uniform(70, 92), 1),  # percentage
            'gait_symmetry': round(random.uniform(80, 98), 1),  # percentage
            'hand_steadiness': round(random.uniform(82, 96), 1),  # percentage
            'tremor_index': round(random.uniform(0.2, 1.5), 2),  # lower is better
            'coordination_score': round(random.uniform(75, 95), 1),  # percentage
            'overall_mobility': round(random.uniform(78, 94), 1)  # percentage
        }
        
        st.session_state.check_completed = True
        time.sleep(0.5)
        st.rerun()
    
    # ========================================
    # RESULTS DISPLAY
    # ========================================
    elif st.session_state.check_completed:
        st.success("✅ Daily Health Check Complete!")
        
        st.markdown("### 📊 Your Movement Analysis Results")
        
        results = st.session_state.analysis_results
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========================================
        # OVERALL SCORE
        # ========================================
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            overall_score = results['overall_mobility']
            score_color = "#50C878" if overall_score >= 85 else "#FF9800" if overall_score >= 70 else "#E74C3C"
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4A90E2 0%, #50C878 100%); 
                        padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;'>
                <h3 style='color: white; margin: 0;'>Overall Mobility Score</h3>
                <h1 style='color: white; font-size: 4rem; margin: 1rem 0;'>{overall_score}%</h1>
                <p style='color: #E8F4F8; margin: 0;'>Based on today's movement assessment</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ========================================
        # DETAILED METRICS
        # ========================================
        st.markdown("### 📈 Detailed Movement Metrics")
        
        # Sit-Stand Metrics
        st.markdown("#### 🪑 Sit-Stand Assessment")
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric(
                label="Average Speed per Repetition",
                value=f"{results['sit_stand_speed']} seconds",
                delta="-0.3s from last week" if random.random() > 0.5 else "+0.2s from last week",
                delta_color="inverse"
            )
        
        with metric_col2:
            st.metric(
                label="Stability Score",
                value=f"{results['sit_stand_stability']}%",
                delta="+2.1% from last week" if random.random() > 0.5 else "-1.5% from last week"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Walking Metrics
        st.markdown("#### 🚶 Walking Assessment")
        walk_col1, walk_col2, walk_col3 = st.columns(3)
        
        with walk_col1:
            st.metric(
                label="Walking Speed",
                value=f"{results['walk_speed']} m/s",
                delta="+0.1 m/s" if random.random() > 0.5 else "-0.05 m/s"
            )
        
        with walk_col2:
            st.metric(
                label="Balance Stability",
                value=f"{results['walk_stability']}%",
                delta="+1.8%" if random.random() > 0.5 else "-0.9%"
            )
        
        with walk_col3:
            st.metric(
                label="Gait Symmetry",
                value=f"{results['gait_symmetry']}%",
                delta="+3.2%" if random.random() > 0.5 else "-1.1%"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Hand Steadiness Metrics
        st.markdown("#### ✋ Hand Steadiness Assessment")
        hand_col1, hand_col2, hand_col3 = st.columns(3)
        
        with hand_col1:
            st.metric(
                label="Steadiness Score",
                value=f"{results['hand_steadiness']}%",
                delta="+2.5%" if random.random() > 0.5 else "-1.2%"
            )
        
        with hand_col2:
            st.metric(
                label="Tremor Index",
                value=f"{results['tremor_index']}",
                delta="-0.3" if random.random() > 0.5 else "+0.2",
                delta_color="inverse",
                help="Lower values indicate less tremor (better)"
            )
        
        with hand_col3:
            st.metric(
                label="Coordination Score",
                value=f"{results['coordination_score']}%",
                delta="+1.9%" if random.random() > 0.5 else "-0.8%"
            )
        
        st.markdown("---")
        
        # ========================================
        # INSIGHTS SECTION
        # ========================================
        st.markdown("### 💡 Today's Insights")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("""
            <div style='background: #E8F5E9; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #50C878;'>
                <h4 style='color: #50C878; margin-top: 0;'>✅ Positive Observations</h4>
                <ul style='margin: 0; padding-left: 1.5rem;'>
                    <li>Movement speed is within healthy range</li>
                    <li>Good stability during standing activities</li>
                    <li>Hand coordination shows strong control</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col2:
            st.markdown("""
            <div style='background: #FFF3E0; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FF9800;'>
                <h4 style='color: #FF9800; margin-top: 0;'>📌 Areas to Monitor</h4>
                <ul style='margin: 0; padding-left: 1.5rem;'>
                    <li>Track walking speed trend over next week</li>
                    <li>Compare stability scores to baseline</li>
                    <li>Continue daily assessments for patterns</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========================================
        # COMPLETION MESSAGE
        # ========================================
        st.info("""
        🎉 **Great job completing your daily check!**
        
        These metrics give us a snapshot of your movement health today. As you continue 
        daily checks, our AI will learn your unique patterns and alert you to any gradual 
        changes that might indicate health drift.
        
        💡 **Tip:** Consistency is key! Try to do your daily check at the same time each day 
        for the most accurate drift detection.
        """)
        
        st.markdown("---")
        
        # ========================================
        # ACTION BUTTONS
        # ========================================
        st.markdown("### 🎯 What's Next?")
        
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            if st.button("📊 View Dashboard", use_container_width=True, type="primary"):
                st.session_state.current_page = "Dashboard"
                st.rerun()
        
        with btn_col2:
            if st.button("💬 Chat with AI", use_container_width=True):
                st.session_state.current_page = "AI Health Chat"
                st.rerun()
        
        with btn_col3:
            if st.button("🔄 New Check", use_container_width=True):
                st.session_state.check_started = False
                st.session_state.check_completed = False
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========================================
        # DISCLAIMER
        # ========================================
        st.warning("""
        📋 **Important Note:** These metrics are for tracking changes over time, not for 
        diagnosing health conditions. If you notice significant changes or have concerns 
        about your movement or balance, please consult a healthcare professional.
        """)
