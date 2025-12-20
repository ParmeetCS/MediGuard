"""
Daily Health Check - MediGuard Drift AI
Movement analysis and health assessment page
"""

import streamlit as st
import cv2
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Import vision modules
from vision.camera import camera_stream
from vision.feature_extraction import extract_features

# Import database module
from storage.database import save_health_record, load_health_records
from storage.health_repository import save_health_check


def load_history_df():
    """Load history for the current user."""
    user_id = st.session_state.get('user_id', 'default_user')
    records = load_health_records(user_id)
    return pd.DataFrame(records) if records else pd.DataFrame()


def show():
    """
    Display the daily health check page
    """
    
    # ========================================
    # PAGE HEADER
    # ========================================
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: #4A90E2; font-size: 2.5rem;'>🩺 Daily Health Check</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                AI-Powered Movement Analysis & Health Assessment
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize Session State FIRST
    if 'stage' not in st.session_state:
        st.session_state.stage = 'intro'
    if 'results' not in st.session_state:
        st.session_state.results = {}
    if 'activity_data' not in st.session_state:
        st.session_state.activity_data = {}
    if 'sit_stand_complete' not in st.session_state:
        st.session_state.sit_stand_complete = False
    if 'stability_complete' not in st.session_state:
        st.session_state.stability_complete = False
    if 'movement_complete' not in st.session_state:
        st.session_state.movement_complete = False
    
    # Debug panel (can be toggled) - Now safe to access session state
    with st.expander("🔧 Debug Info", expanded=False):
        st.write(f"**Current Stage:** `{st.session_state.stage}`")
        st.write(f"**User ID:** `{st.session_state.get('user_id', 'Not set')}`")
        st.write(f"**Authenticated:** `{st.session_state.get('authenticated', False)}`")
        st.write(f"**Completed Tests:** Sit-Stand: `{st.session_state.sit_stand_complete}`, "
                 f"Stability: `{st.session_state.stability_complete}`, "
                 f"Movement: `{st.session_state.movement_complete}`")
        st.write(f"**Activity Data Keys:** `{list(st.session_state.activity_data.keys())}`")
        
        if st.button("🔄 Reset Health Check", key="reset_hc"):
            st.session_state.stage = 'intro'
            st.session_state.results = {}
            st.session_state.activity_data = {}
            st.session_state.sit_stand_complete = False
            st.session_state.stability_complete = False
            st.session_state.movement_complete = False
            st.rerun()

    # Recording Function
    def run_recording_session(activity_key, duration, instruction):
        """Recording session with camera preview."""
        st.info(f"📋 **Instructions:** {instruction}")
        
        # Camera Preview Container
        cam_placeholder = st.empty()
        
        status_col1, status_col2 = st.columns([3, 1])
        with status_col1:
            progress_bar = st.progress(0, text="Ready to record...")
        with status_col2:
            status_text = st.empty()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            start_btn = st.button(f"🎥 Start Recording ({duration}s)", key=f"start_{activity_key}", use_container_width=True, type="primary")
        with col2:
            redo_btn = st.button(f"🔄 Redo Activity", key=f"redo_{activity_key}", use_container_width=True)
        with col3:
            skip_btn = st.button(f"⏭️ Skip", key=f"skip_{activity_key}", use_container_width=True)
        
        if redo_btn and activity_key in st.session_state.activity_data:
            del st.session_state.activity_data[activity_key]
            st.rerun()
        
        if skip_btn:
            return "skip"
        
        if start_btn:
            frames = []
            frame_gen = camera_stream()
            start_time = time.time()
            
            for frame in frame_gen:
                elapsed = time.time() - start_time
                if elapsed > duration:
                    break
                
                if frame is not None:
                    # Add recording indicator overlay
                    h, w = frame.shape[:2]
                    cv2.circle(frame, (30, 30), 15, (255, 0, 0), -1)
                    cv2.putText(frame, "REC", (55, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    
                    cam_placeholder.image(frame, channels="RGB", use_container_width=True)
                    frames.append(frame)
                
                progress = min(elapsed / duration, 1.0)
                progress_bar.progress(progress, text=f"Recording... {int((1-progress)*duration)}s remaining")
                status_text.metric("Frames", len(frames))
            
            progress_bar.progress(1.0, text="✅ Complete!")
            cam_placeholder.success("📹 Recording saved successfully!")
            time.sleep(1)
            
            return frames
        
        cam_placeholder.info("👆 Click 'Start Recording' to begin capturing video")
        return None
    
    def create_interactive_graph(data, title, y_label):
        """Create interactive Plotly graph."""
        fig = go.Figure()
        
        # Add main line
        fig.add_trace(go.Scatter(
            y=data,
            x=list(range(len(data))),
            mode='lines',
            name='Motion',
            line=dict(color='#4A90E2', width=3),
            fill='tozeroy',
            fillcolor='rgba(74, 144, 226, 0.2)'
        ))
        
        # Add smoothed trend line
        if len(data) > 10:
            window = min(10, len(data) // 5)
            smoothed = pd.Series(data).rolling(window=window, center=True).mean()
            fig.add_trace(go.Scatter(
                y=smoothed,
                x=list(range(len(data))),
                mode='lines',
                name='Trend',
                line=dict(color='#FF6B6B', width=2, dash='dash')
            ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color='#2c3e50')),
            xaxis_title="Frame Number",
            yaxis_title=y_label,
            template="plotly_white",
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def display_metrics_with_data(feats, activity_name):
        """Display metrics, graphs, and data tables."""
        st.markdown(f"### 📊 {activity_name} - Analysis Results")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🏃 Speed", f"{feats.get('movement_speed', 0):.2f}")
        with col2:
            st.metric("⚖️ Stability", f"{feats.get('stability', 0):.2f}")
        with col3:
            st.metric("🎯 Smoothness", f"{feats.get('motion_smoothness', 0):.2f}")
        with col4:
            st.metric("📏 Range", f"{feats.get('range_of_motion', 0):.2f}")
        
        st.markdown("---")
        
        # Interactive Graph
        if 'frame_by_frame_motion' in feats and feats['frame_by_frame_motion']:
            st.markdown("#### 📈 Real-Time Motion Analysis")
            fig = create_interactive_graph(
                feats['frame_by_frame_motion'],
                f"{activity_name} - Frame-by-Frame Motion Intensity",
                "Motion Intensity"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Numerical Data Table
            with st.expander("📋 View Detailed Metrics Table"):
                # Create comprehensive data table
                metrics_table = pd.DataFrame({
                    'Metric': [
                        'Movement Speed',
                        'Stability Score',
                        'Motion Smoothness',
                        'Posture Deviation',
                        'Micro-movements',
                        'Range of Motion',
                        'Acceleration Variance',
                        'Frames Analyzed'
                    ],
                    'Value': [
                        f"{feats.get('movement_speed', 0):.3f}",
                        f"{feats.get('stability', 0):.3f}",
                        f"{feats.get('motion_smoothness', 0):.3f}",
                        f"{feats.get('posture_deviation', 0):.3f}",
                        f"{feats.get('micro_movements', 0):.3f}",
                        f"{feats.get('range_of_motion', 0):.3f}",
                        f"{feats.get('acceleration_variance', 0):.3f}",
                        feats.get('frame_count', 0)
                    ],
                    'Status': [
                        '✅ Good' if feats.get('movement_speed', 0) > 0.5 else '⚠️ Low',
                        '✅ Good' if feats.get('stability', 0) > 0.7 else '⚠️ Moderate',
                        '✅ Good' if feats.get('motion_smoothness', 0) > 0.6 else '⚠️ Moderate',
                        '✅ Good' if feats.get('posture_deviation', 0) < 0.3 else '⚠️ High',
                        '✅ Normal' if feats.get('micro_movements', 0) < 0.3 else '⚠️ High',
                        '✅ Good' if feats.get('range_of_motion', 0) > 0.4 else '⚠️ Limited',
                        '✅ Smooth' if feats.get('acceleration_variance', 0) < 0.4 else '⚠️ Variable',
                        '✅'
                    ]
                })
                
                st.dataframe(metrics_table, use_container_width=True, height=350)
            
            # Frame-by-frame data sample
            with st.expander("🔍 View Frame-by-Frame Data (First 20 frames)"):
                frame_data = pd.DataFrame({
                    'Frame #': range(min(20, len(feats['frame_by_frame_motion']))),
                    'Motion Intensity': feats['frame_by_frame_motion'][:20],
                    'Timestamp (s)': [round(i/30, 2) for i in range(min(20, len(feats['frame_by_frame_motion'])))]
                })
                st.dataframe(frame_data, use_container_width=True)

    # STAGE: INTRO
    if st.session_state.stage == 'intro':
        st.info("""
        **Welcome! 👋**
        
        Complete **3 simple activities** to get comprehensive insights into your movement health:
        
        - **🪑 Sit-to-Stand:** Measures leg strength and transition speed
        - **⚖️ Stability Test:** Evaluates balance and posture control  
        - **🏃 Movement Speed:** Assesses coordination and activity level
        """)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Begin Health Assessment", type="primary", use_container_width=True):
                st.session_state.stage = 'sit_stand'
                st.session_state.activity_data = {}
                st.session_state.sit_stand_complete = False
                st.session_state.stability_complete = False
                st.session_state.movement_complete = False
                st.rerun()
        
        st.markdown("---")
        st.subheader("📈 Your Progress Over Time")
        df = load_history_df()
        if not df.empty and 'date' in df.columns:
            fig = go.Figure()
            for col in ['movement_speed', 'stability', 'posture_deviation']:
                if col in df.columns:
                    fig.add_trace(go.Scatter(
                        x=df['date'], 
                        y=df[col], 
                        mode='lines+markers', 
                        name=col.replace('_', ' ').title(),
                        line=dict(width=2)
                    ))
            fig.update_layout(
                title="Historical Health Trends", 
                template="plotly_white", 
                height=400,
                xaxis_title="Date",
                yaxis_title="Score"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 No history yet. Complete your first assessment to track progress!")

    # STAGE: SIT TO STAND
    elif st.session_state.stage == 'sit_stand':
        st.header("1️⃣ Sit-to-Stand Assessment")
        result = run_recording_session("sit_stand", 5, "Sit on a chair with arms crossed. Stand up fully, then sit back down. Repeat naturally.")
        
        if result == "skip":
            st.session_state.stage = 'stability'
            st.rerun()
        elif result:
            with st.spinner("🔬 Analyzing biomechanics..."):
                feats = extract_features(result, activity_name="sit_to_stand")
                st.session_state.activity_data['sit_stand'] = feats
                st.session_state.sit_stand_complete = True
            
        # Show results if test is complete
        if st.session_state.get('sit_stand_complete', False):
            display_metrics_with_data(st.session_state.activity_data['sit_stand'], "Sit-to-Stand")
            st.success("✅ Sit-to-Stand test completed!")
            if st.button("➡️ Continue to Stability Test", type="primary", use_container_width=True, key="continue_stability"):
                st.session_state.stage = 'stability'
                st.session_state.sit_stand_complete = False
                st.rerun()

    # STAGE: STABILITY
    elif st.session_state.stage == 'stability':
        st.header("2️⃣ Stability Assessment")
        result = run_recording_session("stability", 5, "Stand still with feet together, hands at sides. Maintain balance and focus ahead.")
        
        if result == "skip":
            st.session_state.stage = 'movement'
            st.rerun()
        elif result:
            with st.spinner("🔬 Analyzing balance patterns..."):
                feats = extract_features(result, activity_name="stability")
                st.session_state.activity_data['stability'] = feats
                st.session_state.stability_complete = True
        
        # Show results if test is complete
        if st.session_state.get('stability_complete', False):
            display_metrics_with_data(st.session_state.activity_data['stability'], "Stability")
            st.success("✅ Stability test completed!")
            if st.button("➡️ Continue to Movement Test", type="primary", use_container_width=True, key="continue_movement"):
                st.session_state.stage = 'movement'
                st.session_state.stability_complete = False
                st.rerun()

    # STAGE: MOVEMENT
    elif st.session_state.stage == 'movement':
        st.header("3️⃣ Movement Speed Assessment")
        result = run_recording_session("movement", 5, "Walk in place energetically or perform coordinated arm movements.")
        
        if result == "skip":
            st.session_state.stage = 'complete'
            st.rerun()
        elif result:
            with st.spinner("🔬 Analyzing movement dynamics..."):
                feats = extract_features(result, activity_name="general")
                st.session_state.activity_data['movement'] = feats
                st.session_state.movement_complete = True
        
        # Show results if test is complete
        if st.session_state.get('movement_complete', False):
            display_metrics_with_data(st.session_state.activity_data['movement'], "Movement Speed")
            st.success("✅ Movement test completed!")
            if st.button("💾 Complete & Save Results", type="primary", use_container_width=True, key="complete_save"):
                st.session_state.stage = 'complete'
                st.session_state.movement_complete = False
                st.rerun()

    # STAGE: COMPLETE
    elif st.session_state.stage == 'complete':
        st.balloons()
        st.success("✅ **Assessment Complete!** Excellent work! Here's your comprehensive health summary")
        
        all_data = st.session_state.activity_data
        
        # Prepare data for Supabase
        health_data = {}
        
        # Sit-to-Stand data
        if 'sit_stand' in all_data:
            sit_stand = all_data['sit_stand']
            health_data['sit_stand_movement_speed'] = sit_stand.get('movement_speed', 0)
            health_data['sit_stand_stability'] = sit_stand.get('stability', 0)
            health_data['sit_stand_motion_smoothness'] = sit_stand.get('motion_smoothness', 0)
            health_data['sit_stand_posture_deviation'] = sit_stand.get('posture_deviation', 0)
            health_data['sit_stand_micro_movements'] = sit_stand.get('micro_movements', 0)
            health_data['sit_stand_range_of_motion'] = sit_stand.get('range_of_motion', 0)
            health_data['sit_stand_acceleration_variance'] = sit_stand.get('acceleration_variance', 0)
            health_data['sit_stand_frame_count'] = sit_stand.get('frame_count', 0)
        
        # Stability/Balance data (map to steady)
        if 'stability' in all_data:
            stability = all_data['stability']
            health_data['steady_movement_speed'] = stability.get('movement_speed', 0)
            health_data['steady_stability'] = stability.get('stability', 0)
            health_data['steady_motion_smoothness'] = stability.get('motion_smoothness', 0)
            health_data['steady_posture_deviation'] = stability.get('posture_deviation', 0)
            health_data['steady_micro_movements'] = stability.get('micro_movements', 0)
            health_data['steady_range_of_motion'] = stability.get('range_of_motion', 0)
            health_data['steady_acceleration_variance'] = stability.get('acceleration_variance', 0)
            health_data['steady_frame_count'] = stability.get('frame_count', 0)
        
        # Movement data (map to walk)
        if 'movement' in all_data:
            movement = all_data['movement']
            health_data['walk_movement_speed'] = movement.get('movement_speed', 0)
            health_data['walk_stability'] = movement.get('stability', 0)
            health_data['walk_motion_smoothness'] = movement.get('motion_smoothness', 0)
            health_data['walk_posture_deviation'] = movement.get('posture_deviation', 0)
            health_data['walk_micro_movements'] = movement.get('micro_movements', 0)
            health_data['walk_range_of_motion'] = movement.get('range_of_motion', 0)
            health_data['walk_acceleration_variance'] = movement.get('acceleration_variance', 0)
            health_data['walk_frame_count'] = movement.get('frame_count', 0)
        
        # Calculate averages
        speeds = [v for k, v in health_data.items() if 'movement_speed' in k and v]
        stabilities = [v for k, v in health_data.items() if 'stability' in k and v]
        health_data['avg_movement_speed'] = sum(speeds) / len(speeds) if speeds else 0
        health_data['avg_stability'] = sum(stabilities) / len(stabilities) if stabilities else 0
        
        # Save to Supabase
        if 'saved' not in st.session_state.results:
            user_id = st.session_state.get('user_id', 'default_user')
            
            st.info(f"💾 Saving health check data for user: {user_id}...")
            
            # Display what we're about to save in user-friendly format
            with st.expander("📋 View Your Health Check Summary", expanded=False):
                st.markdown("### 📊 Today's Health Check Data")
                
                # Create a formatted display
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🏃 Movement Metrics:**")
                    for key, value in health_data.items():
                        if 'movement' in key or 'speed' in key:
                            formatted_key = key.replace('_', ' ').title()
                            st.text(f"{formatted_key}: {value:.4f}")
                
                with col2:
                    st.markdown("**⚖️ Balance & Stability:**")
                    for key, value in health_data.items():
                        if 'stability' in key or 'balance' in key:
                            formatted_key = key.replace('_', ' ').title()
                            st.text(f"{formatted_key}: {value:.4f}")
                
                st.markdown("---")
                st.caption(f"Total metrics recorded: {len(health_data)}")
            
            # Save to Supabase
            try:
                result = save_health_check(user_id, health_data)
                
                if result['success']:
                    st.session_state.results['saved'] = True
                    st.success(f"✅ {result['message']}")
                    st.balloons()
                    
                    # Show saved data details in a nice format
                    if result.get('data'):
                        st.info(f"📊 Saved to database at {datetime.now().strftime('%H:%M:%S')}")
                        with st.expander("📝 View Saved Record Details"):
                            saved_data = result['data']
                            st.markdown(f"**Date:** {saved_data.get('check_date', 'N/A')}")
                            st.markdown(f"**Time:** {saved_data.get('check_timestamp', 'N/A')}")
                            st.markdown(f"**User ID:** {saved_data.get('user_id', 'N/A')}")
                            st.success("✅ All metrics successfully saved to your health profile")
                else:
                    st.error(f"❌ Error saving to Supabase: {result['message']}")
                    st.warning("⚠️ This might be a connection issue or RLS policy issue.")
                    
                    # Show troubleshooting info
                    with st.expander("🔍 Troubleshooting Information"):
                        st.write("**Possible causes:**")
                        st.write("1. Supabase credentials not configured in .env file")
                        st.write("2. Row Level Security (RLS) policies preventing insert")
                        st.write("3. User ID mismatch with auth.uid()")
                        st.write(f"4. Current user_id: `{user_id}`")
                        st.write("5. Network connection issue")
                    
                    # Fallback to local JSON
                    final_output = {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "movement_speed": health_data.get('avg_movement_speed', 0),
                        "stability": health_data.get('avg_stability', 0),
                    }
                    save_health_record(user_id, final_output)
                    st.success("💾 Data saved to local storage as backup")
            except Exception as e:
                st.error(f"❌ Exception during save: {str(e)}")
                st.code(str(e), language="text")
        
        # Final Summary Table
        st.markdown("### 📊 Complete Results Summary")
        summary_df = pd.DataFrame([
            {'Activity': 'Sit-to-Stand', 'Speed': all_data.get('sit_stand', {}).get('movement_speed', 0), 
             'Stability': all_data.get('sit_stand', {}).get('stability', 0)},
            {'Activity': 'Balance', 'Speed': all_data.get('stability', {}).get('movement_speed', 0), 
             'Stability': all_data.get('stability', {}).get('stability', 0)},
            {'Activity': 'Movement', 'Speed': all_data.get('movement', {}).get('movement_speed', 0), 
             'Stability': all_data.get('movement', {}).get('stability', 0)}
        ])
        st.dataframe(summary_df, use_container_width=True, height=150)
        
        # Comparison Chart
        fig = px.bar(
            summary_df, 
            x='Activity', 
            y=['Speed', 'Stability'], 
            barmode='group',
            title="Performance Comparison Across Activities",
            color_discrete_sequence=['#4A90E2', '#7B68EE']
        )
        fig.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Assessment", use_container_width=True, type="primary"):
                st.session_state.stage = 'intro'
                st.session_state.results = {}
                st.session_state.activity_data = {}
                st.rerun()
        with col2:
            if st.button("📊 View Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
