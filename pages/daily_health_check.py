"""
Daily Health Check - MediGuard Drift AI
Movement analysis and health assessment page with person detection
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
from vision.person_detection import PersonDetector

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
        """Recording session with camera preview and person detection."""
        st.info(f"📋 **Instructions:** {instruction}")
        
        # Initialize person detector
        detector = PersonDetector()
        
        # Camera Preview Container
        cam_placeholder = st.empty()
        
        status_col1, status_col2, status_col3 = st.columns([2, 1, 1])
        with status_col1:
            progress_bar = st.progress(0, text="Ready to record...")
        with status_col2:
            status_text = st.empty()
        with status_col3:
            person_status = st.empty()
        
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
                    # Detect person and draw green bounding boxes
                    processed_frame, person_count = detector.process_frame(frame, draw_boxes=True)
                    
                    # Add recording indicator overlay
                    h, w = processed_frame.shape[:2]
                    cv2.circle(processed_frame, (30, 30), 15, (255, 0, 0), -1)
                    cv2.putText(processed_frame, "REC", (55, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    
                    # Add person detection status
                    if person_count > 0:
                        cv2.putText(processed_frame, f"Person Detected: {person_count}", 
                                  (w - 250, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    else:
                        cv2.putText(processed_frame, "No Person Detected", 
                                  (w - 250, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
                    cam_placeholder.image(processed_frame, channels="RGB", use_container_width=True)
                    frames.append(frame)  # Store original frame for processing
                
                progress = min(elapsed / duration, 1.0)
                progress_bar.progress(progress, text=f"Recording... {int((1-progress)*duration)}s remaining")
                status_text.metric("Frames", len(frames))
                
                # Update person detection status
                if frame is not None:
                    _, count = detector.process_frame(frame, draw_boxes=False)
                    person_status.metric("👤 Detected", count)
            
            progress_bar.progress(1.0, text="✅ Complete!")
            cam_placeholder.success("📹 Recording saved successfully!")
            time.sleep(1)
            
            return frames
        
        cam_placeholder.info("👆 Click 'Start Recording' to begin capturing video with person detection")
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
        
        # Import rating function
        try:
            from agents.ai_integration import rate_metric_value
        except:
            rate_metric_value = None
        
        # Key Metrics with User-Friendly Interpretations
        col1, col2, col3, col4 = st.columns(4)
        
        # Movement Speed with interpretation
        with col1:
            speed_val = feats.get('movement_speed', 0)
            st.metric("🏃 Movement Speed", f"{speed_val:.3f}")
            if rate_metric_value:
                rating = rate_metric_value('movement_speed', speed_val)
                st.markdown(f"""
                <div style='background: {rating['color']}22; padding: 10px; border-radius: 8px; 
                            border-left: 4px solid {rating['color']}; margin-top: 5px;'>
                    <div style='font-size: 1.2rem;'>{rating['emoji']} <b>{rating['rating']}</b></div>
                    <div style='font-size: 0.85rem; color: #555; margin-top: 3px;'>{rating['description']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Stability with interpretation
        with col2:
            stability_val = feats.get('stability', 0)
            st.metric("⚖️ Stability", f"{stability_val:.3f}")
            if rate_metric_value:
                rating = rate_metric_value('stability', stability_val)
                st.markdown(f"""
                <div style='background: {rating['color']}22; padding: 10px; border-radius: 8px; 
                            border-left: 4px solid {rating['color']}; margin-top: 5px;'>
                    <div style='font-size: 1.2rem;'>{rating['emoji']} <b>{rating['rating']}</b></div>
                    <div style='font-size: 0.85rem; color: #555; margin-top: 3px;'>{rating['description']}</div>
                </div>
                """, unsafe_allow_html=True)
        
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
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; color: white; text-align: center;'>
            <h2>🏥 Movement Health Assessment</h2>
            <p style='font-size: 1.1rem; margin-top: 1rem;'>
                Complete 3 simple activities to get comprehensive insights into your movement health
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Activity cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 10px; 
                        border: 2px solid #667eea; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>🪑</div>
                <h3 style='color: #667eea; margin-bottom: 0.5rem;'>Sit-to-Stand</h3>
                <p style='color: #666; font-size: 0.9rem;'>
                    Measures leg strength and transition speed
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 10px; 
                        border: 2px solid #764ba2; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>⚖️</div>
                <h3 style='color: #764ba2; margin-bottom: 0.5rem;'>Stability Test</h3>
                <p style='color: #666; font-size: 0.9rem;'>
                    Evaluates balance and posture control
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 10px; 
                        border: 2px solid #f093fb; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>🏃</div>
                <h3 style='color: #f093fb; margin-bottom: 0.5rem;'>Movement Speed</h3>
                <p style='color: #666; font-size: 0.9rem;'>
                    Assesses coordination and activity level
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.info("🤖 **AI-Powered Detection:** The system uses OpenCV to automatically detect you with green bounding boxes during the assessment!")
        
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
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h3 style='color: #00E5FF;'>📈 YOUR HEALTH PROGRESS - EASY TO READ!</h3>
            <p style='color: #B0BEC5; font-size: 1rem;'>📊 Scores shown as percentages (%) - Higher is better!</p>
        </div>
        """, unsafe_allow_html=True)
        
        df = load_history_df()
        if not df.empty and 'date' in df.columns:
            # Convert date column to datetime and format properly
            df['date'] = pd.to_datetime(df['date'])
            df['formatted_date'] = df['date'].dt.strftime('%b %d')
            df = df.sort_values('date')
            
            # Graph type selector
            col_left, col_right = st.columns([3, 1])
            with col_right:
                chart_type = st.selectbox("📊 Chart Type", ["Bar Chart", "Line Chart"], key="chart_selector")
            
            # Create figure
            fig = go.Figure()
            
            # Define metrics with vibrant colors for better contrast
            metrics = {
                'movement_speed': {'name': 'Movement Speed', 'color': '#00E5FF', 'emoji': '🏃'},
                'stability': {'name': 'Stability', 'color': '#00E676', 'emoji': '⚖️'}
            }
            
            if chart_type == "Bar Chart":
                # Bar chart with clear value labels
                for col, info in metrics.items():
                    if col in df.columns:
                        # Convert to percentage for patient-friendly display
                        values_percent = [val * 100 for val in df[col]]
                        
                        fig.add_trace(go.Bar(
                            x=df['formatted_date'],
                            y=df[col],
                            name=f"{info['emoji']} {info['name']}",
                            marker=dict(
                                color=info['color'],
                                line=dict(color='#1e1e1e', width=2),
                                opacity=0.95
                            ),
                            text=[f"<b>{val:.0f}%</b>" for val in values_percent],
                            textposition='outside',
                            textfont=dict(size=18, color=info['color'], family='Arial Black'),
                            hovertemplate='<b style="font-size:16px; color:white;">%{x}</b><br>' + 
                                        f'<span style="color:{info["color"]}; font-size:16px;">{info["emoji"]} {info["name"]}<br><b>Score: %{{y:.2f}} (%{{text}})</b></span><br>' +
                                        '<extra></extra>'
                        ))
                
                fig.update_layout(barmode='group', bargap=0.3, bargroupgap=0.15)
            else:
                # Line chart with clear value labels
                for col, info in metrics.items():
                    if col in df.columns:
                        # Convert to percentage for patient-friendly display
                        values_percent = [val * 100 for val in df[col]]
                        
                        fig.add_trace(go.Scatter(
                            x=df['formatted_date'],
                            y=df[col],
                            mode='lines+markers+text',
                            name=f"{info['emoji']} {info['name']}",
                            line=dict(width=6, color=info['color'], shape='spline'),
                            marker=dict(
                                size=20, 
                                color=info['color'],
                                line=dict(width=4, color='#1e1e1e'),
                                symbol='circle'
                            ),
                            text=[f"<b>{val:.0f}%</b>" for val in values_percent],
                            textposition='top center',
                            textfont=dict(size=16, color=info['color'], family='Arial Black'),
                            hovertemplate='<b style="font-size:16px; color:white;">%{x}</b><br>' + 
                                        f'<span style="color:{info["color"]}; font-size:16px;">{info["emoji"]} {info["name"]}<br><b>Score: %{{y:.2f}} (%{{text}})</b></span><br>' +
                                        '<extra></extra>'
                        ))
            
            # Update layout with DARK THEME to match page
            fig.update_layout(
                title={
                    'text': "<b style='font-size:32px; color:#00E5FF;'>📊 HEALTH SCORE TRENDS</b>",
                    'x': 0.5,
                    'xanchor': 'center',
                    'y': 0.95,
                    'yanchor': 'top'
                },
                xaxis_title="<b style='font-size:18px; color:#B0BEC5;'>Assessment Date</b>",
                yaxis_title="<b style='font-size:18px; color:#B0BEC5;'>Health Score</b>",
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    tickfont=dict(size=14, color='#CFD8DC', family='Arial'),
                    linecolor='#546E7A',
                    linewidth=2
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    range=[0, 1.1],
                    tickfont=dict(size=14, color='#CFD8DC', family='Arial'),
                    linecolor='#546E7A',
                    linewidth=2
                ),
                font=dict(family='Arial, sans-serif', size=14, color='#ECEFF1'),
                template="plotly_dark",
                height=600,
                hovermode='x unified',
                hoverlabel=dict(
                    bgcolor="#263238",
                    font_size=15,
                    font_family="Arial",
                    bordercolor="#00E5FF"
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=16, family='Arial Black', color='white'),
                    bgcolor='rgba(38, 50, 56, 0.9)',
                    bordercolor='#00E5FF',
                    borderwidth=2
                ),
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#262626',
                margin=dict(l=90, r=60, t=130, b=130)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add summary statistics cards with patient-friendly descriptions
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Add explanation for patients
            st.info("💡 **How to read your scores:** Higher percentages are better! Aim for scores above 70% for optimal health.")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'movement_speed' in df.columns:
                    latest = df['movement_speed'].iloc[-1]
                    avg = df['movement_speed'].mean()
                    delta = latest - avg
                    percent = latest * 100
                    
                    # Patient-friendly interpretation
                    if percent >= 80:
                        status = "🟢 Excellent"
                    elif percent >= 60:
                        status = "🟡 Good"
                    else:
                        status = "🟠 Needs Improvement"
                    
                    st.metric(
                        "🏃 Movement Speed", 
                        f"{percent:.0f}%", 
                        f"{delta*100:+.0f}% vs avg"
                    )
                    st.caption(f"Status: {status}")
            
            with col2:
                if 'stability' in df.columns:
                    latest = df['stability'].iloc[-1]
                    avg = df['stability'].mean()
                    delta = latest - avg
                    percent = latest * 100
                    
                    # Patient-friendly interpretation
                    if percent >= 80:
                        status = "🟢 Excellent"
                    elif percent >= 60:
                        status = "🟡 Good"
                    else:
                        status = "🟠 Needs Improvement"
                    
                    st.metric(
                        "⚖️ Stability", 
                        f"{percent:.0f}%", 
                        f"{delta*100:+.0f}% vs avg"
                    )
                    st.caption(f"Status: {status}")
            
            with col3:
                # Overall health score
                if 'movement_speed' in df.columns and 'stability' in df.columns:
                    overall = (df['movement_speed'].iloc[-1] + df['stability'].iloc[-1]) / 2 * 100
                    
                    if overall >= 80:
                        status = "🟢 Excellent Health"
                    elif overall >= 60:
                        status = "🟡 Good Health"
                    else:
                        status = "🟠 Monitor Closely"
                    
                    st.metric("🎯 Overall Health", f"{overall:.0f}%", status)
                    st.caption(f"Total: {len(df)} assessments")
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
        
        # Final Summary Table with User-Friendly Interpretations
        st.markdown("### 📊 Complete Results Summary")
        
        try:
            from agents.ai_integration import rate_metric_value
            
            # Sit-to-Stand metrics
            sit_stand_speed = all_data.get('sit_stand', {}).get('movement_speed', 0)
            sit_stand_stability = all_data.get('sit_stand', {}).get('stability', 0)
            sit_speed_rating = rate_metric_value('sit_stand_speed', sit_stand_speed)
            sit_stability_rating = rate_metric_value('stability', sit_stand_stability)
            
            # Balance/Stability metrics
            balance_speed = all_data.get('stability', {}).get('movement_speed', 0)
            balance_stability = all_data.get('stability', {}).get('stability', 0)
            balance_speed_rating = rate_metric_value('movement_speed', balance_speed)
            balance_stability_rating = rate_metric_value('stability', balance_stability)
            
            # Movement metrics
            movement_speed = all_data.get('movement', {}).get('movement_speed', 0)
            movement_stability = all_data.get('movement', {}).get('stability', 0)
            movement_speed_rating = rate_metric_value('movement_speed', movement_speed)
            movement_stability_rating = rate_metric_value('stability', movement_stability)
            
            # Create enhanced columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div style='background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                    <h4 style='color: #667eea; margin-bottom: 15px;'>🪑 Sit-to-Stand Test</h4>
                """, unsafe_allow_html=True)
                st.markdown(f"**Movement Speed:** {sit_stand_speed:.3f}")
                st.markdown(f"""
                <div style='background: {sit_speed_rating['color']}22; padding: 8px; border-radius: 6px; 
                            border-left: 3px solid {sit_speed_rating['color']}; margin: 8px 0;'>
                    {sit_speed_rating['emoji']} <b>{sit_speed_rating['rating']}</b><br>
                    <small>{sit_speed_rating['description']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Stability:** {sit_stand_stability:.3f}")
                st.markdown(f"""
                <div style='background: {sit_stability_rating['color']}22; padding: 8px; border-radius: 6px; 
                            border-left: 3px solid {sit_stability_rating['color']}; margin: 8px 0;'>
                    {sit_stability_rating['emoji']} <b>{sit_stability_rating['rating']}</b><br>
                    <small>{sit_stability_rating['description']}</small>
                </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style='background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                    <h4 style='color: #26c6da; margin-bottom: 15px;'>⚖️ Balance Test</h4>
                """, unsafe_allow_html=True)
                st.markdown(f"**Movement Speed:** {balance_speed:.3f}")
                st.markdown(f"""
                <div style='background: {balance_speed_rating['color']}22; padding: 8px; border-radius: 6px; 
                            border-left: 3px solid {balance_speed_rating['color']}; margin: 8px 0;'>
                    {balance_speed_rating['emoji']} <b>{balance_speed_rating['rating']}</b><br>
                    <small>{balance_speed_rating['description']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Stability:** {balance_stability:.3f}")
                st.markdown(f"""
                <div style='background: {balance_stability_rating['color']}22; padding: 8px; border-radius: 6px; 
                            border-left: 3px solid {balance_stability_rating['color']}; margin: 8px 0;'>
                    {balance_stability_rating['emoji']} <b>{balance_stability_rating['rating']}</b><br>
                    <small>{balance_stability_rating['description']}</small>
                </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style='background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                    <h4 style='color: #66bb6a; margin-bottom: 15px;'>🏃 Movement Test</h4>
                """, unsafe_allow_html=True)
                st.markdown(f"**Movement Speed:** {movement_speed:.3f}")
                st.markdown(f"""
                <div style='background: {movement_speed_rating['color']}22; padding: 8px; border-radius: 6px; 
                            border-left: 3px solid {movement_speed_rating['color']}; margin: 8px 0;'>
                    {movement_speed_rating['emoji']} <b>{movement_speed_rating['rating']}</b><br>
                    <small>{movement_speed_rating['description']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Stability:** {movement_stability:.3f}")
                st.markdown(f"""
                <div style='background: {movement_stability_rating['color']}22; padding: 8px; border-radius: 6px; 
                            border-left: 3px solid {movement_stability_rating['color']}; margin: 8px 0;'>
                    {movement_stability_rating['emoji']} <b>{movement_stability_rating['rating']}</b><br>
                    <small>{movement_stability_rating['description']}</small>
                </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Add comprehensive interpretation guide
            st.markdown("---")
            st.markdown("### 📖 Understanding Your Results")
            
            with st.expander("ℹ️ What Do These Scores Mean?", expanded=True):
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;'>
                    <h4 style='color: white; margin-top: 0;'>🎯 Score Interpretation Guide</h4>
                    <p>Your health scores range from 0.000 to 1.000. Here's what they mean:</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div style='background: #4CAF5022; padding: 15px; border-radius: 10px; border-left: 4px solid #4CAF50; margin: 10px 0;'>
                        <h4 style='color: #4CAF50; margin-top: 0;'>🟢 Excellent (0.85-1.00)</h4>
                        <p><strong>What it means:</strong> You're performing at an optimal level with no concerns.</p>
                        <p><strong>Action:</strong> Keep up your current healthy habits!</p>
                    </div>
                    
                    <div style='background: #8BC34A22; padding: 15px; border-radius: 10px; border-left: 4px solid #8BC34A; margin: 10px 0;'>
                        <h4 style='color: #8BC34A; margin-top: 0;'>✅ Good (0.75-0.84)</h4>
                        <p><strong>What it means:</strong> You're in a healthy range with normal function.</p>
                        <p><strong>Action:</strong> Continue regular activity and monitoring.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style='background: #FFC10722; padding: 15px; border-radius: 10px; border-left: 4px solid #FFC107; margin: 10px 0;'>
                        <h4 style='color: #FFC107; margin-top: 0;'>🟡 Fair (0.65-0.74)</h4>
                        <p><strong>What it means:</strong> Below ideal levels, worth monitoring closely.</p>
                        <p><strong>Action:</strong> Consider gentle exercises and track for changes.</p>
                    </div>
                    
                    <div style='background: #FF980022; padding: 15px; border-radius: 10px; border-left: 4px solid #FF9800; margin: 10px 0;'>
                        <h4 style='color: #FF9800; margin-top: 0;'>🟠 Needs Attention (<0.65)</h4>
                        <p><strong>What it means:</strong> Significantly below normal, requires attention.</p>
                        <p><strong>Action:</strong> Consult with your doctor about these results.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Specific metric explanations
                st.markdown("#### 📋 What Each Test Measures:")
                
                tab1, tab2, tab3 = st.tabs(["🪑 Sit-to-Stand", "⚖️ Balance", "🏃 Movement"])
                
                with tab1:
                    st.markdown("""
                    **Sit-to-Stand Test** measures your leg strength and ability to transition from sitting to standing.
                    
                    - **Movement Speed:** How quickly you can stand up
                    - **Stability:** How steady you are during the transition
                    
                    **Why it matters:** This test reveals lower body strength, core stability, and fall risk. 
                    Difficulty standing may indicate muscle weakness or balance issues.
                    """)
                
                with tab2:
                    st.markdown("""
                    **Balance Test** measures your ability to maintain steadiness while standing still.
                    
                    - **Movement Speed:** Minimal movement while standing
                    - **Stability:** How much you sway or wobble
                    
                    **Why it matters:** Good balance reduces fall risk and indicates strong core muscles 
                    and neurological function. Poor balance may need medical evaluation.
                    """)
                
                with tab3:
                    st.markdown("""
                    **Movement Test** measures your overall mobility and coordination.
                    
                    - **Movement Speed:** How quickly you can perform movements
                    - **Stability:** How controlled your movements are
                    
                    **Why it matters:** This shows your general mobility, coordination, and functional fitness. 
                    Changes may indicate muscle weakness, joint issues, or neurological changes.
                    """)
                
                st.markdown("---")
                
                # When to seek help
                st.markdown("""
                <div style='background: #f44336; color: white; padding: 15px; border-radius: 10px; margin: 15px 0;'>
                    <h4 style='color: white; margin-top: 0;'>⚠️ When to Consult Your Doctor:</h4>
                    <ul>
                        <li>Multiple scores in the "Needs Attention" range (below 0.65)</li>
                        <li>Sudden drops in your scores over a few days</li>
                        <li>You're experiencing falls or near-falls</li>
                        <li>You notice difficulty with daily activities</li>
                        <li>You have pain or discomfort during movement</li>
                        <li>Any concerns about your mobility or balance</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("💡 **Remember:** These scores are tools for tracking trends over time. A single test doesn't tell the whole story - consistent monitoring helps spot meaningful changes.")
            
            # ========================================
            # PERSONALIZED HEALTH ANALYSIS BASED ON ACTUAL SCORES
            # ========================================
            st.markdown("---")
            st.markdown("### 🩺 Your Personalized Health Analysis")
            
            # Collect all scores
            scores = {
                'sit_stand_speed': sit_stand_speed,
                'sit_stand_stability': sit_stand_stability,
                'balance_speed': balance_speed,
                'balance_stability': balance_stability,
                'movement_speed': movement_speed,
                'movement_stability': movement_stability
            }
            
            # Count concerning scores
            low_scores = []
            fair_scores = []
            
            for name, val in scores.items():
                if val < 0.65:
                    low_scores.append((name, val))
                elif val < 0.75:
                    fair_scores.append((name, val))
            
            # Overall Health Status
            if len(low_scores) == 0 and len(fair_scores) == 0:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%); 
                            padding: 25px; border-radius: 12px; color: white; margin: 20px 0;'>
                    <h3 style='color: white; margin-top: 0;'>🎉 Excellent Health Status!</h3>
                    <p style='font-size: 1.1rem;'>All your test scores are in the healthy range. 
                    Keep maintaining your current activity levels and healthy lifestyle!</p>
                    <p><b>No medical concerns detected based on these results.</b></p>
                </div>
                """, unsafe_allow_html=True)
            
            elif len(low_scores) == 0 and len(fair_scores) > 0:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #FFC107 0%, #FF9800 100%); 
                            padding: 25px; border-radius: 12px; color: #333; margin: 20px 0;'>
                    <h3 style='color: #333; margin-top: 0;'>🟡 Fair Health Status - Worth Monitoring</h3>
                    <p style='font-size: 1.1rem;'>Some scores are slightly below ideal. 
                    This isn't alarming, but worth keeping an eye on.</p>
                    <p><b>Consider increasing daily exercise and monitor for changes.</b></p>
                </div>
                """, unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #FF5722 0%, #f44336 100%); 
                            padding: 25px; border-radius: 12px; color: white; margin: 20px 0;'>
                    <h3 style='color: white; margin-top: 0;'>🟠 Needs Attention - Please Review</h3>
                    <p style='font-size: 1.1rem;'>Some of your test scores are below normal ranges. 
                    This may indicate underlying health issues that should be evaluated.</p>
                    <p><b>We recommend consulting with your healthcare provider.</b></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show specific medical conditions based on scores
            if len(low_scores) > 0 or len(fair_scores) > 0:
                st.markdown("### ⚕️ Possible Health Conditions Based on Your Results")
                st.warning("⚠️ **Disclaimer:** This is informational only, NOT a diagnosis. Always consult a healthcare professional.")
                
                # Movement Speed Issues
                avg_movement = (sit_stand_speed + balance_speed + movement_speed) / 3
                if avg_movement < 0.75:
                    with st.expander("🏃 Low Movement Speed - Possible Conditions", expanded=True):
                        if avg_movement < 0.65:
                            st.markdown("""
                            <div style='background: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #f44336;'>
                                <h4 style='color: #c62828; margin-top: 0;'>Your Average Movement Speed: {:.3f} (Needs Attention)</h4>
                                <p style='color: #333;'><b>This score range may be associated with:</b></p>
                                <ul style='color: #555;'>
                                    <li><b>🧠 Parkinson's Disease</b> - Characterized by slow movement (bradykinesia)</li>
                                    <li><b>🦵 Peripheral Neuropathy</b> - Nerve damage affecting movement control</li>
                                    <li><b>🫀 Cardiovascular Issues</b> - Heart or circulation problems causing fatigue</li>
                                    <li><b>🦴 Severe Arthritis</b> - Joint pain limiting movement speed</li>
                                    <li><b>🫁 Respiratory Conditions</b> - COPD or lung issues causing breathlessness</li>
                                    <li><b>👴 Frailty Syndrome</b> - Age-related decline in physical function</li>
                                </ul>
                                <p style='color: #c62828; font-weight: bold;'>👨‍⚕️ Recommendation: Schedule an appointment with your doctor for evaluation.</p>
                            </div>
                            """.format(avg_movement), unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style='background: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;'>
                                <h4 style='color: #e65100; margin-top: 0;'>Your Average Movement Speed: {:.3f} (Fair)</h4>
                                <p style='color: #333;'><b>This score range may be associated with:</b></p>
                                <ul style='color: #555;'>
                                    <li><b>💪 Mild Muscle Weakness</b> - Reduced strength in legs or core</li>
                                    <li><b>😴 Fatigue</b> - Low energy or general tiredness</li>
                                    <li><b>🦴 Early Arthritis</b> - Beginning joint stiffness</li>
                                    <li><b>🏃 Deconditioning</b> - Reduced fitness from inactivity</li>
                                    <li><b>💊 Medication Side Effects</b> - Some drugs cause movement slowness</li>
                                </ul>
                                <p style='color: #e65100; font-weight: bold;'>💡 Recommendation: Increase daily walking and monitor for changes.</p>
                            </div>
                            """.format(avg_movement), unsafe_allow_html=True)
                
                # Stability/Balance Issues
                avg_stability = (sit_stand_stability + balance_stability + movement_stability) / 3
                if avg_stability < 0.75:
                    with st.expander("⚖️ Low Stability/Balance - Possible Conditions", expanded=True):
                        if avg_stability < 0.65:
                            st.markdown("""
                            <div style='background: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #f44336;'>
                                <h4 style='color: #c62828; margin-top: 0;'>Your Average Stability: {:.3f} (Needs Attention)</h4>
                                <p style='color: #333;'><b>This score range may be associated with:</b></p>
                                <ul style='color: #555;'>
                                    <li><b>👂 Vertigo/BPPV</b> - Inner ear balance disorder</li>
                                    <li><b>🧠 Cerebellar Disorders</b> - Brain areas affecting coordination</li>
                                    <li><b>🧬 Multiple Sclerosis</b> - Nerve damage affecting balance</li>
                                    <li><b>🩸 Stroke Effects</b> - Post-stroke balance impairment</li>
                                    <li><b>🦶 Severe Neuropathy</b> - Diabetic or other nerve damage in feet</li>
                                    <li><b>📉 Orthostatic Hypotension</b> - Blood pressure drops when standing</li>
                                </ul>
                                <p style='color: #c62828; font-weight: bold;'>👨‍⚕️ Recommendation: See a doctor soon. You may need a neurological or ENT evaluation.</p>
                            </div>
                            """.format(avg_stability), unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style='background: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;'>
                                <h4 style='color: #e65100; margin-top: 0;'>Your Average Stability: {:.3f} (Fair)</h4>
                                <p style='color: #333;'><b>This score range may be associated with:</b></p>
                                <ul style='color: #555;'>
                                    <li><b>👂 Mild Inner Ear Issues</b> - Slight vestibular problems</li>
                                    <li><b>💪 Core Weakness</b> - Weak abdominal or back muscles</li>
                                    <li><b>👁️ Vision Problems</b> - Poor depth perception affecting balance</li>
                                    <li><b>🦶 Mild Neuropathy</b> - Reduced sensation in feet</li>
                                    <li><b>😓 Muscle Fatigue</b> - Overexertion or tiredness</li>
                                </ul>
                                <p style='color: #e65100; font-weight: bold;'>💡 Recommendation: Practice balance exercises and consider a check-up if it persists.</p>
                            </div>
                            """.format(avg_stability), unsafe_allow_html=True)
                
                # Sit-Stand Specific Issues
                if sit_stand_speed < 0.75 or sit_stand_stability < 0.75:
                    with st.expander("🪑 Sit-to-Stand Difficulty - Possible Conditions", expanded=True):
                        if sit_stand_speed < 0.65 or sit_stand_stability < 0.65:
                            st.markdown("""
                            <div style='background: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #f44336;'>
                                <h4 style='color: #c62828; margin-top: 0;'>Sit-Stand Scores: Speed {:.3f}, Stability {:.3f}</h4>
                                <p style='color: #333;'><b>Difficulty rising from seated position may indicate:</b></p>
                                <ul style='color: #555;'>
                                    <li><b>🦵 Sarcopenia</b> - Age-related muscle loss, especially in thighs</li>
                                    <li><b>🦴 Knee/Hip Arthritis</b> - Joint pain and stiffness</li>
                                    <li><b>🫀 Heart Failure</b> - Weakness from poor circulation</li>
                                    <li><b>🫁 COPD</b> - Lung disease causing weakness and breathlessness</li>
                                    <li><b>💪 Myopathy</b> - Muscle disease affecting strength</li>
                                    <li><b>🏥 Joint Replacement Needed</b> - Severe joint deterioration</li>
                                </ul>
                                <p style='color: #c62828; font-weight: bold;'>👨‍⚕️ Recommendation: This is an important indicator. Please consult an orthopedic or geriatric specialist.</p>
                            </div>
                            """.format(sit_stand_speed, sit_stand_stability), unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style='background: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;'>
                                <h4 style='color: #e65100; margin-top: 0;'>Sit-Stand Scores: Speed {:.3f}, Stability {:.3f}</h4>
                                <p style='color: #333;'><b>Mild difficulty with sit-stand transitions may indicate:</b></p>
                                <ul style='color: #555;'>
                                    <li><b>🦵 Quadriceps Weakness</b> - Weak thigh muscles</li>
                                    <li><b>🦴 Mild Knee Arthritis</b> - Early joint wear</li>
                                    <li><b>🦴 Hip Stiffness</b> - Limited hip mobility</li>
                                    <li><b>🔙 Lower Back Pain</b> - Affecting ability to rise</li>
                                    <li><b>⚖️ Obesity Effects</b> - Extra weight making rising harder</li>
                                </ul>
                                <p style='color: #e65100; font-weight: bold;'>💡 Recommendation: Strengthen leg muscles with squats and leg exercises. Consider weight management.</p>
                            </div>
                            """.format(sit_stand_speed, sit_stand_stability), unsafe_allow_html=True)
                
                # Multiple Low Scores Warning
                if len(low_scores) >= 3:
                    st.markdown("""
                    <div style='background: #b71c1c; color: white; padding: 25px; border-radius: 12px; margin: 20px 0;'>
                        <h3 style='color: white; margin-top: 0;'>🚨 Multiple Areas of Concern Detected</h3>
                        <p style='font-size: 1.1rem;'>You have several scores in the "Needs Attention" range. 
                        This pattern may suggest systemic health issues that require comprehensive evaluation.</p>
                        
                        <h4 style='color: #ffcdd2;'>Conditions to discuss with your doctor:</h4>
                        <ul style='color: white;'>
                            <li><b>🧠 Neurological Conditions</b> - Parkinson's, MS, early dementia, stroke effects</li>
                            <li><b>❤️ Cardiovascular Problems</b> - Heart failure, arrhythmias, circulation issues</li>
                            <li><b>🦴 Musculoskeletal Issues</b> - Severe arthritis, osteoporosis, spinal problems</li>
                            <li><b>🩺 Metabolic Disorders</b> - Uncontrolled diabetes, thyroid issues, vitamin deficiencies</li>
                            <li><b>👴 Geriatric Syndromes</b> - Frailty, fall risk syndrome</li>
                        </ul>
                        
                        <p style='color: #ffcdd2; font-weight: bold; font-size: 1.2rem; margin-top: 15px;'>
                            ⚕️ IMPORTANT: Please schedule an appointment with your healthcare provider soon!
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Personalized Recommendations
                st.markdown("### 💊 Personalized Recommendations")
                
                rec_cols = st.columns(3)
                
                with rec_cols[0]:
                    if avg_movement < 0.75:
                        st.markdown("""
                        <div style='background: #1565c0; padding: 15px; border-radius: 10px; color: white;'>
                            <h4 style='color: white; margin-top: 0;'>🚶 For Movement Speed</h4>
                            <ul>
                                <li>Daily walking 15-30 mins</li>
                                <li>Swimming or water aerobics</li>
                                <li>Tai Chi for gentle movement</li>
                                <li>Physical therapy evaluation</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style='background: #2e7d32; padding: 15px; border-radius: 10px; color: white;'>
                            <h4 style='color: white; margin-top: 0;'>✅ Movement Speed OK</h4>
                            <p>Your movement speed is healthy. Maintain with regular activity!</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with rec_cols[1]:
                    if avg_stability < 0.75:
                        st.markdown("""
                        <div style='background: #7b1fa2; padding: 15px; border-radius: 10px; color: white;'>
                            <h4 style='color: white; margin-top: 0;'>⚖️ For Balance</h4>
                            <ul>
                                <li>Stand on one foot practice</li>
                                <li>Yoga or Pilates classes</li>
                                <li>Core strengthening exercises</li>
                                <li>Vision and hearing check</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style='background: #2e7d32; padding: 15px; border-radius: 10px; color: white;'>
                            <h4 style='color: white; margin-top: 0;'>✅ Balance OK</h4>
                            <p>Your balance is healthy. Keep practicing balance activities!</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with rec_cols[2]:
                    if sit_stand_speed < 0.75:
                        st.markdown("""
                        <div style='background: #c62828; padding: 15px; border-radius: 10px; color: white;'>
                            <h4 style='color: white; margin-top: 0;'>🪑 For Sit-Stand</h4>
                            <ul>
                                <li>Chair squats daily</li>
                                <li>Leg strengthening exercises</li>
                                <li>Use chair arms to assist</li>
                                <li>Consider physical therapy</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style='background: #2e7d32; padding: 15px; border-radius: 10px; color: white;'>
                            <h4 style='color: white; margin-top: 0;'>✅ Sit-Stand OK</h4>
                            <p>Your leg strength is good. Keep it up with regular activity!</p>
                        </div>
                        """, unsafe_allow_html=True)
                
        except Exception as e:
            # Fallback to simple table if there's an error
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
