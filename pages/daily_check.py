"""
Daily Health Check - MediGuard Drift AI
Camera-based movement analysis and health drift monitoring
"""

import streamlit as st
import cv2
import time
import json
import pandas as pd
import os
from datetime import datetime, date
from pathlib import Path

# Import vision modules
from vision.camera import camera_stream
from vision.feature_extraction import extract_features

# Import Supabase
from auth.supabase_auth import get_supabase_client


# ==========================================
# CONFIGURATION
# ==========================================
DATA_DIR = Path("data/daily_checks")
DATA_DIR.mkdir(parents=True, exist_ok=True)

STEPS = [
    {
        "name": "Sit to Stand",
        "key": "sit_stand",
        "instruction": "Sit on a chair, then stand up naturally. Repeat 2-3 times.",
        "duration": 5
    },
    {
        "name": "Short Walk",
        "key": "walk",
        "instruction": "Walk in place or take a few steps forward and backward.",
        "duration": 5
    },
    {
        "name": "Hold Steady",
        "key": "steady",
        "instruction": "Stand still with your hands at your sides. Try to remain steady.",
        "duration": 5
    }
]


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_user_data_file():
    """Get the file path for current user's daily check data"""
    user_id = st.session_state.get('user_id', 'default_user')
    date_str = datetime.now().strftime("%Y-%m-%d")
    return DATA_DIR / f"{user_id}_{date_str}.json"


def save_daily_check_data(features: dict):
    """Save daily check features to Supabase health_checks table"""
    try:
        user_id = st.session_state.get('user_id')
        
        if not user_id:
            return False, "User not authenticated"
        
        supabase = get_supabase_client()
        if not supabase:
            return False, "Database connection not available"
        
        # Prepare data for Supabase
        check_date = date.today().isoformat()
        check_timestamp = datetime.now().isoformat()
        
        # Build the data dictionary with proper column mapping
        data = {
            "user_id": user_id,
            "check_date": check_date,
            "check_timestamp": check_timestamp,
        }
        
        # Map combined features to database columns
        # Features are prefixed like: sit_stand_movement_speed, walk_stability, steady_micro_movements
        for key, value in features.items():
            if isinstance(value, (int, float)):
                # Keep the key as is (already has activity prefix from combine step)
                data[key] = float(value)
            elif isinstance(value, str):
                # Skip non-numeric values like status messages
                continue
        
        # Debug: Show what we're saving
        with st.expander("🔍 Debug: View Saved Health Data"):
            st.markdown("### 📊 Your Health Check Data")
            st.markdown("Here's what we're recording for today:")
            
            # Display in a user-friendly table format
            display_data = []
            for key, value in data.items():
                if key not in ['user_id', 'check_date', 'check_timestamp']:
                    # Format the key nicely
                    formatted_key = key.replace('_', ' ').title()
                    display_data.append({
                        'Metric': formatted_key,
                        'Value': f"{value:.4f}" if isinstance(value, float) else str(value)
                    })
            
            if display_data:
                st.table(display_data)
            
            st.caption(f"✅ Saving {len(display_data)} health metrics for {check_date}")
        
        # Upsert (insert or update if exists for this date)
        response = supabase.table('health_checks').upsert(
            data,
            on_conflict='user_id,check_date'
        ).execute()
        
        # Also save to JSON as backup
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            backup_data = {
                "user_id": user_id,
                "date": date_str,
                "timestamp": check_timestamp,
                "features": features
            }
            
            file_path = DATA_DIR / f"{user_id}_{date_str}.json"
            with open(file_path, 'w') as f:
                json.dump(backup_data, f, indent=2)
        except Exception as backup_error:
            st.warning(f"Could not save backup file: {backup_error}")
        
        return True, "✅ Health check data saved to database successfully!"
        
    except Exception as e:
        error_msg = f"Error saving to database: {str(e)}"
        st.error(error_msg)
        
        # Try to save to JSON as fallback
        try:
            user_id = st.session_state.get('user_id', 'default_user')
            date_str = datetime.now().strftime("%Y-%m-%d")
            timestamp = datetime.now().isoformat()
            
            fallback_data = {
                "user_id": user_id,
                "date": date_str,
                "timestamp": timestamp,
                "features": features
            }
            
            file_path = DATA_DIR / f"{user_id}_{date_str}.json"
            with open(file_path, 'w') as f:
                json.dump(fallback_data, f, indent=2)
            
            return True, "⚠️ Saved to local file (database unavailable)"
        except:
            return False, error_msg


def load_user_history():
    """Load all historical daily check data for current user from Supabase"""
    try:
        user_id = st.session_state.get('user_id')
        
        if not user_id:
            return []
        
        supabase = get_supabase_client()
        if not supabase:
            # Fallback to JSON files
            return load_user_history_from_json()
        
        # Query Supabase for user's health checks
        response = supabase.table('health_checks')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('check_date', desc=True)\
            .execute()
        
        if response.data:
            return response.data
        return []
        
    except Exception as e:
        st.warning(f"Could not load from database, trying local files: {str(e)}")
        return load_user_history_from_json()


def load_user_history_from_json():
    """Fallback: Load historical data from JSON files"""
    try:
        user_id = st.session_state.get('user_id', 'default_user')
        history = []
        
        # Find all files for this user
        for file_path in DATA_DIR.glob(f"{user_id}_*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    history.append(data)
            except Exception as e:
                st.warning(f"Could not load {file_path.name}: {str(e)}")
        
        # Sort by date
        history.sort(key=lambda x: x.get('date', ''), reverse=True)
        return history
    except Exception as e:
        st.error(f"Error loading history: {str(e)}")
        return []


def capture_camera_frames(duration: int):
    """
    Capture frames from webcam for specified duration
    Returns: list of frames (numpy arrays)
    """
    frames = []
    cap = None
    
    try:
        # Open webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Camera not available. Please check your webcam connection.")
            return None
        
        # Set camera properties for better quality
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Display placeholder for live preview
        preview_placeholder = st.empty()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        start_time = time.time()
        frame_count = 0
        
        while True:
            elapsed = time.time() - start_time
            
            if elapsed > duration:
                break
            
            # Read frame
            ret, frame = cap.read()
            
            if not ret:
                st.warning("Failed to capture frame")
                break
            
            # Convert BGR to RGB for Streamlit display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Add recording indicator
            cv2.putText(
                frame_rgb, 
                f"RECORDING: {int(duration - elapsed)}s", 
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (255, 0, 0), 
                2
            )
            
            # Display frame
            preview_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            
            # Store frame
            frames.append(frame)
            frame_count += 1
            
            # Update progress
            progress = min(elapsed / duration, 1.0)
            progress_bar.progress(progress)
            status_text.text(f"Captured {frame_count} frames | {int(duration - elapsed)}s remaining")
            
            time.sleep(0.03)  # ~30 FPS
        
        progress_bar.progress(1.0)
        status_text.text(f"✅ Captured {frame_count} frames successfully!")
        
        return frames
        
    except Exception as e:
        st.error(f"Error during capture: {str(e)}")
        return None
    finally:
        if cap is not None:
            cap.release()


def display_features_table(features: dict):
    """Display extracted features in a clean table format"""
    st.markdown("### 📊 Extracted Health Features")
    
    # Create DataFrame for display
    feature_data = []
    for key, value in features.items():
        # Format key for display
        display_name = key.replace('_', ' ').title()
        
        # Format value
        if isinstance(value, (int, float)):
            formatted_value = f"{value:.3f}"
        else:
            formatted_value = str(value)
        
        feature_data.append({
            "Feature": display_name,
            "Value": formatted_value
        })
    
    df = pd.DataFrame(feature_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


def display_history_trends():
    """Display historical trends using charts"""
    history = load_user_history()
    
    if not history:
        st.info("📊 No historical data yet. Complete your first daily check to start tracking trends!")
        return
    
    st.markdown("### 📈 Your Health Trends")
    
    # Prepare data for charting
    trend_data = []
    
    for record in reversed(history):  # Oldest to newest
        # Handle both database format and JSON format
        if 'check_date' in record:
            # Database format
            date_val = record.get('check_date', '')
            row = {'Date': date_val}
            
            # Add key metrics
            if 'avg_movement_speed' in record:
                row['Movement Speed'] = record['avg_movement_speed']
            if 'avg_stability' in record:
                row['Stability'] = record['avg_stability']
            if 'sit_stand_movement_speed' in record:
                row['Sit-Stand Speed'] = record['sit_stand_movement_speed']
            if 'walk_stability' in record:
                row['Walk Stability'] = record['walk_stability']
                
            trend_data.append(row)
        else:
            # JSON format (fallback)
            date_val = record.get('date', '')
            features = record.get('features', {})
            
            row = {'Date': date_val}
            
            # Extract key metrics from features
            if 'avg_movement_speed' in features:
                row['Movement Speed'] = features['avg_movement_speed']
            if 'avg_stability' in features:
                row['Stability'] = features['avg_stability']
                
            trend_data.append(row)
    
    if not trend_data:
        st.info("No trend data available")
        return
    
    df = pd.DataFrame(trend_data)
    
    if 'Date' not in df.columns or df.empty:
        st.info("Insufficient data for trends")
        return
    
    # Display charts for available metrics
    chart_columns = [col for col in df.columns if col != 'Date']
    
    if chart_columns:
        for col in chart_columns:
            if col in df.columns and df[col].notna().any():
                st.line_chart(df.set_index('Date')[col], use_container_width=True)
                st.caption(f"{col} Over Time")
    
    # Show full history table
    with st.expander("📋 View Full History"):
        st.dataframe(df, use_container_width=True)


# ==========================================
# MAIN PAGE FUNCTION
# ==========================================

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
                Camera-Based Movement Analysis & Health Drift Monitoring
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # DISCLAIMER
    # ========================================
    st.warning("""
    ⚠️ **Important Disclaimer**
    
    This system observes movement patterns to detect health drift over time. 
    It does **NOT diagnose medical conditions, diseases, or illnesses**. 
    This tool is for informational purposes only and should not replace professional medical advice.
    """)
    
    st.markdown("---")
    
    # ========================================
    # EXPLANATION
    # ========================================
    st.markdown("""
    ### 📋 How It Works
    
    This check observes your movement patterns to detect subtle changes (health drift) over time.
    
    **What we analyze:**
    - Movement speed and fluidity
    - Postural stability and balance
    - Motion smoothness and coordination
    
    **The Process:**
    1. **Sit to Stand** - Measures transition movement
    2. **Short Walk** - Assesses gait and coordination
    3. **Hold Steady** - Evaluates balance and stability
    
    Each step takes ~5 seconds. Your camera will be active during capture.
    """)
    
    st.markdown("---")
    
    # ========================================
    # INITIALIZE SESSION STATE
    # ========================================
    if 'check_step' not in st.session_state:
        st.session_state.check_step = 0
    
    if 'check_complete' not in st.session_state:
        st.session_state.check_complete = False
    
    if 'daily_health_features' not in st.session_state:
        st.session_state.daily_health_features = {}
    
    if 'step_features' not in st.session_state:
        st.session_state.step_features = {}
    
    # ========================================
    # WORKFLOW: STEP-BY-STEP CHECK
    # ========================================
    
    if not st.session_state.check_complete:
        current_step_idx = st.session_state.check_step
        
        # Check if all steps are done
        if current_step_idx >= len(STEPS):
            st.session_state.check_complete = True
            st.rerun()
        else:
            step = STEPS[current_step_idx]
            
            st.markdown(f"### Step {current_step_idx + 1} of {len(STEPS)}: {step['name']}")
            
            st.info(f"**Instructions:** {step['instruction']}")
            
            # Start capture button
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                if st.button(f"🎥 Start {step['name']}", type="primary", use_container_width=True):
                    with st.spinner(f"Recording {step['name']}..."):
                        # Capture frames
                        frames = capture_camera_frames(step['duration'])
                        
                        if frames and len(frames) > 0:
                            st.success(f"✅ {step['name']} recorded successfully!")
                            
                            # Extract features
                            with st.spinner("Analyzing movement patterns..."):
                                try:
                                    features = extract_features(frames, activity_name=step['key'])
                                    
                                    if features and isinstance(features, dict):
                                        # Store features for this step
                                        st.session_state.step_features[step['key']] = features
                                        
                                        # Display extracted features
                                        display_features_table(features)
                                        
                                        st.success("✅ Analysis complete!")
                                        
                                        # Move to next step
                                        time.sleep(1)
                                        st.session_state.check_step += 1
                                        st.rerun()
                                    else:
                                        st.error("Feature extraction returned invalid data")
                                
                                except Exception as e:
                                    st.error(f"Error extracting features: {str(e)}")
                        else:
                            st.error("Failed to capture frames. Please try again.")
    
    # ========================================
    # COMPLETION & RESULTS
    # ========================================
    else:
        st.success("🎉 **Daily Health Check Complete!**")
        
        # Combine all step features into final result
        combined_features = {}
        for step_key, features in st.session_state.step_features.items():
            for key, value in features.items():
                # Prefix with step name to avoid conflicts
                combined_key = f"{step_key}_{key}"
                combined_features[combined_key] = value
        
        # Also create summary averages for key metrics
        if st.session_state.step_features:
            movement_speeds = []
            stabilities = []
            
            for features in st.session_state.step_features.values():
                if 'movement_speed' in features:
                    movement_speeds.append(features['movement_speed'])
                if 'stability' in features:
                    stabilities.append(features['stability'])
            
            if movement_speeds:
                combined_features['avg_movement_speed'] = sum(movement_speeds) / len(movement_speeds)
            if stabilities:
                combined_features['avg_stability'] = sum(stabilities) / len(stabilities)
        
        # Store in session state
        st.session_state.daily_health_features = combined_features
        
        # Display all results
        st.markdown("### 📊 Complete Results")
        display_features_table(combined_features)
        
        # Auto-save data immediately
        if 'data_saved' not in st.session_state:
            with st.spinner("💾 Saving your health check data..."):
                success, message = save_daily_check_data(combined_features)
                if success:
                    st.success(message)
                    st.session_state.data_saved = True
                    st.session_state.check_completed = True  # Flag for AI Chat
                    st.session_state.has_health_check_data = True  # Flag for AI agents
                else:
                    st.error(message)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 New Check", use_container_width=True):
                st.session_state.check_step = 0
                st.session_state.check_complete = False
                st.session_state.step_features = {}
                st.session_state.daily_health_features = {}
                st.session_state.pop('data_saved', None)
                st.rerun()
        
        with col2:
            if st.button("📊 View Dashboard", use_container_width=True, type="primary"):
                st.session_state.current_page = "Dashboard"
                st.rerun()
        
        with col3:
            if st.button("💬 AI Analysis", use_container_width=True):
                st.session_state.current_page = "AI Health Chat"
                st.rerun()
        
        st.markdown("---")
        
        # Display historical trends
        display_history_trends()
    
    st.markdown("---")
    
    # ========================================
    # FOOTER
    # ========================================
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 1rem 0;'>
        <small>
        🔒 Your privacy matters: No images or videos are stored. 
        Only numerical health features are saved for trend analysis.
        </small>
    </div>
    """, unsafe_allow_html=True)
