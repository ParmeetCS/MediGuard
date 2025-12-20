"""
Daily Health Check - Premium Interactive Assessment
Features: Professional UI, Interactive graphs, Data tables, Enhanced camera preview
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

# =======================
# PREMIUM COLOR SCHEME
# =======================
PRIMARY = "#667EEA"        # Purple
SECONDARY = "#764BA2"      # Deep Purple
ACCENT = "#F093FB"         # Pink
SUCCESS = "#4FACFE"        # Blue
WARNING = "#FFA726"        # Orange
DANGER = "#EF5350"         # Red
BG_GRADIENT = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"

# --- Helper Functions ---

def load_history_df():
    """Load history for the current user."""
    user_id = st.session_state.get('user_id', 'default_user')
    records = load_health_records(user_id)
    return pd.DataFrame(records) if records else pd.DataFrame()

def show():
    # Enhanced Custom CSS
    st.markdown("""
    <style>
        /* Global Styles */
        .stApp {
            background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* Premium Button Styling */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 30px;
            padding: 15px 40px;
            font-weight: 700;
            font-size: 16px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
        }
        
        /* Metric Cards */
        .metric-card {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-top: 4px solid #667eea;
            margin: 15px 0;
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        /* Camera Preview Frame */
        .camera-frame {
            background: linear-gradient(145deg, #1e1e1e, #2d2d2d);
            padding: 20px;
            border-radius: 25px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3),
                        inset 0 0 0 2px rgba(255,255,255,0.1);
            margin: 20px 0;
        }
        
        /* Header Styling */
        .activity-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 25px;
            color: white;
            text-align: center;
            margin-bottom: 2.5rem;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        }
        
        /* Info Boxes */
        .info-box {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            padding: 2rem;
            border-radius: 20px;
            border-left: 5px solid #667eea;
            margin: 1.5rem 0;
        }
        
        /* Data Table Styling */
        .dataframe {
            border-radius: 15px;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='activity-header'>
        <h1 style='font-size: 3rem; margin: 0;'>🩺 Daily Health Check</h1>
        <p style='font-size: 1.3rem; margin-top: 1rem; opacity: 0.95;'>AI-Powered Movement Analysis System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Session State
    if 'stage' not in st.session_state:
        st.session_state.stage = 'intro'
    if 'results' not in st.session_state:
        st.session_state.results = {}
    if 'activity_data' not in st.session_state:
        st.session_state.activity_data = {}

    # Enhanced Recording Function with Beautiful Camera Frame
    def run_recording_session(activity_key, duration, instruction):
        """Enhanced recording with premium camera preview."""
        st.markdown(f"""
        <div class='info-box'>
            <h3 style='color: #667eea; margin: 0 0 10px 0;'>📋 Instructions</h3>
            <p style='font-size: 1.1rem; margin: 0;'>{instruction}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Camera Preview Container
        st.markdown("<div class='camera-frame'>", unsafe_allow_html=True)
        cam_placeholder = st.empty()
        st.markdown("</div>", unsafe_allow_html=True)
        
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
        """Create beautiful interactive Plotly graph."""
        fig = go.Figure()
        
        # Add main line with gradient fill
        fig.add_trace(go.Scatter(
            y=data,
            x=list(range(len(data))),
            mode='lines',
            name='Motion',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)'
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
                line=dict(color='#f093fb', width=2, dash='dash')
            ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, color='#2c3e50')),
            xaxis_title="Frame Number",
            yaxis_title=y_label,
            template="plotly_white",
            hovermode='x unified',
            height=400,
            font=dict(family="Inter, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        return fig
    
    def display_metrics_with_data(feats, activity_name):
        """Display metrics, graphs, and data tables."""
        st.markdown(f"### 📊 {activity_name} - Analysis Results")
        
        # Key Metrics in Cards
        col1, col2, col3, col4 = st.columns(4)
        metrics_data = [
            (col1, "🏃 Speed", feats.get('movement_speed', 0), "#667eea"),
            (col2, "⚖️ Stability", feats.get('stability', 0), "#4facfe"),
            (col3, "🎯 Smoothness", feats.get('motion_smoothness', 0), "#f093fb"),
            (col4, "📏 Range", feats.get('range_of_motion', 0), "#ffa726")
        ]
        
        for col, label, value, color in metrics_data:
            with col:
                st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 15px; text-align: center; 
                            box-shadow: 0 5px 15px rgba(0,0,0,0.08); border-top: 3px solid {color};'>
                    <p style='margin: 0; color: #888; font-size: 0.9rem;'>{label}</p>
                    <h2 style='margin: 10px 0; color: {color}; font-size: 2.5rem;'>{value}</h2>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
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
            st.markdown("#### 📋 Detailed Metrics Table")
            
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
                    feats.get('movement_speed', 0),
                    feats.get('stability', 0),
                    feats.get('motion_smoothness', 0),
                    feats.get('posture_deviation', 0),
                    feats.get('micro_movements', 0),
                    feats.get('range_of_motion', 0),
                    feats.get('acceleration_variance', 0),
                    feats.get('frame_count', 0)
                ],
                'Unit': ['0-1', '0-1', '0-1', '0-1', '0-1', '0-1', '0-1', 'frames'],
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
            
            st.dataframe(
                metrics_table.style.set_properties(**{
                    'background-color': 'white',
                    'color': '#2c3e50',
                    'border-color': '#e0e0e0'
                }),
                use_container_width=True,
                height=350
            )
            
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
        st.markdown("""
        <div class='info-box'>
            <h2 style='color: #667eea; margin-top: 0;'>Welcome! 👋</h2>
            <p style='font-size: 1.1rem; line-height: 1.6;'>
                Complete <strong>3 simple activities</strong> to get comprehensive insights into your movement health:
            </p>
            <div style='margin: 20px 0;'>
                <p style='font-size: 1.05rem;'><strong>🪑 Sit-to-Stand:</strong> Measures leg strength and transition speed</p>
                <p style='font-size: 1.05rem;'><strong>⚖️ Stability Test:</strong> Evaluates balance and posture control</p>
                <p style='font-size: 1.05rem;'><strong>🏃 Movement Speed:</strong> Assesses coordination and activity level</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Begin Health Assessment", type="primary", use_container_width=True):
                st.session_state.stage = 'sit_stand'
                st.session_state.activity_data = {}
                st.rerun()
        
        st.markdown("---")
        st.subheader("📈 Your Progress Over Time")
        df = load_history_df()
        if not df.empty and 'date' in df.columns:
            fig = go.Figure()
            for col in ['movement_speed', 'stability', 'posture_deviation']:
                if col in df.columns:
                    fig.add_trace(go.Scatter(x=df['date'], y=df[col], mode='lines+markers', name=col.replace('_', ' ').title()))
            fig.update_layout(title="Historical Health Trends", template="plotly_white", height=400)
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
                display_metrics_with_data(feats, "Sit-to-Stand")
                if st.button("✅ Continue to Stability Test", type="primary", use_container_width=True):
                    st.session_state.stage = 'stability'
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
                display_metrics_with_data(feats, "Stability")
                if st.button("✅ Continue to Movement Test", type="primary", use_container_width=True):
                    st.session_state.stage = 'movement'
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
                display_metrics_with_data(feats, "Movement Speed")
                if st.button("💾 Complete & Save Results", type="primary", use_container_width=True):
                    st.session_state.stage = 'complete'
                    st.rerun()

    # STAGE: COMPLETE
    elif st.session_state.stage == 'complete':
        st.balloons()
        st.markdown("""
        <div class='activity-header'>
            <h1 style='font-size: 3rem; margin: 0;'>✅ Assessment Complete!</h1>
            <p style='font-size: 1.2rem; margin-top: 1rem;'>Excellent work! Here's your comprehensive health summary</p>
        </div>
        """, unsafe_allow_html=True)
        
        all_data = st.session_state.activity_data
        
        final_output = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "movement_speed": all_data.get('movement', {}).get('movement_speed', 0),
            "stability": all_data.get('stability', {}).get('stability', 0),
            "posture_deviation": all_data.get('stability', {}).get('posture_deviation', 0),
        }
        
        if 'saved' not in st.session_state.results:
            user_id = st.session_state.get('user_id', 'default_user')
            save_health_record(user_id, final_output)
            st.session_state.results['saved'] = True
        
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
        fig = px.bar(summary_df, x='Activity', y=['Speed', 'Stability'], barmode='group',
                     title="Performance Comparison Across Activities",
                     color_discrete_sequence=['#667eea', '#4facfe'])
        fig.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 New Assessment", use_container_width=True, type="primary"):
                st.session_state.stage = 'intro'
                st.session_state.results = {}
                st.session_state.activity_data = {}
                st.rerun()
        with col2:
            if st.button("📊 View Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
